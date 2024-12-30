from flask import Flask, request, jsonify
import os
import cv2
import base64
from model import opencv, rf, facedata as fd

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/haircut', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    result_path, haircut_data = process(file.filename)

    # Convert the image to base64
    with open(result_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Return JSON response with both image and haircut data
    return jsonify({
        "image": encoded_image,
        "haircut_data": haircut_data.arr()
    })

def process(file_name: str):
    ratio = opencv.face_shape(os.path.join(UPLOAD_FOLDER, file_name),
                              show=False,
                              output_path=os.path.join(RESULT_FOLDER, file_name))
    predict = rf.predict(ratio)
    face_data = fd.faceData(predict, True)
    haircut_data = fd.haircutData(face_data.arr(), True)
    return (os.path.join(RESULT_FOLDER, file_name), haircut_data)

if __name__ == '__main__':
    app.run(debug=True)
