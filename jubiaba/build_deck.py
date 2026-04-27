# -*- coding: utf-8 -*-
"""
Build Masterplan KV - Jubiaba investor deck (PDF, A3 landscape).
Output: D:/Copy EI/Jubiaba/masterplan-kv-deck.pdf
"""
import os
import io
from PIL import Image as PILImage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
BASE_JUBIABA = r"D:\Copy EI\Jubiabá"
BASE_FOTOS = r"D:\Copy EI\Fotos Zanuto"
EXTRACTED = os.path.join(BASE_JUBIABA, "extracted_images")
INV = os.path.join(BASE_JUBIABA, "Investidores SERGIPE")
AREA_DIR = os.path.join(INV, "FOTOS_", "Fotos da Área")
REGIAO_DIR = os.path.join(INV, "FOTOS_", "Fotos da Região_")
OUT_PDF = os.path.join(BASE_JUBIABA, "masterplan-kv-deck.pdf")

# ------------------------------------------------------------
# Palette
# ------------------------------------------------------------
BG = HexColor("#0A0906")
GOLD = HexColor("#B8942E")
GOLD_DIM = HexColor("#7E6620")
WHITE = HexColor("#FFFFFF")
CREME = HexColor("#F0EDE6")
MUTED = HexColor("#A8A29A")
BG_RGB = (10/255, 9/255, 6/255)

# ------------------------------------------------------------
# Page size
# ------------------------------------------------------------
W, H = landscape(A3)
MARGIN = 48

# ------------------------------------------------------------
# Fonts (fallback to built-in Helvetica if not available)
# ------------------------------------------------------------
FONT_REG = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_LIGHT = "Helvetica"

# ------------------------------------------------------------
# Image helper — always returns a reportlab ImageReader pointing to
# an RGB JPEG buffer. Handles RGBA/LA/P transparency by flattening onto BG.
# ------------------------------------------------------------
def safe_img(path):
    img = PILImage.open(path)
    if img.mode in ('RGBA', 'LA', 'P'):
        bg = PILImage.new('RGB', img.size, (10, 9, 6))
        src = img.convert('RGBA') if img.mode == 'P' else img
        mask = src.split()[3] if src.mode == 'RGBA' else None
        bg.paste(src, mask=mask)
        img = bg
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    # Downscale huge images to speed up rendering and shrink PDF
    max_px = 2800
    if max(img.size) > max_px:
        ratio = max_px / max(img.size)
        img = img.resize((int(img.size[0]*ratio), int(img.size[1]*ratio)), PILImage.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format='JPEG', quality=86, optimize=True)
    buf.seek(0)
    return ImageReader(buf)

def img_size(path):
    with PILImage.open(path) as im:
        return im.size

# ------------------------------------------------------------
# Drawing primitives
# ------------------------------------------------------------
def draw_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def full_bleed(c, img_path, overlay=0.55):
    c.drawImage(safe_img(img_path), 0, 0, W, H,
                preserveAspectRatio=False, mask='auto')
    c.setFillColor(Color(0.04, 0.035, 0.024, alpha=overlay))
    c.rect(0, 0, W, H, fill=1, stroke=0)

def draw_fitted(c, img_path, x, y, w, h, bg_fill=True):
    """Draws an image fitted to (w,h) preserving aspect, with BG padding."""
    iw, ih = img_size(img_path)
    ratio = min(w / iw, h / ih)
    nw, nh = iw * ratio, ih * ratio
    nx = x + (w - nw) / 2
    ny = y + (h - nh) / 2
    if bg_fill:
        c.setFillColor(BG)
        c.rect(x, y, w, h, fill=1, stroke=0)
    c.drawImage(safe_img(img_path), nx, ny, nw, nh,
                preserveAspectRatio=True, mask='auto')

def draw_cover(c, img_path, x, y, w, h):
    """Like CSS background-size: cover — fills area, may crop."""
    iw, ih = img_size(img_path)
    ratio = max(w / iw, h / ih)
    nw, nh = iw * ratio, ih * ratio
    nx = x + (w - nw) / 2
    ny = y + (h - nh) / 2
    c.saveState()
    p = c.beginPath()
    p.rect(x, y, w, h)
    c.clipPath(p, stroke=0, fill=0)
    c.drawImage(safe_img(img_path), nx, ny, nw, nh,
                preserveAspectRatio=True, mask='auto')
    c.restoreState()

def header_mark(c):
    """Small JUBIABA wordmark at top-left and page tag at top-right."""
    c.setFillColor(GOLD)
    c.setFont(FONT_BOLD, 9)
    c.drawString(MARGIN, H - 30, "JUBIABÁ")
    c.setFillColor(MUTED)
    c.setFont(FONT_REG, 8)
    c.drawRightString(W - MARGIN, H - 30, "MASTERPLAN · KV ARCHITECTS")
    c.setStrokeColor(GOLD_DIM)
    c.setLineWidth(0.4)
    c.line(MARGIN, H - 38, W - MARGIN, H - 38)

def footer_mark(c, page_num, total):
    c.setFillColor(MUTED)
    c.setFont(FONT_REG, 7.5)
    c.drawString(MARGIN, 22, "CONFIDENCIAL · USO EXCLUSIVO INVESTIDORES")
    c.drawRightString(W - MARGIN, 22, f"{page_num:02d} / {total:02d}")

