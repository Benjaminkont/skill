#!/usr/bin/env python3
"""Render JSON annotation data to self-contained SVG and optional PNG."""
import argparse
import base64
import io
import json
import math
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)


def region(value, bounds, name):
    if (not isinstance(value, list) or len(value) != 4
            or any(type(v) is not int for v in value)):
        raise ValueError(f'{name}: expected integer [x, y, width, height]')
    x, y, w, h = value
    bx, by, bw, bh = bounds
    if w <= 0 or h <= 0 or x < bx or y < by or x+w > bx+bw or y+h > by+bh:
        raise ValueError(f'{name}: outside bounds {bounds}')
    return x, y, w, h


def generate(spec_path):
    from PIL import Image

    spec = json.loads(spec_path.read_text(encoding='utf-8'))
    source = (spec_path.parent / spec['source']).resolve()
    with Image.open(source) as original:
        crop = region(spec.get('crop', [0, 0, *original.size]),
                      [0, 0, *original.size], 'crop')
        cx, cy, cw, ch = crop
        picture = original.crop((cx, cy, cx+cw, cy+ch))
        buf = io.BytesIO()
        picture.save(buf, format='PNG')
    items = spec.get('items')
    if not isinstance(items, list) or not items:
        raise ValueError('items must be a nonempty array')
    label_width = spec.get('label_width', 430)
    if type(label_width) is not int or label_width < 200:
        raise ValueError('label_width must be an integer >= 200')
    ox, oy = label_width + 110, 80
    cards = []
    previous_bottom = oy - 18
    for i, item in enumerate(items, 1):
        x, y, w, h = region(item['box'], crop, f'items[{i}].box')
        lines = item['lines']
        if (not isinstance(lines, list) or not 1 <= len(lines) <= 3
                or any(not isinstance(s, str) or not s or '\n' in s for s in lines)):
            raise ValueError(f'items[{i}].lines: expected 1 to 3 nonempty single-line strings')
        box = (ox+x-cx, oy+y-cy, w, h)
        height = 24 + 32 * len(lines)
        top = max(oy, box[1]+h/2-height/2, previous_bottom+18)
        cards.append((i, lines, box, top, height))
        previous_bottom = top + height
    width = ox + cw + 30
    height = math.ceil(max(oy+ch, previous_bottom)+30)
    root = ET.Element(f'{{{SVG}}}svg', {
        'width': str(width), 'height': str(height), 'viewBox': f'0 0 {width} {height}',
        'font-family': spec.get('font_family', 'PingFang SC, Hiragino Sans GB, Noto Sans CJK SC, sans-serif')})

    def node(tag, attrs=None, text=None):
        e = ET.SubElement(root, f'{{{SVG}}}{tag}',
                          {k.replace('_', '-'): str(v) for k, v in (attrs or {}).items()})
        e.text = text
        return e

    node('title', text=spec.get('title', '图片标注'))
    node('desc', text=spec.get('context', ''))
    node('rect', dict(width=width, height=height, fill='#f7f8fa'))
    if spec.get('title'):
        node('text', dict(x=30, y=46, font_size=25, fill='#192333'), spec['title'])
    node('image', dict(x=ox, y=oy, width=cw, height=ch,
                      href='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()))
    red = '#e53935'
    for i, lines, box, top, card_height in cards:
        x, y, w, h = box
        mid = top + card_height/2
        node('rect', dict(x=x, y=y, width=w, height=h, rx=8,
                          fill='none', stroke=red, stroke_width=3))
        node('rect', dict(x=30, y=top, width=label_width, height=card_height, rx=12,
                          fill='white', stroke='#dfe3e8', stroke_width=2))
        node('circle', dict(cx=65, cy=mid, r=19, fill=red))
        node('text', dict(x=65, y=mid+7, text_anchor='middle', font_size=20, fill='white'), str(i))
        for j, line in enumerate(lines):
            node('text', dict(x=102, y=top+31+j*32, font_size=24 if j == 0 else 19,
                              fill='#192333' if j == 0 else '#596579'), line)
        sx, sy, ex, ey = 30+label_width+12, mid, x-5, y+h/2
        node('line', dict(x1=sx, y1=sy, x2=ex, y2=ey, stroke=red, stroke_width=3))
        angle = math.atan2(ey-sy, ex-sx)
        points = [(ex, ey)]+[(ex-14*math.cos(angle+d), ey-14*math.sin(angle+d))
                              for d in (-0.45, 0.45)]
        node('polygon', dict(points=' '.join(f'{a},{b}' for a, b in points), fill=red))
    return ET.tostring(root, encoding='utf-8', xml_declaration=True), source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('spec', type=Path, help='JSON configuration')
    parser.add_argument('--svg', type=Path, required=True)
    parser.add_argument('--png', type=Path, help='Optional CairoSVG raster output')
    args = parser.parse_args()
    try:
        outputs = [p.resolve() for p in (args.svg, args.png) if p is not None]
        if len(set(outputs)) != len(outputs):
            raise ValueError('SVG and PNG outputs must be different paths')
        for out in outputs:
            if out.exists():
                raise FileExistsError(f'Output exists; choose a new filename: {out}')
            if not out.parent.is_dir():
                raise ValueError(f'Output directory does not exist: {out.parent}')
        svg, source = generate(args.spec.resolve())
        if source in outputs or args.spec.resolve() in outputs:
            raise ValueError('Output cannot replace source or configuration')
        png = None
        if args.png:
            import cairosvg
            png = cairosvg.svg2png(bytestring=svg)
        with args.svg.open('xb') as f:
            f.write(svg)
        if png is not None:
            with args.png.open('xb') as f:
                f.write(png)
        print(f'SVG: {args.svg.resolve()}')
        if args.png:
            print(f'PNG: {args.png.resolve()}')
        return 0
    except (ValueError, KeyError, TypeError, OSError, ImportError) as exc:
        print(f'Annotation failed: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
