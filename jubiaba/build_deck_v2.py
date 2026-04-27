# -*- coding: utf-8 -*-
"""
Masterplan KV - Jubiabá — Deck v2
Design system fiel ao site gswp.com.br
- Paleta: void #090907, gold #B8942E, cream #F0EDE6
- Tipografia: Cormorant Garamond (serif) + DM Sans (sans)
- Linguagem: editorial luxury real estate
"""
import os, io
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.colors import HexColor, Color
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas as _RLCanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PIL import Image as PILImage, ImageFilter

# Polyfill para setCharSpace (usado por ReportLab em TextObject, patchamos em Canvas)
def _canvas_set_char_space(self, amt):
    self._charSpace = amt
    self._code.append('%s Tc' % amt)
if not hasattr(_RLCanvas, 'setCharSpace'):
    _RLCanvas.setCharSpace = _canvas_set_char_space

# ============================================================
# PATHS
# ============================================================
BASE        = r"D:\Copy EI\Jubiabá"
OUT_PDF     = os.path.join(BASE, "masterplan-kv-v2.pdf")
PRANCHAS    = os.path.join(BASE, "selected_pages")
FONTS       = os.path.join(BASE, "fonts")
INV         = os.path.join(BASE, "Investidores SERGIPE")
FOTOS_AREA  = os.path.join(INV, r"FOTOS_\Fotos da Área")
FOTOS_REG   = os.path.join(INV, r"FOTOS_\Fotos da Região_")
ZANUTO      = r"D:\Copy EI\Fotos Zanuto"

# ============================================================
# FONTS
# ============================================================
pdfmetrics.registerFont(TTFont('Cormorant',       os.path.join(FONTS, 'cormorant-regular.ttf')))
pdfmetrics.registerFont(TTFont('Cormorant-Med',   os.path.join(FONTS, 'cormorant-medium.ttf')))
pdfmetrics.registerFont(TTFont('Cormorant-SB',    os.path.join(FONTS, 'cormorant-semibold.ttf')))
pdfmetrics.registerFont(TTFont('DMSans',          os.path.join(FONTS, 'dmsans-regular.ttf')))
pdfmetrics.registerFont(TTFont('DMSans-Med',      os.path.join(FONTS, 'dmsans-medium.ttf')))
pdfmetrics.registerFont(TTFont('DMSans-Light',    os.path.join(FONTS, 'dmsans-light.ttf')))

SERIF      = 'Cormorant'
SERIF_MED  = 'Cormorant-Med'
SERIF_SB   = 'Cormorant-SB'
SANS       = 'DMSans'
SANS_MED   = 'DMSans-Med'
SANS_LT    = 'DMSans-Light'

# ============================================================
# PALETA (gswp.com.br)
# ============================================================
VOID       = HexColor('#090907')   # fundo principal (near-black warm)
VOID_SOFT  = HexColor('#1A1917')   # surface escuro secundário
SURFACE    = HexColor('#2C2B28')   # card/box surface
LINE       = HexColor('#3D3C38')   # divisores sutis
GOLD       = HexColor('#B8942E')   # dourado principal
GOLD_LIGHT = HexColor('#C4A84A')   # dourado claro / accent
GOLD_MUTE  = HexColor('#7E6420')   # dourado muted
CREAM      = HexColor('#F0EDE6')   # creme claro (body)
CREAM_SOFT = HexColor('#E8E3D8')   # creme secundário
WHITE_PURE = HexColor('#FAF8F4')   # branco off
MUTED      = HexColor('#A8A29A')   # cinza morno (captions)

# ============================================================
# PAGE (A3 landscape)
# ============================================================
PAGESIZE = landscape(A3)
W, H = PAGESIZE  # 1190.55 x 841.89 pt

# ============================================================
# IMAGE HELPERS
# ============================================================
def safe_img(path, bg_rgb=(9, 9, 7)):
    """Carrega imagem, flattening RGBA sobre fundo VOID."""
    img = PILImage.open(path)
    if img.mode in ('RGBA', 'LA', 'P'):
        bg = PILImage.new('RGB', img.size, bg_rgb)
        src = img.convert('RGBA') if img.mode == 'P' else img
        if src.mode == 'RGBA':
            bg.paste(src, mask=src.split()[3])
        else:
            bg.paste(src)
        img = bg
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=92)
    buf.seek(0)
    return ImageReader(buf)

def darken_img(path, factor=0.55, blur=0):
    """Escurece imagem (para usar como fundo com overlay editorial)."""
    img = PILImage.open(path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    if blur > 0:
        img = img.filter(ImageFilter.GaussianBlur(blur))
    # Blend com preto
    black = PILImage.new('RGB', img.size, (9, 9, 7))
    out = PILImage.blend(img, black, 1 - factor)
    buf = io.BytesIO()
    out.save(buf, format='JPEG', quality=90)
    buf.seek(0)
    return ImageReader(buf)

def cover_rect(c, img_reader, x, y, w, h, img_w, img_h):
    """Desenha imagem no retângulo (x,y,w,h) cobrindo-o (crop proporcional)."""
    target_ratio = w / h
    img_ratio = img_w / img_h
    if img_ratio > target_ratio:
        new_w = h * img_ratio
        new_h = h
        dx = x - (new_w - w) / 2
        dy = y
    else:
        new_w = w
        new_h = w / img_ratio
        dx = x
        dy = y - (new_h - h) / 2
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, w, h)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(img_reader, dx, dy, new_w, new_h, mask='auto')
    c.restoreState()