def title_block(c, kicker, title, subtitle=None, y_top=None):
    if y_top is None:
        y_top = H - 110
    c.setFillColor(GOLD)
    c.setFont(FONT_BOLD, 11)
    c.drawString(MARGIN, y_top, kicker.upper())
    c.setFillColor(WHITE)
    c.setFont(FONT_BOLD, 36)
    c.drawString(MARGIN, y_top - 50, title)
    if subtitle:
        c.setFillColor(CREME)
        c.setFont(FONT_REG, 14)
        # wrap subtitle
        max_w = W - 2*MARGIN
        wrap_text(c, subtitle, MARGIN, y_top - 82, max_w, FONT_REG, 14, 18, CREME)

def wrap_text(c, text, x, y, max_w, font, size, leading, color, max_lines=None):
    c.setFillColor(color)
    c.setFont(font, size)
    words = text.split()
    line = ""
    cy = y
    lines_drawn = 0
    for w in words:
        test = (line + " " + w).strip()
        if pdfmetrics.stringWidth(test, font, size) <= max_w:
            line = test
        else:
            c.drawString(x, cy, line)
            cy -= leading
            lines_drawn += 1
            line = w
            if max_lines and lines_drawn >= max_lines:
                return cy
    if line:
        c.drawString(x, cy, line)
        cy -= leading
    return cy

def bullet_list(c, items, x, y, max_w, font=FONT_REG, size=12, leading=18, color=None):
    if color is None:
        color = CREME
    cy = y
    for it in items:
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, size)
        c.drawString(x, cy, "›")
        cy = wrap_text(c, it, x + 18, cy, max_w - 18, font, size, leading, color)
        cy -= 4
    return cy

def stat_box(c, x, y, w, h, number, label):
    c.setStrokeColor(GOLD_DIM)
    c.setLineWidth(0.6)
    c.rect(x, y, w, h, fill=0, stroke=1)
    c.setFillColor(GOLD)
    c.setFont(FONT_BOLD, 28)
    c.drawString(x + 16, y + h - 42, number)
    c.setFillColor(CREME)
    c.setFont(FONT_REG, 9.5)
    wrap_text(c, label, x + 16, y + h - 66, w - 32, FONT_REG, 9.5, 12, CREME)

# ------------------------------------------------------------
# Slide-level helpers
# ------------------------------------------------------------
SLIDES_TOTAL = 0  # patched at end

def new_slide(c):
    draw_bg(c)

def finalize_slide(c, page_idx):
    footer_mark(c, page_idx, SLIDES_TOTAL)
    c.showPage()

# ------------------------------------------------------------
# Content: choose representative page images and photos
# ------------------------------------------------------------
def page_path(n):
    return os.path.join(EXTRACTED, f"page_{n:02d}.png")

MASTER_PAGES = sorted([f for f in os.listdir(EXTRACTED) if f.startswith("page_")])
TOTAL_MASTER = len(MASTER_PAGES)

# Pick curated Zanuto renders
def zpath(name):
    return os.path.join(BASE_FOTOS, name)

FACHADAS = [zpath("09_FACHADA 03.jpg"), zpath("10_FACHADA 05.jpg"), zpath("07_FACHADA 02.jpg")]
PLANTAS = [zpath("05_PH_TERREO.jpg"), zpath("02_PH_P1_MEZANINO.jpg"),
           zpath("03_PH_P2_SETOR INTIMO.jpg"), zpath("04_PH_COBERTURA.jpg"),
           zpath("01_PH_SUBSOLO.jpg"), zpath("06_CORTE.jpg")]
GOURMET = [zpath("12_AREA GOURMET 01.jpg"), zpath("13_AREA GOURMET 02.jpg"),
           zpath("16_ESTAR E COZINHA.jpg"), zpath("17_ESTAR 01.jpg"),
           zpath("18_ESTAR 02.jpg"), zpath("19_COZINHA 02.jpg")]
INTERIORES = [zpath("21_SUÍTE MASTER.jpg"), zpath("22_BANHEIRO MASTER.jpg"),
              zpath("24_CLOSET 02.jpg"), zpath("25_BANHEIRO 02.jpg"),
              zpath("26_SUÍTE 01.jpg"), zpath("27_SUÍTE 02.jpg")]

# Region & Area photos (pick a handful of representative jpegs)
def pick_photos(d, limit=6):
    out = []
    if not os.path.isdir(d):
        return out
    for f in sorted(os.listdir(d)):
        low = f.lower()
        if low.endswith((".jpg", ".jpeg", ".png", ".webp")):
            out.append(os.path.join(d, f))
        if len(out) >= limit:
            break
    return out

REGIAO_PHOTOS = pick_photos(REGIAO_DIR, 6)
AREA_PHOTOS = pick_photos(AREA_DIR, 6)

AREA_TOTAL_IMG = os.path.join(INV, "ÁREA TOTAL JUBIABÁ.jpeg")
JUBIABA_01_02 = os.path.join(INV, "Jubiabá 01 e 02.jpeg")
JURERE_OVERLAY = os.path.join(INV, "Simulação de Jurerê, sobreposta em roxo pelo tamanho do terreno de Jubiabá.png")

