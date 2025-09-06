import pytesseract
from flask import Flask, request, jsonify
from PIL import Image
import logging

# Si estás en Windows y la prueba local falla, puede que necesites esta línea:
# Ya luego no se usa porque es para local nada mas // pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}
app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No se encontró el archivo en la petición"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Ningún archivo seleccionado"}), 400

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if file and allowed_file(file.filename):
        try:
            img = Image.open(file.stream)
            text = pytesseract.image_to_string(img, lang='eng+spa')
            logging.info(f"OCR exitoso para el archivo: {file.filename}")
            return jsonify({"text": text})
        except Exception as e:
            logging.error(f"Error procesando el archivo {file.filename}: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)