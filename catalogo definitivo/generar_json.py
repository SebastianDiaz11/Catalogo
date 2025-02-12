import pandas as pd
import json
import os
import base64
import unicodedata

# Cargar el archivo Excel
archivo_excel = "datos.xlsx"  # Reemplázalo con tu archivo
df = pd.read_excel(archivo_excel, dtype=str)  # Cargar como string para evitar problemas

# Carpetas
carpeta_salida = "json_categorias"
carpeta_imagenes = "static/images"  # Carpeta donde están las imágenes
ruta_txt = "faltantes.txt"

# Crear la carpeta de salida si no existe
os.makedirs(carpeta_salida, exist_ok=True)

# Función para convertir imagen a Base64
def imagen_a_base64(ruta_imagen):
    with open(ruta_imagen, "rb") as img_file:
        return "data:image/png;base64," + base64.b64encode(img_file.read()).decode("utf-8")

def eliminar_tildes(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    ).upper()

# Agrupar por rubrodesc y lineadesc
grupos = df.groupby(["rubrodesc", "lineadesc"])

prods_poco_stock = {}  # Usamos un diccionario para evitar duplicados por SKU

# Procesar cada categoría y subcategoría
for (rubro, linea), grupo in grupos:
    productos = []

    for _, row in grupo.iterrows():
        codigo = row["codigo"]
        nombre = row["descripcion"]
        nombre_imagen = f"{codigo}.png"
        ruta_imagen = os.path.join(carpeta_imagenes, nombre_imagen)
        stock = int(row["stock"])

        if not os.path.exists(ruta_imagen):
            if stock > 0:
                with open(ruta_txt, "a") as txt:
                    txt.write(f"{codigo} - {nombre}\n")
            continue

        if stock == 0:
            continue

        imagen_base64 = imagen_a_base64(ruta_imagen)

        if stock > 3:
            productos.append({
                "sku": codigo,
                "nombre": nombre,
                "precio": "{:,.0f}".format(float(row["precio_neto"].replace(",", "."))).replace(",", "."),
                "stock": stock,
                "imagen": imagen_base64
            })

        if 1 <= stock <= 3 and codigo not in prods_poco_stock:
            prods_poco_stock[codigo] = {
                "sku": codigo,
                "nombre": nombre,
                "precio": "{:,.0f}".format(float(row["precio_neto"].replace(",", "."))).replace(",", "."),
                "stock": stock,
                "imagen": imagen_base64
            }

    if productos:
        productos.sort(key=lambda x: x['stock'], reverse=True)
        data = {
            "categ_sec": eliminar_tildes(rubro),
            "categ_prin": eliminar_tildes(linea),
            "products": productos
        }
        nombre_archivo = f"{rubro}_{linea}.json".replace(" ", "_").replace("/", "-")
        ruta_archivo = os.path.join(carpeta_salida, nombre_archivo)
        
        with open(ruta_archivo, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        print(f"Archivo generado: {ruta_archivo}")

# Guardar últimas unidades sin duplicados
prods_poco_stock_list = list(prods_poco_stock.values())  
prods_poco_stock_list.sort(key=lambda x: x['stock'], reverse=True)

data = {
    "categ_sec": "",
    "categ_prin": "ULTIMAS UNIDADES",
    "products": prods_poco_stock_list
}

nombre_archivo = "ult_unidades.json"
ruta_archivo = os.path.join(carpeta_salida, nombre_archivo)

with open(ruta_archivo, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)

print(f"Archivo generado: {ruta_archivo}")

print("Todos los JSON han sido generados correctamente.")
