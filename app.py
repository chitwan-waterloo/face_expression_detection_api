from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import base64
from keras.models import model_from_json
# from keras_preprocessing.image import load_img
from flask_cors import CORS

json_file = open("emotiondetector.json", 'r')
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("emotiondetector.h5")

# hear_file = cv2.data.haarcascades + 'haarcascades_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Check if the cascade file was loaded correctly
if face_cascade.empty():
    raise IOError('Cannot load the specified xml file.')

def extract_feature_single(image):
    feature = np.array(image)
    feature = feature.reshape(1,48,48,1)
    return feature / 255.0

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('home.html')

labels = {0 : 'angry', 
          1 : 'disgust', 
          2 : 'fear', 
          3 : 'happy', 
          4 : 'neutral', 
          5 : 'sad', 
          6 : 'surprise'}

@app.route('/predictemotion', methods=['POST'])
def predict_emotion():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'No data found'}) , 400
    string_image = data['image']
    string_image = string_image.split(',')
    
    if len(string_image) ==2:
        string_image = string_image[1]
        print(string_image)
    else:
        string_image = string_image[0]
        print(string_image)
    
    string_image = base64.b64decode(string_image)
    nparr_image = np.frombuffer(string_image, np.uint8)

    img = cv2.imdecode(nparr_image, cv2.IMREAD_GRAYSCALE)
    faces = face_cascade.detectMultiScale(img,1.1,5)

    for (x,y,w,h) in faces:
        image = img[y:y+h,x:x+w]
        image = cv2.resize(image, (48,48))
        im = extract_feature_single(image)
        pred = model.predict(im)
        prediction_label = labels[pred.argmax()]

        return jsonify({"emotion": prediction_label,"x1":str(x),"y1":str(y),"x2":str(x+w),"y2":str(y+h)}) , 200
    
    return jsonify({"emotion": "face not detected","x1":str(0),"y1":str(0),"x2":str(0),"y2":str(0)}), 200

@app.route('/predictemotion', methods=['GET'])
def emotion_page():
    return render_template('predictemotion.html')

if __name__ == "__main__":
    app.run()
