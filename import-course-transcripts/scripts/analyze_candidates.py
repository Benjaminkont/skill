#!/usr/bin/env python3
"""Read-only structural analysis for course transcript candidates.

The report is evidence for an agent's semantic review. This program never writes
to source or target directories and never declares a semantic winner.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Optional
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


SUPPORTED_SUFFIXES = {".md", ".txt", ".json", ".srt", ".vtt"}
TRACKING_QUERY_KEYS = {
    "from",
    "spm_id_from",
    "utm_campaign",
    "utm_content",
    "utm_medium",
    "utm_source",
    "utm_term",
    "vd_source",
}
TIMESTAMP_RE = re.compile(
    r"(?P<start>\d{1,2}:)?\d{1,2}:\d{2}[,.]\d{3}\s*-->\s*"
    r"(?P<end>\d{1,2}:)?\d{1,2}:\d{2}[,.]\d{3}"
)
URL_RE = re.compile(r"https?://[^\s\]\)\"']+")
TITLE_NUMBER_PATTERNS = (
    ("Lecture", re.compile(r"\b(?:lecture|lec)\s*0*(\d+)\b", re.I)),
    ("Unit", re.compile(r"\bunit\s*0*(\d+)\b", re.I)),
    ("Lecture", re.compile(r"第\s*0*(\d+)\s*讲")),
    ("Lecture", re.compile(r"(?:^|\s)0*(\d+)[.、]\s*")),
)
PART_RE = re.compile(r"(?:^|[\s_])p(?:art)?\s*0*(\d+)\b", re.I)


@dataclass(frozen=True)
class Extracted:
    text: str
    title: str
    source_url: str
    language: str
    segments: int
    duration_seconds: Optional[float]


@dataclass(frozen=True)
class Candidate:
    path: str
    origin: str
    format: str
    title: str
    source_url: str
    language: str
    lecture_kind: str
    lecture_number: Optional[int]
    lecture_number_source: str
    part_number: Optional[int]
    group_key: str
    characters: int
    words: int
    segments: int
    duration_seconds: Optional[float]
    repeated_segment_ratio: float
    replacement_characters: int
    control_characters: int
    text_sha256: str
    text_preview: str


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).replace("\u00a0", " ")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    output: list[str] = []
    blank = False
    for line in lines:
        if line:
            output.append(line)
            blank = False
        elif output and not blank:
            output.append("")
            blank = True
    return "\n".join(output).strip()


def canonicalize_url(value: str) -> str:
    match = URL_RE.search(value or "")
    if not match:
        return ""
    raw = match.group(0).rstrip(".,;:")
    parsed = urlsplit(raw)
    query = [
        (key, val)
        for key, val in parse_qsl(parsed.query, keep_blank_values=True)
        if key.casefold() not in TRACKING_QUERY_KEYS
    ]
    return urlunsplit(
        (parsed.scheme.casefold(), parsed.netloc.casefold(), parsed.path, urlencode(query), "")
    )


def parse_simple_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    marker = text.find("\n---", 4)
    if marker < 0:
        return {}, text
    frontmatter: dict[str, Any] = {}
    current_list: Optional[str] = None
    for line in text[4:marker].splitlines():
        item = re.match(r"^\s*-\s+[\"']?(.*?)[\"']?\s*$", line)
        if item and current_list:
            frontmatter.setdefault(current_list, []).append(item.group(1))
            continue
        field = re.match(r"^([A-Za-z_][\w-]*):\s*(.*?)\s*$", line)
        if not field:
            current_list = None
            continue
        key, value = field.groups()
        if not value:
            frontmatter[key] = []
            current_list = key
        else:
            frontmatter[key] = value.strip("\"'")
            current_list = None
    return frontmatter, text[marker + 4 :].lstrip("\n")


def extract_markdown(path: Path) -> Extracted:
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    frontmatter, body = parse_simple_frontmatter(raw)
    heading = re.search(r"^#\s+(.+?)\s*$", body, re.M)
    title = heading.group(1) if heading else path.stem
    if heading:
        body = body[: heading.start()] + body[heading.end() :]
    source_value = frontmatter.get("source", "")
    source_url = canonicalize_url(str(source_value))
    return Extracted(
        normalize_text(body),
        title,
        source_url,
        str(frontmatter.get("language", "")),
        count_segments(body),
        None,
    )


def extract_json(path: Path) -> Extracted:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(data, dict):
        segments = data.get("segments")
        title = str(data.get("title") or path.stem)
        source_url = canonicalize_url(str(data.get("source") or ""))
        if not source_url and isinstance(data.get("metadata"), dict):
            source_url = canonicalize_url(str(data["metadata"].get("webpage_url") or ""))
        language = str(data.get("language") or "")
        duration = numeric_or_none(data.get("duration"))
    elif isinstance(data, list):
        segments = data
        title, source_url, language, duration = path.stem, "", "", None
    else:
        raise ValueError("JSON root is not an object or list")
    if not isinstance(segments, list):
        raise ValueError("JSON does not contain a transcript segments list")
    text_parts: list[str] = []
    for segment in segments:
        if isinstance(segment, str):
            value = segment
        elif isinstance(segment, dict):
            value = segment.get("clean_text") or segment.get("raw_text") or segment.get("text") or ""
        else:
            value = ""
        value = str(value).strip()
        if value:
            text_parts.append(value)
    if not text_parts:
        raise ValueError("JSON transcript has no textual segments")
    return Extracted(
        normalize_text("\n\n".join(text_parts)),
        title,
        source_url,
        language,
        len(text_parts),
        duration,
    )


def extract_subtitles(path: Path) -> Extracted:
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    blocks = re.split(r"\n\s*\n", raw.replace("\r\n", "\n"))
    cues: list[str] = []
    max_end = 0.0
    for block in blocks:
        lines = block.splitlines()
        kept: list[str] = []
        skip_block = False
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped == "WEBVTT" or stripped.isdigit():
                continue
            if stripped.startswith(("NOTE", "STYLE", "REGION")):
                skip_block = True
                break
            if "-->" in stripped:
                match = TIMESTAMP_RE.search(stripped)
                if match:
                    max_end = max(max_end, timestamp_to_seconds(match.group(0).split("-->", 1)[1].strip()))
                continue
            stripped = html.unescape(re.sub(r"<[^>]+>", "", stripped))
            if stripped:
                kept.append(stripped)
        if kept and not skip_block:
            cues.append(" ".join(kept))
    if not cues:
        raise ValueError("subtitle file has no cues")
    return Extracted(
        normalize_text("\n\n".join(cues)),
        strip_variant_suffixes(path.stem),
        "",
        "",
        len(cues),
        max_end or None,
    )


def extract_text(path: Path) -> Extracted:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    return Extracted(
        normalize_text(text),
        strip_variant_suffixes(path.stem),
        "",
        "",
        count_segments(text),
        None,
    )


def extract(path: Path) -> Extracted:
    if path.suffix.casefold() == ".md":
        return extract_markdown(path)
    if path.suffix.casefold() == ".json":
        return extract_json(path)
    if path.suffix.casefold() in {".srt", ".vtt"}:
        return extract_subtitles(path)
    return extract_text(path)


def strip_variant_suffixes(value: str) -> str:
    return re.sub(
        r"(?:\.(?:clean|raw|bilingual|zh-CN|en))+$",
        "",
        value,
        flags=re.I,
    )


def numeric_or_none(value: Any) -> Optional[float]:
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def timestamp_to_seconds(value: str) -> float:
    pieces = value.replace(",", ".").split(":")
    try:
        if len(pieces) == 3:
            return float(pieces[0]) * 3600 + float(pieces[1]) * 60 + float(pieces[2])
        return float(pieces[0]) * 60 + float(pieces[1])
    except (ValueError, IndexError):
        return 0.0


def count_segments(text: str) -> int:
    paragraphs = [item for item in re.split(r"\n\s*\n|\n", text) if item.strip()]
    return len(paragraphs)


def repeat_ratio(text: str) -> float:
    parts = [re.sub(r"\s+", " ", item).strip().casefold() for item in re.split(r"\n\s*\n|\n", text)]
    parts = [item for item in parts if item]
    if not parts:
        return 0.0
    return round(1.0 - (len(set(parts)) / len(parts)), 4)


def detect_numbers(title: str, path: Path) -> tuple[str, Optional[int], str, Optional[int]]:
    part_match = PART_RE.search(f" {title} {path.as_posix()} ")
    part = int(part_match.group(1)) if part_match else None
    for kind, pattern in TITLE_NUMBER_PATTERNS:
        match = pattern.search(title)
        if match:
            return kind, int(match.group(1)), "title", part
    name_without_part = PART_RE.sub(" ", path.stem)
    for kind, pattern in TITLE_NUMBER_PATTERNS:
        match = pattern.search(name_without_part)
        if match:
            return kind, int(match.group(1)), "filename", part
    if part is not None:
        return "Part", part, "part", part
    return "", None, "", None


def normalized_title(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    value = re.sub(r"https?://\S+", " ", value)
    value = re.sub(r"[^\w]+", "-", value, flags=re.UNICODE).strip("-")
    return value[:96] or "untitled"


def make_group_key(course: str, kind: str, number: Optional[int], source_url: str, title: str) -> str:
    course_key = normalized_title(course)
    if number is not None:
        label = "unit" if kind == "Unit" else "lec"
        return f"{course_key}:{label}-{number:02d}"
    if source_url:
        return f"{course_key}:url-{hashlib.sha256(source_url.encode()).hexdigest()[:12]}"
    return f"{course_key}:title-{normalized_title(title)}"


def is_course_candidate(course: str, path: Path, extracted: Extracted, origin: str) -> bool:
    if origin == "target":
        return True
    needle = unicodedata.normalize("NFKC", course).casefold()
    haystack = unicodedata.normalize("NFKC", f"{path.as_posix()} {extracted.title}").casefold()
    return needle in haystack


def iter_files(roots: Iterable[tuple[Path, str]]) -> Iterable[tuple[Path, str]]:
    seen: set[Path] = set()
    for root, origin in roots:
        if not root.exists():
            continue
        scan_root = root / "原文" if origin == "target" and (root / "原文").is_dir() else root
        paths = [scan_root] if scan_root.is_file() else sorted(scan_root.rglob("*"))
        for path in paths:
            if not path.is_file() or path.suffix.casefold() not in SUPPORTED_SUFFIXES:
                continue
            if path.name.casefold() == "readme.md" or ".readme." in path.name.casefold():
                continue
            relative_parts = path.relative_to(scan_root).parts
            if origin == "target" and (path.name.casefold() == "readme.md" or "归档" in relative_parts):
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            yield path, origin


def analyze(args: argparse.Namespace) -> dict[str, Any]:
    roots = [(Path(item).expanduser(), "source") for item in args.source]
    explicit_source_files = {root.resolve() for root, _ in roots if root.is_file()}
    if args.target:
        roots.append((Path(args.target).expanduser(), "target"))
    candidates: list[Candidate] = []
    errors: list[dict[str, str]] = []
    for path, origin in iter_files(roots):
        if (
            origin == "source"
            and path.resolve() not in explicit_source_files
            and args.course.casefold() not in path.as_posix().casefold()
        ):
            continue
        try:
            extracted = extract(path)
            if not extracted.text:
                raise ValueError("empty extracted text")
            if not is_course_candidate(args.course, path, extracted, origin):
                continue
            kind, number, number_source, part = detect_numbers(extracted.title, path)
            source_url = canonicalize_url(extracted.source_url)
            group_key = make_group_key(args.course, kind, number, source_url, extracted.title)
            text = extracted.text
            candidates.append(
                Candidate(
                    path=str(path.resolve()),
                    origin=origin,
                    format=path.suffix.casefold().lstrip("."),
                    title=extracted.title,
                    source_url=source_url,
                    language=extracted.language,
                    lecture_kind=kind,
                    lecture_number=number,
                    lecture_number_source=number_source,
                    part_number=part,
                    group_key=group_key,
                    characters=len(text),
                    words=len(re.findall(r"\b\w+\b", text, flags=re.UNICODE)),
                    segments=extracted.segments,
                    duration_seconds=extracted.duration_seconds,
                    repeated_segment_ratio=repeat_ratio(text),
                    replacement_characters=text.count("�"),
                    control_characters=sum(
                        1 for char in text if unicodedata.category(char) == "Cc" and char not in "\n\t"
                    ),
                    text_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    text_preview=re.sub(r"\s+", " ", text)[: args.preview_chars],
                )
            )
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as error:
            if args.course.casefold() in path.as_posix().casefold() or origin == "target":
                errors.append({"path": str(path.resolve()), "error": str(error)})
    groups: dict[str, list[Candidate]] = {}
    for candidate in candidates:
        groups.setdefault(candidate.group_key, []).append(candidate)
    ordered_groups = []
    for key, items in sorted(
        groups.items(),
        key=lambda pair: (
            min(item.lecture_number if item.lecture_number is not None else 10**9 for item in pair[1]),
            pair[0],
        ),
    ):
        max_chars = max(item.characters for item in items) or 1
        candidate_rows = []
        for item in sorted(items, key=lambda value: (value.origin != "target", value.path)):
            row = asdict(item)
            row["relative_completeness"] = round(item.characters / max_chars, 4)
            candidate_rows.append(row)
        ordered_groups.append({"group_key": key, "candidates": candidate_rows})
    numbers = sorted(
        {
            item.lecture_number
            for item in candidates
            if item.lecture_number is not None and item.lecture_kind != "Part"
        }
    )
    missing = list(range(numbers[0], numbers[-1] + 1)) if numbers else []
    missing = [number for number in missing if number not in numbers]
    return {
        "course": args.course,
        "sources": [str(Path(item).expanduser().resolve()) for item in args.source],
        "target": str(Path(args.target).expanduser().resolve()) if args.target else "",
        "read_only": True,
        "semantic_selection_performed": False,
        "group_count": len(ordered_groups),
        "candidate_count": len(candidates),
        "numbered_lectures": numbers,
        "missing_between_min_and_max": missing,
        "groups": ordered_groups,
        "errors": errors,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# {report['course']} 候选结构分析",
        "",
        "> 只读结构证据；尚未进行语义质量选择，也未修改文件。",
        "",
        f"- 候选：{report['candidate_count']}",
        f"- 内容组：{report['group_count']}",
        f"- 编号：{', '.join(map(str, report['numbered_lectures'])) or '未识别'}",
        f"- 编号范围内缺项：{', '.join(map(str, report['missing_between_min_and_max'])) or '无'}",
        "",
        "| 内容组 | 来源 | 格式 | 讲次依据 | 分 P | 字符 | 相对完整度 | 重复率 | 乱码 | 路径 |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for group in report["groups"]:
        for item in group["candidates"]:
            number = item["lecture_number"]
            lecture = f"{item['lecture_kind']} {number}" if number is not None else "未识别"
            basis = f"{lecture}（{item['lecture_number_source'] or '无'}）"
            lines.append(
                "| {group} | {origin} | {format} | {basis} | {part} | {chars} | {complete:.1%} | "
                "{repeat:.1%} | {bad} | `{path}` |".format(
                    group=group["group_key"],
                    origin=item["origin"],
                    format=item["format"],
                    basis=basis,
                    part=item["part_number"] if item["part_number"] is not None else "",
                    chars=item["characters"],
                    complete=item["relative_completeness"],
                    repeat=item["repeated_segment_ratio"],
                    bad=item["replacement_characters"] + item["control_characters"],
                    path=item["path"].replace("|", "\\|"),
                )
            )
    if report["errors"]:
        lines.extend(["", "## 无法解析", ""])
        for item in report["errors"]:
            lines.append(f"- `{item['path']}`：{item['error']}")
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", action="append", required=True, help="Source directory; repeatable")
    parser.add_argument("--target", help="Course directory or its 原文 directory")
    parser.add_argument("--course", required=True, help="Course token used to filter source candidates")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--preview-chars", type=int, default=160)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    report = analyze(args)
    if args.format == "json":
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
