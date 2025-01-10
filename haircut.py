from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import base64
from model import opencv, rf, facedata as fd
from io import BytesIO
from PIL import Image


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/haircut', methods=['POST'])
def process_image():
    try:
        os.remove("/results/image.png")
        os.remove("uploads/image.png")
    except:
        pass
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400

    image_data = data['image']
    
    if image_data.startswith('data:image'):
        header, encoded = image_data.split(',', 1)
    else:
        encoded = image_data

    try:
        image_binary = base64.b64decode(encoded)
    except Exception as e:
        return jsonify({'error': 'Invalid base64 encoding', 'message': str(e)}), 400
    
    file_name = 'image.png'
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    with open(file_path, 'wb') as file:
        file.write(image_binary)

    result_path, haircut_data = process(file_name)

    image_url = f"/results/{file_name}"

    return jsonify({
        "image_url": image_url,
        "head_shape": haircut_data
    })

@app.route('/results/<filename>')
def serve_result_image(filename):
    return send_from_directory(RESULT_FOLDER, filename)

def process(file_name: str):
    ratio = opencv.face_shape(os.path.join(UPLOAD_FOLDER, file_name),
                              show=False,
                              output_path=os.path.join(RESULT_FOLDER, file_name))
    predict = rf.predict(ratio)
    face_data = fd.faceData(predict, True)
    ret = face_data.getHeadShape()
    
    return (os.path.join(RESULT_FOLDER, file_name), ret)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
