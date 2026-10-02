# app.py
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import io
import base64
import uuid
from Muzz_Factory_UMB import UMB_Generator

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8MB

ALLOWED_EXTENSIONS = {'png'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generar', methods=['POST'])
def generar():
    """Genera plantillas y devuelve PDF + previews + nombre_base en una sola respuesta."""
    temp_path = None
    try:
        if 'skin' not in request.files:
            return jsonify({'error': 'No se envió ninguna skin'}), 400

        file = request.files['skin']
        if file.filename == '':
            return jsonify({'error': 'Nombre de archivo vacío'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Solo se permiten archivos PNG'}), 400

        modo_slim = request.form.get('modo_slim', 'false').lower() == 'true'
        modo_borde = request.form.get('modo_borde', 'false').lower() == 'true'
        modo_croma = request.form.get('modo_croma', 'false').lower() == 'true'
        fondo_p5 = request.form.get('fondo_p5', 'DESACTIVADO')

        borde_1 = request.form.get('borde_1', 'false').lower() == 'true'
        borde_2 = request.form.get('borde_2', 'false').lower() == 'true'
        borde_3 = request.form.get('borde_3', 'false').lower() == 'true'

        croma_1 = request.form.get('croma_1', 'OFF')
        croma_2 = request.form.get('croma_2', 'OFF')
        croma_3 = request.form.get('croma_3', 'OFF')
        croma_5 = request.form.get('croma_5', 'OFF')

        cape_1 = request.form.get('cape_1', 'false').lower() == 'true'
        cape_2 = request.form.get('cape_2', 'false').lower() == 'true'
        cape_3 = request.form.get('cape_3', 'false').lower() == 'true'
        cape_4 = request.form.get('cape_4', 'false').lower() == 'true'
        cape_5 = request.form.get('cape_5', 'false').lower() == 'true'

        # Nombre original del usuario (para nombrar el PDF final)
        original_name = secure_filename(file.filename)
        if original_name.lower().endswith('.png'):
            nombre_base = original_name[:-4]
        else:
            nombre_base = original_name
        if not nombre_base:
            nombre_base = "skin"

        # Nombre único en disco para evitar colisiones entre usuarios
        temp_filename = f"{uuid.uuid4().hex}.png"
        temp_path = os.path.join('/tmp', temp_filename)
        file.save(temp_path)

        gen = UMB_Generator()
        gen.importar_skin(temp_path)
        gen.modo_slim = modo_slim
        gen.modo_borde = modo_borde
        gen.bordes_activos = {1: borde_1, 2: borde_2, 3: borde_3}
        gen.modo_croma = modo_croma
        gen.cromas_colores = {1: croma_1, 2: croma_2, 3: croma_3, 5: croma_5}
        gen.modo_fondo_p5 = fondo_p5
        gen.capas_cape_activas = {1: cape_1, 2: cape_2, 3: cape_3, 4: cape_4, 5: cape_5}

        gen.generar_todas()

        pdf_buffer = io.BytesIO()
        gen.exportar_pdf_memoria(pdf_buffer)
        pdf_buffer.seek(0)
        pdf_b64 = base64.b64encode(pdf_buffer.getvalue()).decode()

        previews = {}
        for num in range(1, 6):
            if gen.plantillas.get(num):
                img = gen.plantillas[num].copy()
                img.thumbnail((400, 400))
                img_buffer = io.BytesIO()
                img.save(img_buffer, format='PNG')
                previews[str(num)] = 'data:image/png;base64,' + base64.b64encode(img_buffer.getvalue()).decode()

        try:
            os.remove(temp_path)
        except OSError:
            pass
        temp_path = None

        return jsonify({
            'pdf': 'data:application/pdf;base64,' + pdf_b64,
            'previews': previews,
            'nombre_base': nombre_base
        })

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500
    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass


@app.route('/ads.txt')
def ads_txt():
    return send_from_directory('static', 'ads.txt', mimetype='text/plain')


@app.route('/health')
def health():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
