#!/usr/bin/env python3
"""Convert a local exercise video to a verified looping GIF without overwriting files."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def run(args):
    return subprocess.run(args, check=True, capture_output=True, text=True).stdout


def probe(path):
    return json.loads(run([
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,nb_frames:format=duration',
        '-of', 'json', str(path),
    ]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--width', type=int, default=640)
    parser.add_argument('--fps', type=int, default=15)
    parser.add_argument('--colors', type=int, default=160)
    args = parser.parse_args()
    if not args.source.is_file():
        parser.error('source must be an existing local video')
    if args.output.exists():
        parser.error('output already exists; choose a new path')
    if args.output.suffix.lower() != '.gif':
        parser.error('output must have a .gif extension')
    if args.width < 2 or not 1 <= args.fps <= 60 or not 4 <= args.colors <= 256:
        parser.error('require width >= 2, fps 1..60, and colors 4..256')
    if not all(shutil.which(tool) for tool in ['ffmpeg', 'ffprobe']):
        parser.error('ffmpeg and ffprobe must be available on PATH')

    original = probe(args.source)
    stream = original['streams'][0]
    width = min(args.width, stream['width'])
    duration = float(original['format']['duration'])
    filters = (
        f'fps={args.fps},scale={width}:-2:flags=lanczos,split[a][b];'
        f'[a]palettegen=max_colors={args.colors}[p];'
        '[b][p]paletteuse=dither=bayer:bayer_scale=3'
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.gif-convert-', dir=args.output.parent) as tmp:
        result = Path(tmp) / 'result.gif'
        run(['ffmpeg', '-hide_banner', '-v', 'error', '-threads', '1',
             '-filter_complex_threads', '1', '-i', str(args.source),
             '-filter_complex', filters, '-an', '-loop', '0', str(result)])
        converted = probe(result)
        gif_stream = converted['streams'][0]
        gif_duration = float(converted['format']['duration'])
        if int(gif_stream['nb_frames']) < 2:
            raise ValueError('result has fewer than two frames')
        if abs(gif_duration - duration) > max(0.15, 2 / args.fps):
            raise ValueError('GIF duration differs materially from source')
        for media in [args.source, result]:
            run(['ffmpeg', '-hide_banner', '-v', 'error', '-xerror', '-threads', '1',
                 '-i', str(media), '-f', 'null', '-'])
        # Exclusive creation also protects a file created after the initial check.
        with args.output.open('xb') as dest, result.open('rb') as src:
            shutil.copyfileobj(src, dest)
    hasher = hashlib.sha256()
    with args.source.open('rb') as source_file:
        for chunk in iter(lambda: source_file.read(1024 * 1024), b''):
            hasher.update(chunk)
    digest = hasher.hexdigest()
    print(json.dumps({
        'source': str(args.source.resolve()), 'gif': str(args.output.resolve()),
        'source_sha256': digest, 'source_duration_seconds': duration,
        'gif_duration_seconds': gif_duration, 'source_dimensions': [stream['width'], stream['height']],
        'gif_dimensions': [gif_stream['width'], gif_stream['height']],
        'gif_frames': int(gif_stream['nb_frames']), 'fps': args.fps,
        'max_colors': args.colors,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