def fit_rect(c, img_reader, x, y, w, h, img_w, img_h):
    """Desenha imagem centralizada dentro de (x,y,w,h) (fit/contain)."""
    target_ratio = w / h
    img_ratio = img_w / img_h
    if img_ratio > target_ratio:
        new_w = w
        new_h = w / img_ratio
    else:
        new_h = h
        new_w = h * img_ratio
    dx = x + (w - new_w) / 2
    dy = y + (h - new_h) / 2
    c.drawImage(img_reader, dx, dy, new_w, new_h, mask='auto')

def get_img_size(path):
    with PILImage.open(path) as im:
        return im.size

# ============================================================
# DESIGN PRIMITIVES (gswp style)
# ============================================================
def fill_void(c):
    c.setFillColor(VOID)
    c.rect(0, 0, W, H, stroke=0, fill=1)

def draw_hairline(c, x1, y1, x2, y2, color=GOLD, width=0.4):
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)

def draw_overlay(c, x, y, w, h, alpha=0.62):
    c.saveState()
    c.setFillColor(Color(9/255, 9/255, 7/255, alpha=alpha))
    c.rect(x, y, w, h, stroke=0, fill=1)
    c.restoreState()

def draw_gradient_bottom(c, x, y, w, h, steps=40, alpha_top=0.0, alpha_bot=0.85):
    """Gradiente vertical do topo (transparente) para baixo (escuro)."""
    for i in range(steps):
        t = i / (steps - 1)
        a = alpha_top + (alpha_bot - alpha_top) * t
        c.setFillColor(Color(9/255, 9/255, 7/255, alpha=a))
        yy = y + h - (i + 1) * (h / steps)
        c.rect(x, yy, w, h / steps + 0.5, stroke=0, fill=1)

def draw_gradient_top(c, x, y, w, h, steps=40, alpha_top=0.85, alpha_bot=0.0):
    for i in range(steps):
        t = i / (steps - 1)
        a = alpha_top + (alpha_bot - alpha_top) * t
        c.setFillColor(Color(9/255, 9/255, 7/255, alpha=a))
        yy = y + h - (i + 1) * (h / steps)
        c.rect(x, yy, w, h / steps + 0.5, stroke=0, fill=1)

def draw_tracked(c, x, y, text, font, size, color, tracking=2.0, align='left'):
    """Desenha texto com letter-spacing usando TextObject, isolado do estado do canvas."""
    c.setFillColor(color)
    c.setFont(font, size)
    t = c.beginText()
    t.setFont(font, size)
    t.setCharSpace(tracking)
    t.setFillColor(color)
    try:
        text_w = c.stringWidth(text, font, size) + tracking * max(len(text) - 1, 0)
    except Exception:
        text_w = c.stringWidth(text, font, size)
    if align == 'center':
        x_draw = x - text_w / 2
    elif align == 'right':
        x_draw = x - text_w
    else:
        x_draw = x
    t.setTextOrigin(x_draw, y)
    t.textOut(text)
    # Reset dentro do TextObject antes de fechá-lo
    t.setCharSpace(0)
    c.drawText(t)
    # Força reset no canvas também
    c.setCharSpace(0)

def draw_eyebrow(c, x, y, text, color=GOLD, size=8.5, tracking=2.8):
    """Eyebrow text — pequeno, uppercase, tracked."""
    draw_tracked(c, x, y, text.upper(), SANS_MED, size, color, tracking)

def draw_gold_bar(c, x, y, length=42, width=0.6):
    """Barra dourada horizontal (linha marca do deck)."""
    c.setStrokeColor(GOLD)
    c.setLineWidth(width)
    c.line(x, y, x + length, y)

def draw_footer(c, page_num, total):
    """Rodapé editorial GSWP style."""
    # Linha dourada fina
    c.setStrokeColor(GOLD_MUTE)
    c.setLineWidth(0.3)
    c.line(40, 26, W - 40, 26)
    # Wordmark
    draw_tracked(c, 40, 14, 'JUBIABÁ', SERIF_MED, 8, GOLD, tracking=2.0, align='left')
    # Center
    draw_tracked(c, W/2, 14, 'CONFIDENCIAL · USO EXCLUSIVO INVESTIDORES', SANS_LT, 6, MUTED, tracking=1.6, align='center')
    # Page number
    c.setFillColor(MUTED)
    c.setFont(SANS, 7)
    c.drawRightString(W - 40, 14, f'{page_num:02d} / {total:02d}')

def wrap_text(text, max_width_chars):
    """Simple word wrap by character count."""
    words = text.split(' ')
    lines = []
    cur = ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if len(test) <= max_width_chars:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def draw_paragraph(c, x, y, text, font=SANS_LT, size=10, leading=16, color=CREAM, max_width_chars=62):
    c.setFillColor(color)
    c.setFont(font, size)
    lines = wrap_text(text, max_width_chars)
    yy = y
    for ln in lines:
        c.drawString(x, yy, ln)
        yy -= leading
    return yy

