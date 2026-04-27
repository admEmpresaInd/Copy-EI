import fitz, os

pdf_path = r"D:\Copy EI\Fotos Zanuto\Masterplan - KV.pdf"
out_dir = r"D:\Copy EI\Jubiabá\selected_pages"
os.makedirs(out_dir, exist_ok=True)

# Páginas selecionadas (1-based)
selected = [1, 2, 3, 5, 8, 9, 10, 12, 14, 16, 17, 20, 22, 24, 27, 28, 29, 31, 33, 34]
selected_0 = [n - 1 for n in selected]

doc = fitz.open(pdf_path)
mat = fitz.Matrix(3.0, 3.0)

for page_num in selected_0:
    if page_num < len(doc):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=mat)
        fname = f"slide_{page_num+1:02d}.png"
        pix.save(os.path.join(out_dir, fname))
        print(f"Extraido: pag {page_num+1} -> {fname}")

doc.close()
print(f"Total: {len(selected_0)} paginas extraidas")
