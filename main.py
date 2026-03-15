import fitz
from ocr import ocr_with_ollama
from segment_text import segment_glm_ocr_text


doc = fitz.open('723b7c45ee9db98185e8f8fdc9b991f71713546065.pdf')

for page_num in range(len(doc)):
    page = doc[page_num]
    matrice = fitz.Matrix(2, 2)  # Zoom 2x
    pix = page.get_pixmap(matrix=matrice)
    pix.save(f'page_{page_num+1}.png')


image_file = "page_19.png"
result = ocr_with_ollama(image_file)
print(result)
print("\n--- SEGMENTED TEXT ---")
segments = segment_glm_ocr_text(result)
for seg in segments:
    print(f"[{seg['entity_group'].upper()}] {seg['word']}\n")