# ============================================================
# SLIDE TYPES
# ============================================================
def slide_prancha_fullbleed(c, img_path, page_num, total):
    """TIPO A: prancha do KV em full-bleed."""
    iw, ih = get_img_size(img_path)
    img = safe_img(img_path)
    cover_rect(c, img, 0, 0, W, H, iw, ih)
    # Rodapé sutil (sem overlay pesado sobre a prancha)
    # Apenas numeração e wordmark discretos sobre barra fina escura
    c.saveState()
    c.setFillColor(Color(9/255, 9/255, 7/255, alpha=0.78))
    c.rect(0, 0, W, 28, stroke=0, fill=1)
    c.restoreState()
    c.setStrokeColor(GOLD_MUTE)
    c.setLineWidth(0.3)
    c.line(40, 27, W - 40, 27)
    draw_tracked(c, 40, 12, 'JUBIABÁ', SERIF_MED, 8, GOLD, tracking=2.0, align='left')
    draw_tracked(c, W/2, 12, 'MASTERPLAN · KV ARCHITECTS · 2025', SANS_LT, 6, MUTED, tracking=1.6, align='center')
    c.setFillColor(MUTED)
    c.setFont(SANS, 7)
    c.drawRightString(W - 40, 12, f'{page_num:02d} / {total:02d}')

# ----- CONTEXT SLIDES -----
def slide_cover(c, page_num, total):
    """CAPA: foto aérea full-bleed + overlay + wordmark central."""
    bg = os.path.join(INV, "ÁREA TOTAL JUBIABÁ.jpeg")
    iw, ih = get_img_size(bg)
    img = darken_img(bg, factor=0.28, blur=3)
    cover_rect(c, img, 0, 0, W, H, iw, ih)
    # Escurecimento adicional em gradiente central
    draw_overlay(c, 0, 0, W, H, alpha=0.42)
    draw_gradient_bottom(c, 0, 0, W, H * 0.45, steps=50, alpha_top=0.0, alpha_bot=0.65)
    draw_gradient_top(c, 0, H * 0.55, W, H * 0.45, steps=50, alpha_top=0.65, alpha_bot=0.0)

    # Eyebrow superior
    draw_gold_bar(c, 60, H - 62, length=50, width=0.6)
    draw_eyebrow(c, 60, H - 78, 'Greystone Wellness Propriety', color=GOLD, size=8, tracking=2.8)

    # Wordmark JUBIABÁ grande — centrado vertical
    wordmark_baseline = H/2 + 30
    draw_tracked(c, W/2, wordmark_baseline, 'JUBIABÁ',
                 SERIF, 170, CREAM, tracking=14, align='center')

    # Linha fina dourada divisor abaixo do wordmark
    c.setStrokeColor(GOLD_MUTE)
    c.setLineWidth(0.5)
    c.line(W/2 - 80, wordmark_baseline - 32, W/2 + 80, wordmark_baseline - 32)

    # Subtítulo editorial — centrado, abaixo do wordmark e da linha
    c.setFillColor(GOLD_LIGHT)
    c.setFont(SERIF, 26)
    c.drawCentredString(W/2, wordmark_baseline - 64, 'Masterplan de um trecho de Brasil')

    draw_tracked(c, W/2, wordmark_baseline - 92,
                 'Praia dos Abais  ·  Estância  ·  Sergipe  ·  Litoral Sul',
                 SANS_LT, 10.5, CREAM_SOFT, tracking=2.4, align='center')

    # Rodapé da capa — metadata editorial
    c.setStrokeColor(GOLD_MUTE)
    c.setLineWidth(0.4)
    c.line(60, 95, W - 60, 95)

    draw_tracked(c, 60, 75, 'MASTERPLAN  ·  KV ARCHITECTS', SANS_LT, 7, MUTED, tracking=1.8, align='left')
    draw_tracked(c, 60, 60, 'APRESENTAÇÃO A INVESTIDORES  ·  2026', SANS_LT, 7, MUTED, tracking=1.8, align='left')
    draw_tracked(c, W - 60, 75, 'VOL. I', SANS_LT, 7, MUTED, tracking=1.8, align='right')
    draw_tracked(c, W - 60, 60, 'CONFIDENCIAL', SANS_LT, 7, MUTED, tracking=1.8, align='right')

