import subprocess

def ejecutar_script(script):
    print(f"🚀 Ejecutando {script}...")
    resultado = subprocess.run(["python", script], capture_output=True, text=True)
    print(resultado.stdout)  # Mostrar salida estándar
    if resultado.stderr:  # Mostrar errores si los hay
        print(f"❌ Error en {script}: {resultado.stderr}")
    return resultado.returncode == 0  # Retorna True si no hubo errores

if __name__ == "__main__":
    if ejecutar_script("generar_json.py"):
        if ejecutar_script("app.py"):  # Ahora app.py se cierra solo
            ejecutar_script("unirPDF.py")