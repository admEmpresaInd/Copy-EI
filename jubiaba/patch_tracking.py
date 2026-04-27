# Refactor: transforma blocos c.setFillColor/c.setFont/c.setCharSpace(T)/c.drawX(...)/c.setCharSpace(0)
# em chamadas para draw_tracked, garantindo isolamento de estado.
import re, io

path = r"D:\Copy EI\Jubiabá\build_deck_v2.py"
with open(path, 'r', encoding='utf-8') as f:
    src = f.read()

# Pattern que reconhece:
#   c.setFillColor(COLOR)
#   c.setFont(FONT, SIZE)
#   c.setCharSpace(TRACK)
#   c.drawString|drawCentredString|drawRightString(X, Y, TEXT)
#   c.setCharSpace(0)

pattern = re.compile(
    r"(?P<indent>[ \t]+)c\.setFillColor\((?P<color>[^)]+)\)\s*\n"
    r"[ \t]+c\.setFont\((?P<font>[^,]+),\s*(?P<size>[^)]+)\)\s*\n"
    r"[ \t]+c\.setCharSpace\((?P<track>[^)]+)\)\s*\n"
    r"[ \t]+c\.(?P<draw>drawString|drawCentredString|drawRightString)\((?P<args>[^)]+)\)\s*\n"
    r"[ \t]+c\.setCharSpace\(0\)"
)

ALIGN_MAP = {
    'drawString': 'left',
    'drawCentredString': 'center',
    'drawRightString': 'right',
}

def split_args(args):
    # args = "X, Y, TEXT"  — split into 3 by first two commas (respecting strings/parens)
    depth = 0
    in_str = None
    parts = []
    cur = ''
    for ch in args:
        if in_str:
            cur += ch
            if ch == in_str:
                in_str = None
            continue
        if ch in ('"', "'"):
            in_str = ch; cur += ch; continue
        if ch in '([{':
            depth += 1; cur += ch; continue
        if ch in ')]}':
            depth -= 1; cur += ch; continue
        if ch == ',' and depth == 0 and len(parts) < 2:
            parts.append(cur.strip()); cur = ''
            continue
        cur += ch
    parts.append(cur.strip())
    return parts

def repl(m):
    indent = m.group('indent')
    color = m.group('color').strip()
    font  = m.group('font').strip()
    size  = m.group('size').strip()
    track = m.group('track').strip()
    draw  = m.group('draw')
    args  = m.group('args')
    align = ALIGN_MAP[draw]
    parts = split_args(args)
    if len(parts) != 3:
        return m.group(0)  # fallback: deixa como está
    x, y, text = parts
    return (f"{indent}draw_tracked(c, {x}, {y}, {text}, "
            f"{font}, {size}, {color}, tracking={track}, align='{align}')")

new_src, n = pattern.subn(repl, src)
with open(path, 'w', encoding='utf-8') as f:
    f.write(new_src)
print(f"Replacements: {n}")