def slide_sumario(c, page_num, total):
    """SUMÁRIO editorial."""
    fill_void(c)
    # Header
    draw_gold_bar(c, 60, H - 90, length=50)
    draw_eyebrow(c, 60, H - 78, 'Sumário', size=8, tracking=2.8)

    c.setFillColor(CREAM)
    c.setFont(SERIF, 62)
    c.drawString(60, H - 160, 'Índice')

    c.setFillColor(MUTED)
    c.setFont(SERIF_MED, 18)
    c.drawString(60, H - 195, 'Do território ao flywheel de investimento.')

    # Lista em 2 colunas
    items = [
        ('I',    'O Território',              'Praia dos Abais · Estância'),
        ('II',   'A Oportunidade',            'ZEEC · Plano Diretor · Frente de mar'),
        ('III',  'Masterplan',                'KV Architects · Zoneamento · Produto'),
        ('IV',   'Arquitetura',               'Volumetrias · Densidade · Tipologias'),
        ('V',    'KV Architects',             'Parceiro estratégico · Cannes 2026'),
        ('VI',   'Hamam Global',              'Wellness Operator · Curadoria'),
        ('VII',  'A Escala',                  'Jubiabá vs. Jurerê Internacional'),
        ('VIII', 'Tese de Investimento',      'Flywheel · Ativo escasso · Yield'),
        ('IX',   'Contrarrapa',               'Next Steps · Contato'),
    ]

    col1_x = 60
    col2_x = 640
    col_w  = 480
    top_y  = H - 260
    row_h  = 50

    for i, (rom, title, sub) in enumerate(items):
        col = 0 if i < 5 else 1
        row = i if col == 0 else i - 5
        x = col1_x if col == 0 else col2_x
        y = top_y - row * row_h

        # roman numeral
        c.setFillColor(GOLD)
        c.setFont(SERIF_MED, 14)
        c.drawString(x, y, rom)
        # title
        c.setFillColor(CREAM)
        c.setFont(SERIF_MED, 24)
        c.drawString(x + 60, y, title)
        # sub
        c.setFillColor(MUTED)
        c.setFont(SANS_LT, 9)
        c.drawString(x + 60, y - 16, sub)
        # hairline
        c.setStrokeColor(LINE)
        c.setLineWidth(0.3)
        c.line(x, y - 26, x + col_w, y - 26)

    draw_footer(c, page_num, total)

def slide_context_projeto(c, page_num, total):
    """Contexto: O Projeto / Localização."""
    # foto região à direita
    foto = os.path.join(FOTOS_REG, "dji-1599-2-1.jpg")
    if not os.path.exists(foto):
        foto = os.path.join(FOTOS_REG, "foto-praia-do-saco-em-aracaju-sergipe-8803.jpg")
    iw, ih = get_img_size(foto)
    img = safe_img(foto)
    # metade direita
    cover_rect(c, img, W/2, 0, W/2, H, iw, ih)
    # metade esquerda void
    c.setFillColor(VOID)
    c.rect(0, 0, W/2, H, stroke=0, fill=1)

    # gradiente suave no meio
    draw_gradient_top(c, W/2, 0, 80, H, steps=40, alpha_top=0.65, alpha_bot=0.0)

    # conteúdo editorial à esquerda
    x = 60
    draw_gold_bar(c, x, H - 130, length=50)
    draw_eyebrow(c, x, H - 118, 'I  ·  O Território', size=8.5, tracking=2.8)

    c.setFillColor(CREAM)
    c.setFont(SERIF, 72)
    c.drawString(x, H - 220, 'O Projeto')

    c.setFillColor(GOLD_LIGHT)
    c.setFont(SERIF_MED, 22)
    c.drawString(x, H - 255, 'Praia dos Abais · Estância · Sergipe')

    # hairline
    c.setStrokeColor(LINE)
    c.setLineWidth(0.3)
    c.line(x, H - 280, x + 380, H - 280)

    # body
    body = ('Um trecho contínuo de frente de mar no Litoral Sul de Sergipe. '
            'Do Aeroporto de Aracaju — com voos diretos de São Paulo, Brasília e Rio. '
            'Da divisa da Bahia — acesso pela Linha Verde (SE-100). '
            'Zoneamento Ecológico-Econômico Costeiro aprovado. Plano Diretor sancionado. '
            'Masterplan KV ZEEC-compliant.')
    draw_paragraph(c, x, H - 310, body, font=SANS_LT, size=10.5, leading=17,
                   color=CREAM_SOFT, max_width_chars=62)

    # stats em baixo
    y_stat = 190
    c.setStrokeColor(LINE)
    c.setLineWidth(0.3)
    c.line(x, y_stat + 40, x + 500, y_stat + 40)

    stats = [
        ('2.000 ha', 'Área contínua'),
        ('12 km',    'Frente de mar'),
        ('ZEEC',     'Aprovado'),
    ]
    for i, (val, lab) in enumerate(stats):
        xs = x + i * 170
        c.setFillColor(GOLD)
        c.setFont(SERIF, 36)
        c.drawString(xs, y_stat, val)
        draw_tracked(c, xs, y_stat - 14, lab.upper(), SANS_LT, 7.5, MUTED, tracking=1.6, align='left')

    # caption da foto
    c.setFillColor(CREAM_SOFT)
    c.setFont(SERIF, 14)
    c.drawString(W/2 + 30, 60, 'Praia do Saco · Litoral Sul SE')
    draw_tracked(c, W/2 + 30, 46, 'COSTA PRESERVADA  ·  VISTA AÉREA', SANS_LT, 7, MUTED, tracking=1.6, align='left')

    draw_footer(c, page_num, total)

