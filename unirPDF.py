import os
from PyPDF2 import PdfMerger

# Ruta de la carpeta que contiene los archivos PDF
carpeta_pdf = r"C:/Users/Sebastián Díaz/Desktop/catalogoexcel/pdfs"

# Crear una instancia de PdfMerger
merger = PdfMerger()

# Listar todos los archivos PDF en la carpeta
for archivo in os.listdir(carpeta_pdf):
    if archivo.endswith('.pdf'):
        # Unir los archivos PDF
        merger.append(os.path.join(carpeta_pdf, archivo))

# Guardar el PDF resultante
merger.write(os.path.join(carpeta_pdf, 'Catalogomayorista.pdf'))
merger.close()

print("Archivos PDF unidos exitosamente.")
