import os
import cv2
import numpy as np
from datetime import datetime
from flask import Flask, render_template, request, send_file

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def apply_filter(img, filter_type):
    if filter_type == 'grayscale':
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif filter_type == 'sepia':
        sepia = np.array([[0.272, 0.534, 0.131],
                          [0.349, 0.686, 0.168],
                          [0.393, 0.769, 0.189]])
        return cv2.transform(img, sepia)
    elif filter_type == 'blur':
        return cv2.GaussianBlur(img, (15, 15), 0)
    else:
        return img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No image uploaded", 400

    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400

    filter_type = request.form.get('filter', 'none')
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    img = cv2.imread(filepath)
    filtered = apply_filter(img, filter_type)

    out_path = os.path.join(UPLOAD_FOLDER, "filtered_" + filename)
    cv2.imwrite(out_path, filtered)

    return send_file(out_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