def slide_context_kv(c, page_num, total):
    """Contexto KV Architects."""
    fill_void(c)
    # header
    draw_gold_bar(c, 60, H - 90, length=50)
    draw_eyebrow(c, 60, H - 78, 'V  ·  Parceiro Estratégico', size=8.5, tracking=2.8)

    c.setFillColor(CREAM)
    c.setFont(SERIF, 72)
    c.drawString(60, H - 175, 'KV Architects')

    c.setFillColor(GOLD_LIGHT)
    c.setFont(SERIF_MED, 22)
    c.drawString(60, H - 208, 'Königsberger Vannucchi · arquitetura do território')

    c.setStrokeColor(LINE)
    c.setLineWidth(0.3)
    c.line(60, H - 232, W - 60, H - 232)

    # Two columns
    col1_x = 60
    col2_x = 640
    col_w  = 480

    # Col 1 — filosofia
    c.setFillColor(CREAM_SOFT)
    c.setFont(SERIF_MED, 20)
    c.drawString(col1_x, H - 290, 'Um escritório, uma tese.')

    p1 = ('Königsberger Vannucchi assina alguns dos masterplans mais relevantes do Brasil '
          'contemporâneo. Mixed-use em São Paulo, intervenções culturais na Paulista, '
          'projetos icônicos no Itaim. Em Jubiabá, o escritório opera no território: '
          'desenha a escala, a densidade e o compliance ZEEC.')
    draw_paragraph(c, col1_x, H - 325, p1, font=SANS_LT, size=10, leading=17,
                   color=CREAM_SOFT, max_width_chars=58)

    p2 = ('O produto é o território. A arquitetura é o instrumento que converte '
          'natureza preservada em ativo investível — sem sacrificar o que faz o lugar valer.')
    draw_paragraph(c, col1_x, H - 430, p2, font=SANS_LT, size=10, leading=17,
                   color=MUTED, max_width_chars=58)

    # Col 2 — Project tags / stats
    draw_tracked(c, col2_x, H - 290, 'PROJETOS DE REFERÊNCIA', SANS_MED, 8, GOLD, tracking=2.2, align='left')

    refs = [
        ('Mixed-Use',   'São Paulo'),
        ('Masterplan',  'Tatuapé'),
        ('Icônico',     'Itaim Bibi'),
        ('Cultura',     'Av. Paulista'),
    ]
    for i, (tag, loc) in enumerate(refs):
        y = H - 320 - i * 40
        # tag
        c.setFillColor(CREAM)
        c.setFont(SERIF_MED, 22)
        c.drawString(col2_x, y, tag)
        # separador
        c.setFillColor(GOLD_MUTE)
        c.setFont(SERIF, 22)
        c.drawString(col2_x + 130, y, '·')
        # local
        c.setFillColor(MUTED)
        c.setFont(SANS_LT, 11)
        c.drawString(col2_x + 150, y, loc)
        # hairline
        c.setStrokeColor(LINE)
        c.setLineWidth(0.3)
        c.line(col2_x, y - 10, col2_x + col_w, y - 10)

    # stat box inferior
    y_stat = 160
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.4)
    c.line(col2_x, y_stat + 50, col2_x + 220, y_stat + 50)

    c.setFillColor(GOLD)
    c.setFont(SERIF, 42)
    c.drawString(col2_x, y_stat, 'Cannes 2026')
    draw_tracked(c, col2_x, y_stat - 18, 'RECONHECIMENTO INTERNACIONAL', SANS_LT, 8, MUTED, tracking=1.8, align='left')

    # Pull quote
    c.setFillColor(GOLD_LIGHT)
    c.setFont(SERIF_MED, 26)
    c.drawString(60, 160, '"A natureza é o produto. A natureza é o ativo."')
    draw_tracked(c, 60, 138, 'KV ARCHITECTS  ·  TESE DE PROJETO', SANS_LT, 8, MUTED, tracking=1.6, align='left')

    draw_footer(c, page_num, total)

def slide_context_hamam(c, page_num, total):
    """Contexto Hamam Global."""
    # foto direita
    foto = os.path.join(FOTOS_REG, "55068306Master.jpg")
    if not os.path.exists(foto):
        fallbacks = ["55068218Master.jpg","55068290Master.jpg","55067858Master.jpg","barraca-sape-praia-do-saco-aracaju-se.jpg"]
        for fb in fallbacks:
            candidate = os.path.join(FOTOS_REG, fb)
            if os.path.exists(candidate):
                foto = candidate; break
    iw, ih = get_img_size(foto)
    img = darken_img(foto, factor=0.52, blur=1)
    cover_rect(c, img, 0, 0, W, H, iw, ih)
    # overlay
    draw_overlay(c, 0, 0, W, H, alpha=0.55)

    # Header
    draw_gold_bar(c, 60, H - 90, length=50)
    draw_eyebrow(c, 60, H - 78, 'VI  ·  Wellness Operator', size=8.5, tracking=2.8)

    c.setFillColor(CREAM)
    c.setFont(SERIF, 72)
    c.drawString(60, H - 175, 'Hamam Global')

    c.setFillColor(GOLD_LIGHT)
    c.setFont(SERIF_MED, 22)
    c.drawString(60, H - 208, 'A hospitalidade como curadoria de lugar.')

    c.setStrokeColor(GOLD_MUTE)
    c.setLineWidth(0.4)
    c.line(60, H - 232, W - 60, H - 232)

    # body
    body = ('Hamam Global opera o eixo wellness de Jubiabá. Não é hotelaria convencional — '
            'é curadoria de território. O programa integra spa, experiência termal, F&B assinado '
            'e residências privadas num sistema que captura o maior prêmio do mercado brasileiro: '
            'o yield da segunda casa com operação profissional.')
    draw_paragraph(c, 60, H - 280, body, font=SANS_LT, size=11, leading=18,
                   color=CREAM_SOFT, max_width_chars=90)

    # Três pilares
    pillars = [
        ('Spa & Termal',   'Programa wellness integrado à paisagem costeira.'),
        ('F&B Assinado',   'Beach club e restaurantes com curadoria gastronômica.'),
        ('Branded Res.',   'Residências com rental pool e operação profissional.'),
    ]
    y_p = 260
    col_w = (W - 120) / 3
    for i, (t, d) in enumerate(pillars):
        x = 60 + i * col_w
        # número
        c.setFillColor(GOLD)
        c.setFont(SERIF, 14)
        c.drawString(x, y_p + 80, f'0{i+1}')
        # hairline
        c.setStrokeColor(GOLD_MUTE)
        c.setLineWidth(0.3)
        c.line(x, y_p + 68, x + col_w - 30, y_p + 68)
        # título
        c.setFillColor(CREAM)
        c.setFont(SERIF_MED, 26)
        c.drawString(x, y_p + 38, t)
        # desc
        draw_paragraph(c, x, y_p + 12, d, font=SANS_LT, size=9.5, leading=15,
                       color=MUTED, max_width_chars=int((col_w-30)/5.4))

    draw_footer(c, page_num, total)