# ------------------------------------------------------------
# Build PDF
# ------------------------------------------------------------
def build():
    c = canvas.Canvas(OUT_PDF, pagesize=landscape(A3))
    c.setTitle("Masterplan KV — Jubiabá")
    c.setAuthor("Empresa Independente · Jubiabá")
    c.setSubject("Investor Deck — Masterplan Jubiabá / KV Architects / Hamam Global")

    slide_fns = []

    # ========================================================
    # SLIDE 1 — Cover
    # ========================================================
    def s_cover(c, idx):
        new_slide(c)
        # Use first masterplan page as hero if available; otherwise a fachada
        hero = page_path(1) if os.path.exists(page_path(1)) else FACHADAS[0]
        c.drawImage(safe_img(hero), 0, 0, W, H, preserveAspectRatio=False, mask='auto')
        # Dark gradient overlay bottom
        c.setFillColor(Color(0.04, 0.035, 0.024, alpha=0.55))
        c.rect(0, 0, W, H, fill=1, stroke=0)
        # Title
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 13)
        c.drawString(MARGIN, H - 80, "MASTERPLAN · KV ARCHITECTS")
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 96)
        c.drawString(MARGIN, H/2 - 30, "JUBIABÁ")
        c.setFillColor(CREME)
        c.setFont(FONT_REG, 18)
        c.drawString(MARGIN, H/2 - 62, "A Próxima Fronteira do Luxo no Nordeste")
        c.setFillColor(MUTED)
        c.setFont(FONT_REG, 10.5)
        c.drawString(MARGIN, 80, "ESTÂNCIA · SERGIPE · BRASIL")
        c.drawString(MARGIN, 64, "EMPRESA INDEPENDENTE · HAMAM GLOBAL · KÖNIGSBERGER VANNUCCHI")
        finalize_slide(c, idx)
    slide_fns.append(s_cover)

    # ========================================================
    # SLIDE 2 — Sumário / O Projeto
    # ========================================================
    def s_sumario(c, idx):
        new_slide(c)
        header_mark(c)
        title_block(c, "O Projeto", "Um destino. Uma tese. Um masterplan.",
                    "Jubiabá é um empreendimento multifásico no litoral sul de Sergipe, desenhado pela KV Architects e operado em parceria com a Hamam Global. Residências, hospitalidade e experiência costeira em escala até hoje inédita no Nordeste brasileiro.")
        # 4 stat boxes
        box_w = (W - 2*MARGIN - 3*20) / 4
        box_h = 95
        by = 200
        stats = [
            ("+1,2M m²", "Área total do masterplan"),
            ("2 fases", "Jubiabá 01 e 02, integradas"),
            ("KV", "Königsberger Vannucchi — assinatura arquitetônica"),
            ("Hamam", "Curadoria global de hospitalidade e FF&E"),
        ]
        for i, (num, lab) in enumerate(stats):
            x = MARGIN + i*(box_w + 20)
            stat_box(c, x, by, box_w, box_h, num, lab)
        # Agenda
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, 155, "O QUE VOCÊ VERÁ NESTE DECK")
        agenda = [
            "1. Tese macro — por que Nordeste, por que agora",
            "2. Terreno, escala e localização — comparativo Jurerê",
            "3. Masterplan integral — as 35 páginas da KV",
            "4. Assinaturas — KV Architects e Hamam Global",
            "5. Produto — fachadas, plantas e interiores Zanuto",
            "6. Tese de investimento, VGV e próximos passos",
        ]
        cy = 128
        for a in agenda:
            c.setFillColor(CREME)
            c.setFont(FONT_REG, 10.5)
            c.drawString(MARGIN, cy, a)
            cy -= 16
        finalize_slide(c, idx)
    slide_fns.append(s_sumario)

    # ========================================================
    # SLIDE 3 — Por que agora — Nordeste
    # ========================================================
    def s_why_now(c, idx):
        new_slide(c)
        header_mark(c)
        # Side image
        img_w = W * 0.45
        if REGIAO_PHOTOS:
            draw_cover(c, REGIAO_PHOTOS[0], W - img_w, 60, img_w, H - 120)
        # Overlay on right image
        c.setFillColor(Color(0.04, 0.035, 0.024, alpha=0.30))
        c.rect(W - img_w, 60, img_w, H - 120, fill=1, stroke=0)
        # Text
        text_x = MARGIN
        text_w = W - img_w - MARGIN - 40
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(text_x, H - 130, "POR QUE AGORA")
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 34)
        c.drawString(text_x, H - 180, "O Nordeste virou")
        c.drawString(text_x, H - 215, "mercado de destino.")
        bullets = [
            "Fluxo internacional consolidado em Sergipe, Alagoas e Bahia — demanda qualificada por segunda residência de alto padrão.",
            "Infraestrutura aeroportuária e rodoviária do litoral sul de SE amadurecendo com investimentos federais e privados.",
            "Escassez estrutural de produto de altíssimo padrão com assinatura arquitetônica reconhecida nacionalmente.",
            "Câmbio e juros globais favorecem captação de investidor internacional — janela de 24–36 meses.",
        ]
        bullet_list(c, bullets, text_x, H - 260, text_w, size=11.5, leading=16)
        finalize_slide(c, idx)
    slide_fns.append(s_why_now)

    # ========================================================
    # SLIDE 4 — Localização & Acessos
    # ========================================================
    def s_localizacao(c, idx):
        new_slide(c)
        header_mark(c)
        title_block(c, "Localização", "Estância, litoral sul de Sergipe.",
                    "A 60 km do Aeroporto Internacional de Aracaju. No eixo de expansão natural entre Aracaju e a Costa Dourada baiana — uma das faixas litorâneas mais preservadas do país.")
        # 3 region photos strip
        strip_y = 120
        strip_h = 260
        gap = 20
        strip_w = (W - 2*MARGIN - 2*gap) / 3
        photos = REGIAO_PHOTOS[:3] if len(REGIAO_PHOTOS) >= 3 else (REGIAO_PHOTOS + AREA_PHOTOS)[:3]
        for i, p in enumerate(photos):
            x = MARGIN + i*(strip_w + gap)
            draw_cover(c, p, x, strip_y, strip_w, strip_h)
            # caption band
            c.setFillColor(Color(0.04, 0.035, 0.024, alpha=0.70))
            c.rect(x, strip_y, strip_w, 28, fill=1, stroke=0)
            c.setFillColor(GOLD)
            c.setFont(FONT_BOLD, 8.5)
            captions = ["PRAIA DO SACO", "AEROPORTO ARACAJU", "LITORAL ESTÂNCIA"]
            c.drawString(x + 10, strip_y + 10, captions[i] if i < len(captions) else "")
        finalize_slide(c, idx)
    slide_fns.append(s_localizacao)

    # ========================================================
    # SLIDE 5 — Escala Única (Jurerê overlay)
    # ========================================================
    def s_escala(c, idx):
        new_slide(c)
        header_mark(c)
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, H - 110, "ESCALA ÚNICA")
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 38)
        c.drawString(MARGIN, H - 160, "Do tamanho de Jurerê Internacional.")
        c.setFillColor(CREME)
        c.setFont(FONT_REG, 13)
        wrap_text(c, "A simulação em roxo abaixo sobrepõe o terreno de Jubiabá sobre Jurerê Internacional — o bairro-ícone de Florianópolis. Nosso masterplan ocupa a mesma malha urbana inteira.",
                  MARGIN, H - 195, W - 2*MARGIN, FONT_REG, 13, 18, CREME)
        # Big overlay image
        if os.path.exists(JURERE_OVERLAY):
            draw_fitted(c, JURERE_OVERLAY, MARGIN, 70, W - 2*MARGIN, H - 310)
        finalize_slide(c, idx)
    slide_fns.append(s_escala)

    # ========================================================
    # SLIDE 6 — O Terreno (ÁREA TOTAL)
    # ========================================================
    def s_terreno(c, idx):
        new_slide(c)
        header_mark(c)
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, H - 110, "O TERRENO")
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 34)
        c.drawString(MARGIN, H - 155, "Área total Jubiabá 01 + 02.")
        if os.path.exists(AREA_TOTAL_IMG):
            draw_fitted(c, AREA_TOTAL_IMG, MARGIN, 70, W - 2*MARGIN, H - 245)
        finalize_slide(c, idx)
    slide_fns.append(s_terreno)

    # ========================================================
    # SLIDE 7 — Jubiabá 01 e 02
    # ========================================================
    def s_fases(c, idx):
        new_slide(c)
        header_mark(c)
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, H - 110, "AS DUAS FASES")
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 34)
        c.drawString(MARGIN, H - 155, "Jubiabá 01 e 02 — masterplan integrado.")
        if os.path.exists(JUBIABA_01_02):
            draw_fitted(c, JUBIABA_01_02, MARGIN, 70, W - 2*MARGIN, H - 245)
        finalize_slide(c, idx)
    slide_fns.append(s_fases)

    # ========================================================
    # SLIDES 8..8+N — Masterplan pages (uma por slide, full-bleed elegante)
    # We include ALL 35 masterplan pages on their own slides.
    # ========================================================
    def make_master_page_slide(n, subtitle):
        def _slide(c, idx):
            new_slide(c)
            # Dark band top with page ref
            c.setFillColor(BG)
            c.rect(0, H - 50, W, 50, fill=1, stroke=0)
            c.setFillColor(GOLD)
            c.setFont(FONT_BOLD, 10)
            c.drawString(MARGIN, H - 32, f"MASTERPLAN · PRANCHA {n:02d} / {TOTAL_MASTER:02d}")
            c.setFillColor(MUTED)
            c.setFont(FONT_REG, 9)
            c.drawRightString(W - MARGIN, H - 32, subtitle)
            # Image fitted below band with padding
            pad = 30
            top_limit = H - 50 - 10
            bottom_limit = 40
            draw_fitted(c, page_path(n), pad, bottom_limit,
                        W - 2*pad, top_limit - bottom_limit)
            finalize_slide(c, idx)
        return _slide

    master_subtitles = [
        "Contexto & implantação",
        "Malha urbana & setorização",
        "Sistema viário principal",
        "Eixos estruturadores",
        "Distribuição de usos",
        "Áreas verdes & permeabilidade",
        "Plano de massas — visão geral",
        "Fase 01 — recorte",
        "Fase 01 — lotes & quadras",
        "Fase 01 — áreas comuns",
        "Fase 02 — recorte",
        "Fase 02 — lotes & quadras",
        "Fase 02 — hospitalidade",
        "Eixo praia-lagoa",
        "Circulações & transições",
        "Mobilidade interna",
        "Parque linear",
        "Marina & frente d'água",
        "Resort & beach club",
        "Spa, wellness & hamam",
        "Clubhouse & golf",
        "Centro de eventos",
        "Capela & retiros",
        "Equipamentos institucionais",
        "Sustentabilidade & água",
        "Manejo de dunas & vegetação",
        "Paisagismo — estratégia",
        "Materialidade & paleta",
        "Fachadas de referência",
        "Volumetrias de residências",
        "Tipologias & prumadas",
        "Painel de vistas",
        "Etapas de implantação",
        "Cronograma macro",
        "Síntese & próximos passos",
    ]
    for n in range(1, TOTAL_MASTER + 1):
        sub = master_subtitles[n-1] if n-1 < len(master_subtitles) else "Prancha de projeto"
        slide_fns.append(make_master_page_slide(n, sub))

    # ========================================================
    # KV Architects — Quem São
    # ========================================================
    def s_kv_who(c, idx):
        new_slide(c)
        header_mark(c)
        title_block(c, "Assinatura arquitetônica", "Königsberger Vannucchi.",
                    "Escritório paulistano de referência nacional em uso misto, residencial de alto padrão e masterplans de grande escala. Mais de cinco décadas redesenhando eixos urbanos em São Paulo e em capitais brasileiras.")
        pillars = [
            ("CRIAÇÃO COLABORATIVA", "Escutas e trocas constantes entre equipe e clientes — ideias lapidadas e integradas em ativos de valor comercial e cultural."),
            ("EXCELÊNCIA TÉCNICA", "Profissionais altamente experientes concebendo projetos cuidadosamente elaborados para atender aos mais altos padrões do mercado."),
            ("SUSTENTABILIDADE", "Arquitetura que responde aos desafios do nosso tempo e dialoga com o entorno — identificando mudanças e se reinventando."),
            ("REINVENÇÃO CONSTANTE", "Soluções responsáveis por meio de pensamento culturalmente comprometido, criativo e integrador."),
        ]
        col_w = (W - 2*MARGIN - 3*20) / 4
        col_h = 220
        by = 120
        for i, (h, t) in enumerate(pillars):
            x = MARGIN + i*(col_w + 20)
            c.setStrokeColor(GOLD_DIM)
            c.setLineWidth(0.6)
            c.rect(x, by, col_w, col_h, fill=0, stroke=1)
            c.setFillColor(GOLD)
            c.setFont(FONT_BOLD, 10.5)
            c.drawString(x + 16, by + col_h - 28, h)
            c.setFillColor(CREME)
            wrap_text(c, t, x + 16, by + col_h - 56, col_w - 32, FONT_REG, 10, 14, CREME)
        finalize_slide(c, idx)
    slide_fns.append(s_kv_who)

    # ========================================================
    # KV Architects — Portfólio
    # ========================================================
    def s_kv_portfolio(c, idx):
        new_slide(c)
        header_mark(c)
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, H - 110, "PORTFÓLIO KV")
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 34)
        c.drawString(MARGIN, H - 155, "Os projetos que desenharam uma cidade.")
        c.setFillColor(CREME)
        c.setFont(FONT_REG, 12)
        wrap_text(c, "Seleção de projetos recentes e icônicos do escritório — em uso misto, residencial de alto padrão, institucional e masterplan. O Jubiabá se soma a este portfólio como o maior e mais ambicioso masterplan litorâneo da KV.",
                  MARGIN, H - 185, W - 2*MARGIN, FONT_REG, 12, 16, CREME)
        projects = [
            ("LISBÔ", "Pinheiros · SP", "Uso misto · 236 unidades · HIS, HMP e padrão"),
            ("HY PINHEIROS", "Pinheiros · SP", "Uso misto · torre residencial premium"),
            ("BUENO BRANDÃO 257", "Jardins · SP", "Residencial de alto padrão"),
            ("ALMAGAH 227", "São Paulo · SP", "Residencial padrão elevado"),
            ("MONTELENA PLATINA 220", "São Paulo · SP", "Residencial boutique"),
            ("ARTE CONCRETA", "São Paulo · SP", "Residencial com assinatura"),
            ("SESC AV. PAULISTA", "Av. Paulista · SP", "Institucional · referência nacional"),
            ("MN15 · MEET SP", "São Paulo · SP", "Edifícios de escritórios"),
        ]
        cols = 4
        rows = 2
        gap = 18
        gw = (W - 2*MARGIN - (cols-1)*gap) / cols
        gh = 95
        by = 140
        for i, (name, loc, desc) in enumerate(projects):
            col = i % cols
            row = i // cols
            x = MARGIN + col*(gw + gap)
            y = by - row*(gh + gap)
            c.setStrokeColor(GOLD_DIM)
            c.setLineWidth(0.5)
            c.rect(x, y, gw, gh, fill=0, stroke=1)
            c.setFillColor(GOLD)
            c.setFont(FONT_BOLD, 11.5)
            c.drawString(x + 14, y + gh - 26, name)
            c.setFillColor(MUTED)
            c.setFont(FONT_REG, 8.5)
            c.drawString(x + 14, y + gh - 42, loc.upper())
            c.setFillColor(CREME)
            wrap_text(c, desc, x + 14, y + gh - 62, gw - 28, FONT_REG, 9, 12, CREME)
        finalize_slide(c, idx)
    slide_fns.append(s_kv_portfolio)

    # ========================================================
    # KV — Reconhecimento / Filosofia
    # ========================================================
    def s_kv_awards(c, idx):
        new_slide(c)
        header_mark(c)
        title_block(c, "Reconhecimento", "Arquitetura premiada, reconhecimento regional e nacional.",
                    "O escritório é reconhecido por ativos que se tornam marcos urbanos — com valor comercial e cultural consolidado. A KV atua com método próprio de escuta e co-criação com clientes e comunidades.")
        bullets = [
            "Reconhecimento regional e nacional como referência em uso misto e residencial premium.",
            "Obras publicadas em mídia especializada de arquitetura e mercado imobiliário.",
            "Sócio e CEO, Daniel Toledo, conduz missões técnicas da ADIT — Associação para o Desenvolvimento Imobiliário e Turístico do Brasil.",
            "Abordagem integrada: masterplan, arquitetura, interiores e paisagismo sob mesma direção criativa.",
            "Projetos sustentáveis com mobilidade ativa, bicicletário estruturado e serviços compartilhados como default.",
        ]
        bullet_list(c, bullets, MARGIN, H - 260, W - 2*MARGIN, size=12, leading=18)
        finalize_slide(c, idx)
    slide_fns.append(s_kv_awards)

    # ========================================================
    # Hamam Global — Quem São
    # ========================================================
    def s_hamam_who(c, idx):
        new_slide(c)
        header_mark(c)
        title_block(c, "Curadoria de hospitalidade", "Hamam Global.",
                    "Mais de 26 anos de expertise em procurement para empreendimentos hoteleiros e residenciais de altíssimo padrão. Presença em São Paulo, Miami e Dubai.")
        pillars = [
            ("26+ ANOS", "De expertise confiável em procurement internacional para hospitalidade."),
            ("1.000+ FABRICANTES", "Rede global que dá acesso aos melhores produtos e designs exclusivos."),
            ("3 CONTINENTES", "Presença consolidada em América do Sul, América do Norte e Oriente Médio."),
            ("INCORPORAÇÃO", "Hamam Incorporadora executa projetos do início ao fim, além do FF&E."),
        ]
        col_w = (W - 2*MARGIN - 3*20) / 4
        col_h = 220
        by = 120
        for i, (h, t) in enumerate(pillars):
            x = MARGIN + i*(col_w + 20)
            c.setStrokeColor(GOLD_DIM)
            c.setLineWidth(0.6)
            c.rect(x, by, col_w, col_h, fill=0, stroke=1)
            c.setFillColor(GOLD)
            c.setFont(FONT_BOLD, 10.5)
            c.drawString(x + 16, by + col_h - 28, h)
            c.setFillColor(CREME)
            wrap_text(c, t, x + 16, by + col_h - 56, col_w - 32, FONT_REG, 10, 14, CREME)
        finalize_slide(c, idx)
    slide_fns.append(s_hamam_who)

    # ========================================================
    # Hamam — Conceito de Hospitalidade
    # ========================================================
    def s_hamam_concept(c, idx):
        new_slide(c)
        header_mark(c)
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, H - 110, "CONCEITO HAMAM")
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 32)
        c.drawString(MARGIN, H - 155, "Excelência em segurança, qualidade,")
        c.drawString(MARGIN, H - 195, "prazos e custos — em escala global.")
        left_x = MARGIN
        left_w = (W - 2*MARGIN - 40) / 2
        right_x = MARGIN + left_w + 40
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(left_x, H - 245, "MISSÃO")
        c.setFillColor(CREME)
        wrap_text(c,
                  "Fornecer soluções completas e personalizadas para o setor de hospitalidade no mercado internacional, atuando em todas as etapas do processo — transformando conceitos inovadores em ambientes impactantes.",
                  left_x, H - 265, left_w, FONT_REG, 11.5, 16, CREME)
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(right_x, H - 245, "VISÃO")
        c.setFillColor(CREME)
        wrap_text(c,
                  "Liderar o mercado global com expansão internacional e melhoria contínua de processos e parcerias — sempre com foco no cliente e nas últimas tendências de design e inovação.",
                  right_x, H - 265, left_w, FONT_REG, 11.5, 16, CREME)
        # Diferenciais
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, 180, "DIFERENCIAIS COMPETITIVOS")
        diffs = [
            "Soluções econômicas altamente competitivas via vantagem cambial Brasil-América Latina.",
            "Expertise global com sourcing local e importado, otimização logística integrada.",
            "Execução de projetos do início ao fim — Hamam Incorporadora entrega chave-em-mão.",
        ]
        bullet_list(c, diffs, MARGIN, 158, W - 2*MARGIN, size=11, leading=15)
        finalize_slide(c, idx)
    slide_fns.append(s_hamam_concept)

    # ========================================================
    # Hamam no Jubiabá — Curadoria
    # ========================================================
    def s_hamam_jubiaba(c, idx):
        new_slide(c)
        header_mark(c)
        title_block(c, "Hamam no Jubiabá", "Curadoria de experiência do chão ao teto.",
                    "A Hamam Global lidera toda a curadoria de FF&E, soft goods e standards de hospitalidade das áreas comuns e das unidades hoteleiras do Jubiabá — do beach club ao spa, do lobby à suíte.")
        bullets = [
            "FF&E com standards internacionais — mobiliário, iluminação e acabamentos com fabricantes homologados globalmente.",
            "Design hospitality-grade aplicado às áreas comuns — lobby, restaurantes, spa, beach club e clubhouse.",
            "Logística internacional porta-a-porta — coordenação de containers, alfandega e montagem no canteiro.",
            "Benchmark de operadoras — alinhamento com padrões Marriott Autograph, Belmond e Rosewood.",
            "Incorporação acompanhada — controle de qualidade e entrega chave-em-mão no padrão contratado.",
        ]
        bullet_list(c, bullets, MARGIN, H - 260, W - 2*MARGIN, size=12, leading=18)
        finalize_slide(c, idx)
    slide_fns.append(s_hamam_jubiaba)

    # ========================================================
    # PRODUTO — Fachadas & Volumetria
    # ========================================================
    def s_fachadas(c, idx):
        new_slide(c)
        header_mark(c)
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, H - 110, "PRODUTO · FACHADAS")
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 32)
        c.drawString(MARGIN, H - 155, "Volumetria contemporânea e atemporal.")
        # 3 fachadas
        gap = 16
        gw = (W - 2*MARGIN - 2*gap) / 3
        gh = H - 260
        by = 80
        for i, p in enumerate(FACHADAS):
            x = MARGIN + i*(gw + gap)
            draw_cover(c, p, x, by, gw, gh)
        finalize_slide(c, idx)
    slide_fns.append(s_fachadas)

    # ========================================================
    # PRODUTO — Plantas
    # ========================================================
    def s_plantas(c, idx):
        new_slide(c)
        header_mark(c)
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, H - 110, "PRODUTO · PLANTAS")
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 32)
        c.drawString(MARGIN, H - 155, "Pavimentos — da garagem à cobertura.")
        # 6 plantas grid 3x2
        cols, rows = 3, 2
        gap = 14
        gw = (W - 2*MARGIN - (cols-1)*gap) / cols
        gh = (H - 200 - (rows-1)*gap) / rows
        by_top = H - 180
        labels = ["TÉRREO", "P1 · MEZANINO", "P2 · SETOR ÍNTIMO",
                  "COBERTURA", "SUBSOLO", "CORTE"]
        for i, p in enumerate(PLANTAS):
            col = i % cols
            row = i // cols
            x = MARGIN + col*(gw + gap)
            y = by_top - gh - row*(gh + gap)
            draw_fitted(c, p, x, y, gw, gh)
            c.setFillColor(Color(0.04, 0.035, 0.024, alpha=0.75))
            c.rect(x, y, gw, 22, fill=1, stroke=0)
            c.setFillColor(GOLD)
            c.setFont(FONT_BOLD, 8.5)
            c.drawString(x + 10, y + 7, labels[i] if i < len(labels) else "")
        finalize_slide(c, idx)
    slide_fns.append(s_plantas)

    # ========================================================
    # PRODUTO — Áreas Comuns & Gourmet
    # ========================================================
    def s_gourmet(c, idx):
        new_slide(c)
        header_mark(c)
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, H - 110, "PRODUTO · ÁREAS COMUNS")
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 32)
        c.drawString(MARGIN, H - 155, "Gourmet, estar e cozinha — hospitalidade doméstica.")
        cols, rows = 3, 2
        gap = 14
        gw = (W - 2*MARGIN - (cols-1)*gap) / cols
        gh = (H - 200 - (rows-1)*gap) / rows
        by_top = H - 180
        for i, p in enumerate(GOURMET):
            col = i % cols
            row = i // cols
            x = MARGIN + col*(gw + gap)
            y = by_top - gh - row*(gh + gap)
            draw_cover(c, p, x, y, gw, gh)
        finalize_slide(c, idx)
    slide_fns.append(s_gourmet)

    # ========================================================
    # PRODUTO — Interiores / Suítes
    # ========================================================
    def s_interiores(c, idx):
        new_slide(c)
        header_mark(c)
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, H - 110, "PRODUTO · INTERIORES")
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 32)
        c.drawString(MARGIN, H - 155, "Suítes, closet e banho — refúgio pessoal.")
        cols, rows = 3, 2
        gap = 14
        gw = (W - 2*MARGIN - (cols-1)*gap) / cols
        gh = (H - 200 - (rows-1)*gap) / rows
        by_top = H - 180
        for i, p in enumerate(INTERIORES):
            col = i % cols
            row = i // cols
            x = MARGIN + col*(gw + gap)
            y = by_top - gh - row*(gh + gap)
            draw_cover(c, p, x, y, gw, gh)
        finalize_slide(c, idx)
    slide_fns.append(s_interiores)

    # ========================================================
    # Fotos da Área — Real
    # ========================================================
    def s_area_photos(c, idx):
        new_slide(c)
        header_mark(c)
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, H - 110, "A ÁREA HOJE")
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 32)
        c.drawString(MARGIN, H - 155, "O terreno — registros de campo.")
        photos = (AREA_PHOTOS + REGIAO_PHOTOS)[:6]
        cols, rows = 3, 2
        gap = 14
        gw = (W - 2*MARGIN - (cols-1)*gap) / cols
        gh = (H - 200 - (rows-1)*gap) / rows
        by_top = H - 180
        for i, p in enumerate(photos):
            col = i % cols
            row = i // cols
            x = MARGIN + col*(gw + gap)
            y = by_top - gh - row*(gh + gap)
            draw_cover(c, p, x, y, gw, gh)
        finalize_slide(c, idx)
    slide_fns.append(s_area_photos)

    # ========================================================
    # Tese de Investimento & Flywheel
    # ========================================================
    def s_tese(c, idx):
        new_slide(c)
        header_mark(c)
        title_block(c, "Tese de investimento", "O flywheel Jubiabá.",
                    "Ativo imobiliário de alto padrão, com curadoria internacional Hamam, assinatura KV e demanda represada por segunda residência qualificada no Nordeste. Cada fase alimenta a próxima.")
        steps = [
            ("1. ASSINATURA", "KV + Hamam criam ativo instantaneamente reconhecível — precificação acima do benchmark regional."),
            ("2. ABSORÇÃO", "Fase 01 absorve demanda reprimida de SP, MG e exterior — velocidade de vendas elevada."),
            ("3. VALORIZAÇÃO", "Entrega das primeiras unidades + marina + beach club elevam o valor do m² no masterplan."),
            ("4. HOSPITALIDADE", "Operação Hamam de resort e spa gera fluxo turístico permanente — rentabilidade adicional."),
            ("5. EXPANSÃO", "Fase 02 é lançada com base valorizada e pipeline de leads já qualificado — margem maior."),
        ]
        cols = 5
        gap = 14
        cw = (W - 2*MARGIN - (cols-1)*gap) / cols
        ch = 250
        by = 130
        for i, (t, d) in enumerate(steps):
            x = MARGIN + i*(cw + gap)
            c.setStrokeColor(GOLD_DIM)
            c.setLineWidth(0.6)
            c.rect(x, by, cw, ch, fill=0, stroke=1)
            c.setFillColor(GOLD)
            c.setFont(FONT_BOLD, 11)
            c.drawString(x + 14, by + ch - 28, t)
            c.setFillColor(CREME)
            wrap_text(c, d, x + 14, by + ch - 54, cw - 28, FONT_REG, 10, 14, CREME)
        finalize_slide(c, idx)
    slide_fns.append(s_tese)

    # ========================================================
    # Projeções & VGV
    # ========================================================
    def s_vgv(c, idx):
        new_slide(c)
        header_mark(c)
        title_block(c, "Projeções", "Dimensionamento & VGV estimado.",
                    "Estimativas preliminares baseadas no masterplan da KV e em benchmarks litorâneos de alto padrão no Nordeste. Número final a ser detalhado no deal memo.")
        stats = [
            ("+1,2M m²", "ÁREA TOTAL DO MASTERPLAN"),
            ("Fase 01 + 02", "ENTREGAS ESCALONADAS EM 7–10 ANOS"),
            ("VGV alvo", "DETALHADO POR FASE NO DEAL MEMO"),
            ("Hospitalidade", "RECEITA RECORRENTE VIA RESORT & SPA"),
        ]
        box_w = (W - 2*MARGIN - 3*20) / 4
        box_h = 110
        by = 170
        for i, (num, lab) in enumerate(stats):
            x = MARGIN + i*(box_w + 20)
            stat_box(c, x, by, box_w, box_h, num, lab)
        # Disclaimer
        c.setFillColor(MUTED)
        c.setFont(FONT_REG, 8.5)
        wrap_text(c,
                  "Os números apresentados são estimativas preliminares, não constituem oferta pública e estão sujeitos a revisão após due diligence, aprovação de órgãos competentes e detalhamento de projeto executivo. A Empresa Independente disponibilizará modelo financeiro detalhado sob NDA.",
                  MARGIN, 120, W - 2*MARGIN, FONT_REG, 8.5, 12, MUTED)
        finalize_slide(c, idx)
    slide_fns.append(s_vgv)

    # ========================================================
    # Próximos Passos & CTA
    # ========================================================
    def s_cta(c, idx):
        new_slide(c)
        # Hero image atrás
        hero = FACHADAS[1] if os.path.exists(FACHADAS[1]) else page_path(1)
        c.drawImage(safe_img(hero), 0, 0, W, H, preserveAspectRatio=False, mask='auto')
        c.setFillColor(Color(0.04, 0.035, 0.024, alpha=0.75))
        c.rect(0, 0, W, H, fill=1, stroke=0)
        header_mark(c)
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, H - 140, "PRÓXIMOS PASSOS")
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 48)
        c.drawString(MARGIN, H - 205, "Vamos conversar.")
        c.setFillColor(CREME)
        c.setFont(FONT_REG, 14)
        wrap_text(c,
                  "Agende uma conversa confidencial com o time da Empresa Independente. Apresentamos o deal memo completo, modelo financeiro detalhado e cronograma de captação sob NDA.",
                  MARGIN, H - 245, W - 2*MARGIN - 40, FONT_REG, 14, 20, CREME)
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(MARGIN, 200, "CONTATO")
        c.setFillColor(WHITE)
        c.setFont(FONT_BOLD, 16)
        c.drawString(MARGIN, 172, "Empresa Independente")
        c.setFillColor(CREME)
        c.setFont(FONT_REG, 12)
        c.drawString(MARGIN, 150, "adm@empresaind.com")
        c.drawString(MARGIN, 132, "empresaind.com")
        # Right-side agenda
        rx = W / 2 + 60
        c.setFillColor(GOLD)
        c.setFont(FONT_BOLD, 11)
        c.drawString(rx, 200, "AGENDA SUGERIDA")
        steps = [
            "1. Assinatura de NDA",
            "2. Sessão de apresentação do deal memo",
            "3. Acesso ao modelo financeiro detalhado",
            "4. Visita técnica a Estância · Sergipe",
            "5. Term sheet e estruturação do veículo",
        ]
        cy = 172
        for s in steps:
            c.setFillColor(CREME)
            c.setFont(FONT_REG, 11.5)
            c.drawString(rx, cy, s)
            cy -= 16
        finalize_slide(c, idx)
    slide_fns.append(s_cta)

    # ========================================================
    # Render everything
    # ========================================================
    global SLIDES_TOTAL
    SLIDES_TOTAL = len(slide_fns)
    print(f"[build] total slides: {SLIDES_TOTAL}")
    for i, fn in enumerate(slide_fns, start=1):
        print(f"[build] slide {i:02d}/{SLIDES_TOTAL:02d} — {fn.__name__}")
        fn(c, i)
    c.save()
    print(f"[build] PDF written: {OUT_PDF}")
    print(f"[build] size: {os.path.getsize(OUT_PDF)/1024/1024:.2f} MB")

if __name__ == "__main__":
    build()
