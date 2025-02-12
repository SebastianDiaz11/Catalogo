from flask import Flask, render_template, make_response, jsonify, url_for
from weasyprint import HTML
from datetime import datetime, timedelta
import json
app = Flask(__name__)
import os

directorio = os.path.dirname(os.path.abspath(__file__))
ruta_json = os.path.join(directorio, "json_categorias")
archivos_json = [f for f in os.listdir(ruta_json) if f.endswith('.json')]

products = []
def get_fecha():
    fecha_actual = datetime.now()
    fecha_incrementada = fecha_actual + timedelta(days=1)
    fecha_formateada = fecha_incrementada.strftime("%d/%m/%Y")
    return fecha_formateada

with app.app_context():
    for archivo in archivos_json:
            ruta = os.path.join(ruta_json, archivo)
            try:
                with open(ruta, 'r', encoding="ISO-8859-1") as f:
                    contenido = json.load(f)
                    if isinstance(contenido, list): 
                        products=contenido  
                    else:
                        products=[contenido]
                
                nombre_pdf=f'pdfs/{os.path.splitext(archivo)[0]}.pdf'
                fecha=get_fecha()
                
                html_content = render_template('template.html',products=products,fecha=fecha)
                pdf = HTML(string=html_content).write_pdf(nombre_pdf) 
                print(f"PDF generado: {nombre_pdf}")

            except Exception as e:
                print(f"Error al leer {archivo}: {e}")


@app.route('/products')
def index():
    return "PDFs generados con exito"
    #return render_template('template.html',products=products,fecha=fecha)

if __name__ == "__main__":
    app.run(debug=True)