def slide_context_escala(c, page_num, total):
    """A Escala — comparativo Jurerê."""
    fill_void(c)
    # Header
    draw_gold_bar(c, 60, H - 90, length=50)
    draw_eyebrow(c, 60, H - 78, 'VII  ·  A Escala', size=8.5, tracking=2.8)

    c.setFillColor(CREAM)
    c.setFont(SERIF, 72)
    c.drawString(60, H - 175, 'Jubiabá × Jurerê')

    c.setFillColor(GOLD_LIGHT)
    c.setFont(SERIF_MED, 20)
    c.drawString(60, H - 205, 'Sobreposição em roxo · tamanho real do terreno.')

    c.setStrokeColor(LINE)
    c.setLineWidth(0.3)
    c.line(60, H - 228, W - 60, H - 228)

    # Imagem comparativa
    comp = os.path.join(INV, "Simulação de Jurerê, sobreposta em roxo pelo tamanho do terreno de Jubiabá.png")
    if os.path.exists(comp):
        iw, ih = get_img_size(comp)
        img = safe_img(comp)
        # fit no bloco central
        rect_x, rect_y, rect_w, rect_h = 60, 160, W - 440, H - 430
        fit_rect(c, img, rect_x, rect_y, rect_w, rect_h, iw, ih)
        # caption
        draw_tracked(c, 60, 140, 'JUBIABÁ (ROXO) SOBREPOSTO A JURERÊ INTERNACIONAL  ·  FLORIPA / SC',
                     SANS_LT, 7.5, MUTED, tracking=1.6, align='left')

    # Coluna lateral direita
    xs = W - 340
    draw_tracked(c, xs, H - 290, 'A LEITURA DA ESCALA', SANS_MED, 8, GOLD, tracking=2.2, align='left')

    p1 = ('Jurerê Internacional cabe inteiro dentro de Jubiabá. '
          'Não é comparação retórica — é sobreposição cartográfica.')
    draw_paragraph(c, xs, H - 320, p1, font=SERIF_MED, size=14, leading=20,
                   color=CREAM, max_width_chars=38)

    c.setStrokeColor(GOLD_MUTE)
    c.setLineWidth(0.3)
    c.line(xs, H - 420, xs + 280, H - 420)

    # Stats comparativos
    comps = [
        ('Jubiabá',  '2.000 ha'),
        ('Jurerê',   '≈ 670 ha'),
        ('Razão',    '≈ 3×'),
    ]
    for i, (lab, val) in enumerate(comps):
        y = H - 460 - i * 54
        draw_tracked(c, xs, y + 22, lab.upper(), SANS_LT, 8, MUTED, tracking=1.8, align='left')
        c.setFillColor(GOLD)
        c.setFont(SERIF, 32)
        c.drawRightString(xs + 280, y + 14, val)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.3)
        c.line(xs, y - 2, xs + 280, y - 2)

    draw_footer(c, page_num, total)

