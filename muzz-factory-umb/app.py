# app.py
from flask import Flask, request, render_template, send_file
from Muzz_Factory_UMB import UMB_Generator
import io
import os
import time

app = Flask(__name__)

# Configuración
CARPETA_TEMP = "temp"
os.makedirs(CARPETA_TEMP, exist_ok=True)

@app.route('/')
def index():
    """Página principal con el formulario."""
    return render_template('index.html')

@app.route('/generar', methods=['POST'])
def generar():
    """Recibe la skin, la procesa y devuelve el PDF."""
    skin_file = request.files.get('skin')
    if not skin_file:
        return "No se subió ningún archivo", 400
    
    # Guardar skin temporalmente
    timestamp = str(int(time.time()))
    skin_path = os.path.join(CARPETA_TEMP, f"skin_{timestamp}.png")
    skin_file.save(skin_path)
    
    try:
        # Usar tu clase UMB_Generator
        generador = UMB_Generator()
        generador.importar_skin(skin_path)
        generador.generar_todas()
        
        # Exportar a PDF en memoria
        pdf_buffer = io.BytesIO()
        generador.exportar_pdf_memoria(pdf_buffer)
        pdf_buffer.seek(0)
        
        # Nombre del archivo
        nombre_base = os.path.basename(skin_path).replace('.png', '')
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f'plantilla_muzz_factory.pdf',
            mimetype='application/pdf'
        )
    
    except Exception as e:
        return f"Error al generar: {str(e)}", 500
    
    finally:
        # Limpiar skin temporal
        if os.path.exists(skin_path):
            os.remove(skin_path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)