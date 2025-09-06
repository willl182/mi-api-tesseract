import pytesseract
from flask import Flask, request, jsonify
from PIL import Image

# Si estás en Windows y la prueba local falla, puede que necesites esta línea:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No se encontró el archivo en la petición"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Ningún archivo seleccionado"}), 400

    if file:
        try:
            img = Image.open(file.stream)
            text = pytesseract.image_to_string(img, lang='eng+spa')
            return jsonify({"text": text})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)