def slide_context_produto(c, page_num, total):
    """Contexto editorial — Produto / Natureza é o ativo."""
    # Background image darkened
    foto = os.path.join(ZANUTO, "07_FACHADA 02.jpg")
    if os.path.exists(foto):
        iw, ih = get_img_size(foto)
        img = darken_img(foto, factor=0.4)
        cover_rect(c, img, 0, 0, W, H, iw, ih)
    else:
        fill_void(c)

    draw_overlay(c, 0, 0, W, H, alpha=0.48)
    draw_gradient_bottom(c, 0, 0, W, H*0.5, steps=40, alpha_top=0.0, alpha_bot=0.75)

    # Big editorial quote center-left
    draw_gold_bar(c, 60, H - 130, length=50)
    draw_eyebrow(c, 60, H - 118, 'IV  ·  Arquitetura', size=8.5, tracking=2.8)

    c.setFillColor(CREAM)
    c.setFont(SERIF, 64)
    c.drawString(60, H - 230, 'A natureza é o produto.')
    c.setFillColor(GOLD_LIGHT)
    c.setFont(SERIF, 64)
    c.drawString(60, H - 300, 'A natureza é o ativo.')

    c.setStrokeColor(GOLD_MUTE)
    c.setLineWidth(0.4)
    c.line(60, H - 330, 60 + 320, H - 330)

    body = ('O masterplan KV preserva 70% da área em mata nativa e mangue. '
            'A densidade é calibrada ao território. O produto não é metro quadrado — '
            'é acesso vitalício a um pedaço intocado do litoral brasileiro.')
    draw_paragraph(c, 60, H - 365, body, font=SANS_LT, size=11, leading=18,
                   color=CREAM_SOFT, max_width_chars=70)

    # Pequeno caption inferior direito
    draw_tracked(c, W - 60, 56, 'VOLUMETRIA  ·  ZANUTO + KV  ·  2025', SANS_LT, 7.5, MUTED, tracking=1.6, align='right')

    draw_footer(c, page_num, total)

def slide_context_tese(c, page_num, total):
    """Tese de Investimento / Flywheel."""
    fill_void(c)
    # Header
    draw_gold_bar(c, 60, H - 90, length=50)
    draw_eyebrow(c, 60, H - 78, 'VIII  ·  Tese de Investimento', size=8.5, tracking=2.8)

    c.setFillColor(CREAM)
    c.setFont(SERIF, 68)
    c.drawString(60, H - 175, 'O Flywheel de Jubiabá')

    c.setFillColor(GOLD_LIGHT)
    c.setFont(SERIF_MED, 20)
    c.drawString(60, H - 208, 'Ativo escasso, ciclo composto, yield operacional.')

    c.setStrokeColor(LINE)
    c.setLineWidth(0.3)
    c.line(60, H - 232, W - 60, H - 232)

    # Flywheel — 4 estágios horizontais
    stages = [
        ('01', 'Território',   'Escassez estrutural', '2.000 ha · ZEEC · frente contínua.'),
        ('02', 'Masterplan',   'Arquitetura do lugar', 'KV + compliance + densidade calibrada.'),
        ('03', 'Operação',     'Wellness curadoria',  'Hamam Global · yield profissional.'),
        ('04', 'Ativo',        'Composição no tempo', 'Segunda casa com rental pool e brand.'),
    ]

    y_top = H - 300
    col_w = (W - 120 - 90) / 4  # 90pt for arrows
    x0 = 60
    for i, (num, title, sub, body) in enumerate(stages):
        x = x0 + i * (col_w + 30)
        # número grande dourado
        c.setFillColor(GOLD)
        c.setFont(SERIF, 48)
        c.drawString(x, y_top - 20, num)
        # linha fina
        c.setStrokeColor(GOLD_MUTE)
        c.setLineWidth(0.4)
        c.line(x, y_top - 38, x + col_w - 10, y_top - 38)
        # título
        c.setFillColor(CREAM)
        c.setFont(SERIF_MED, 24)
        c.drawString(x, y_top - 68, title)
        # sub em dourado
        c.setFillColor(GOLD_LIGHT)
        c.setFont(SERIF_MED, 12)
        c.drawString(x, y_top - 92, sub)
        # body
        draw_paragraph(c, x, y_top - 118, body, font=SANS_LT, size=9.5, leading=15,
                       color=MUTED, max_width_chars=int(col_w/5.2))
        # arrow between columns
        if i < 3:
            ax = x + col_w + 6
            c.setStrokeColor(GOLD_MUTE)
            c.setLineWidth(0.5)
            c.line(ax, y_top - 45, ax + 18, y_top - 45)
            # arrowhead
            c.line(ax + 18, y_top - 45, ax + 14, y_top - 42)
            c.line(ax + 18, y_top - 45, ax + 14, y_top - 48)

    # Stat row
    y_stat = 150
    c.setStrokeColor(GOLD_MUTE)
    c.setLineWidth(0.4)
    c.line(60, y_stat + 55, W - 60, y_stat + 55)

    stats = [
        ('70%',   'Preservação nativa'),
        ('12 km', 'Frente de mar'),
        ('ZEEC',  'Compliance total'),
        ('3×',    'Escala de Jurerê'),
    ]
    col_w = (W - 120) / 4
    for i, (v, l) in enumerate(stats):
        x = 60 + i * col_w
        c.setFillColor(GOLD)
        c.setFont(SERIF, 40)
        c.drawString(x, y_stat, v)
        draw_tracked(c, x, y_stat - 16, l.upper(), SANS_LT, 7.5, MUTED, tracking=1.8, align='left')

    draw_footer(c, page_num, total)

