import pytesseract
from flask import Flask, request, jsonify
from PIL import Image
from pdf2image import convert_from_bytes
import logging
import os

# Configuración básica de logging para ver información en los logs de Render.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# La siguiente línea es SOLO para pruebas locales en Windows.
# Debe estar comentada para que funcione en Render (Linux).
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

@app.route('/ocr', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logging.warning("Petición recibida sin la parte del archivo.")
        return jsonify({"error": "No se encontró el archivo en la petición"}), 400
    
    file = request.files['file']

    if file.filename == '':
        logging.warning("Petición recibida con un nombre de archivo vacío.")
        return jsonify({"error": "Ningún archivo seleccionado"}), 400

    if file:
        try:
            filename = file.filename
            # Revisa si el archivo es un PDF por su extensión
            if filename.lower().endswith('.pdf'):
                logging.info(f"Procesando archivo PDF: {filename}")
                pdf_bytes = file.read()
                
                # Usa pdf2image para convertir los bytes en una lista de imágenes (una por página)
                images = convert_from_bytes(pdf_bytes)
                
                texto_completo = ""
                # Itera sobre cada imagen/página para extraer el texto
                for i, page_image in enumerate(images):
                    texto_pagina = pytesseract.image_to_string(page_image, lang='eng+spa')
                    texto_completo += f"--- Página {i+1} ---\n{texto_pagina}\n\n"
                
                logging.info(f"OCR exitoso para el PDF: {filename}")
                return jsonify({"text": texto_completo})

            else: # Si no es PDF, lo procesa como una imagen
                logging.info(f"Procesando archivo de imagen: {filename}")
                img = Image.open(file.stream)
                text = pytesseract.image_to_string(img, lang='eng+spa')
                
                logging.info(f"OCR exitoso para la imagen: {filename}")
                return jsonify({"text": text})

        except Exception as e:
            # Devuelve un error detallado si algo falla
            logging.error(f"Error procesando el archivo {file.filename}: {e}", exc_info=True)
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)