def slide_contrarapa(c, page_num, total):
    """CTA final - contrarapa editorial."""
    # Background image darkened aerea
    foto = os.path.join(INV, "Jubiabá 01 e 02.jpeg")
    if os.path.exists(foto):
        iw, ih = get_img_size(foto)
        img = darken_img(foto, factor=0.32, blur=3)
        cover_rect(c, img, 0, 0, W, H, iw, ih)
    else:
        fill_void(c)
    draw_overlay(c, 0, 0, W, H, alpha=0.55)

    # Center composition
    draw_gold_bar(c, W/2 - 25, H/2 + 150, length=50)

    draw_tracked(c, W/2, H/2 + 125, 'CONTRARRAPA', SANS_MED, 8.5, GOLD, tracking=2.8, align='center')

    c.setFillColor(CREAM)
    c.setFont(SERIF, 72)
    c.drawCentredString(W/2, H/2 + 50, 'Há um trecho de Brasil')

    c.setFillColor(GOLD_LIGHT)
    c.setFont(SERIF_MED, 72)
    c.drawCentredString(W/2, H/2 - 15, 'à venda.')

    c.setStrokeColor(GOLD_MUTE)
    c.setLineWidth(0.4)
    c.line(W/2 - 200, H/2 - 55, W/2 + 200, H/2 - 55)

    c.setFillColor(CREAM_SOFT)
    c.setFont(SERIF_MED, 18)
    c.drawCentredString(W/2, H/2 - 90, 'E ele não se repete.')

    # Contact block
    y_c = 210
    draw_tracked(c, W/2, y_c + 40, 'PARA APROFUNDAR  ·  NEXT STEPS', SANS_LT, 8, MUTED, tracking=2.4, align='center')

    c.setStrokeColor(GOLD_MUTE)
    c.setLineWidth(0.3)
    c.line(W/2 - 60, y_c + 20, W/2 + 60, y_c + 20)

    c.setFillColor(CREAM)
    c.setFont(SERIF_MED, 22)
    c.drawCentredString(W/2, y_c - 5, 'GSWP  ·  Greystone Wellness Propriety')

    c.setFillColor(MUTED)
    c.setFont(SANS_LT, 10)
    c.drawCentredString(W/2, y_c - 28, 'contato@gswp.com.br  ·  gswp.com.br/jubiaba')

    draw_footer(c, page_num, total)

# ============================================================
# DECK SEQUENCE
# ============================================================
def build_deck():
    c = canvas.Canvas(OUT_PDF, pagesize=PAGESIZE)
    c.setTitle('Masterplan KV · Jubiabá')
    c.setAuthor('GSWP — Greystone Wellness Propriety')
    c.setSubject('Apresentação a Investidores')

    # Sequence definition
    sequence = []
    sequence.append(('cover',   None))
    sequence.append(('sumario', None))
    sequence.append(('prancha', 'slide_01.png'))
    sequence.append(('prancha', 'slide_02.png'))
    sequence.append(('prancha', 'slide_03.png'))
    sequence.append(('ctx_projeto', None))
    sequence.append(('prancha', 'slide_05.png'))
    sequence.append(('prancha', 'slide_08.png'))
    sequence.append(('prancha', 'slide_09.png'))
    sequence.append(('prancha', 'slide_10.png'))
    sequence.append(('ctx_kv', None))
    sequence.append(('prancha', 'slide_12.png'))
    sequence.append(('ctx_produto', None))
    sequence.append(('prancha', 'slide_14.png'))
    sequence.append(('prancha', 'slide_16.png'))
    sequence.append(('prancha', 'slide_17.png'))
    sequence.append(('ctx_hamam', None))
    sequence.append(('prancha', 'slide_20.png'))
    sequence.append(('prancha', 'slide_22.png'))
    sequence.append(('prancha', 'slide_24.png'))
    sequence.append(('ctx_escala', None))
    sequence.append(('prancha', 'slide_27.png'))
    sequence.append(('prancha', 'slide_28.png'))
    sequence.append(('prancha', 'slide_29.png'))
    sequence.append(('ctx_tese', None))
    sequence.append(('prancha', 'slide_31.png'))
    sequence.append(('prancha', 'slide_33.png'))
    sequence.append(('prancha', 'slide_34.png'))
    sequence.append(('contrarapa', None))

    total = len(sequence)

    for idx, (kind, asset) in enumerate(sequence, start=1):
        if kind == 'cover':
            slide_cover(c, idx, total)
        elif kind == 'sumario':
            slide_sumario(c, idx, total)
        elif kind == 'prancha':
            slide_prancha_fullbleed(c, os.path.join(PRANCHAS, asset), idx, total)
        elif kind == 'ctx_projeto':
            slide_context_projeto(c, idx, total)
        elif kind == 'ctx_kv':
            slide_context_kv(c, idx, total)
        elif kind == 'ctx_produto':
            slide_context_produto(c, idx, total)
        elif kind == 'ctx_hamam':
            slide_context_hamam(c, idx, total)
        elif kind == 'ctx_escala':
            slide_context_escala(c, idx, total)
        elif kind == 'ctx_tese':
            slide_context_tese(c, idx, total)
        elif kind == 'contrarapa':
            slide_contrarapa(c, idx, total)
        c.showPage()
        print(f'  [{idx:02d}/{total}]  {kind:14s}  {asset or ""}')

    c.save()
    print(f'\nPDF gerado: {OUT_PDF}')
    print(f'Total de slides: {total}')

if __name__ == '__main__':
    build_deck()
