from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
import base64
from keras.models import model_from_json
from flask_cors import CORS

# Load the pre-trained model
json_file = open("emotiondetector.json", 'r')
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("emotiondetector.h5")

# Load the face detection model
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Check if the cascade file was loaded correctly
if face_cascade.empty():
    raise IOError('Cannot load the specified xml file.')

def extract_feature_single(image):
    """
    Preprocess the image to extract features for emotion prediction.

    Args:
        image (numpy array): The grayscale image of the detected face.

    Returns:
        numpy array: The preprocessed image ready for prediction.
    """
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0

# Initialize the Flask app
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    """
    Render the home page with a button to navigate to the emotion detection page.

    Returns:
        html: The home page HTML content.
    """
    return render_template('home.html')

# Define the emotion labels
labels = {0: 'angry', 
          1: 'disgust', 
          2: 'fear', 
          3: 'happy', 
          4: 'neutral', 
          5: 'sad', 
          6: 'surprise'}

@app.route('/predictemotion', methods=['POST'])
def predict_emotion():
    """
    Predict the emotion from the given image.

    Expects a JSON payload with a base64-encoded image.

    Returns:
        json: The predicted emotion and coordinates of the detected face.
    """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'No data found'}), 400
    
    # Extract the base64 string from the data
    string_image = data['image'].split(',')
    
    if len(string_image) == 2:
        string_image = string_image[1]
    else:
        string_image = string_image[0]
    
    string_image = base64.b64decode(string_image)
    nparr_image = np.frombuffer(string_image, np.uint8)

    # Decode the image from the numpy array
    img = cv2.imdecode(nparr_image, cv2.IMREAD_GRAYSCALE)
    faces = face_cascade.detectMultiScale(img, 1.1, 5)

    for (x, y, w, h) in faces:
        # Preprocess the detected face image
        image = img[y:y+h, x:x+w]
        image = cv2.resize(image, (48, 48))
        im = extract_feature_single(image)

        # Predict the emotion
        pred = model.predict(im)
        prediction_label = labels[pred.argmax()]

        return jsonify({"emotion": prediction_label, "x1": str(x), "y1": str(y), "x2": str(x+w), "y2": str(y+h)}), 200
    
    return jsonify({"emotion": "face not detected", "x1": str(0), "y1": str(0), "x2": str(0), "y2": str(0)}), 200

@app.route('/predictemotion', methods=['GET'])
def emotion_page():
    """
    Render the emotion detection page with the webcam feed.

    Returns:
        html: The emotion detection page HTML content.
    """
    return render_template('predictemotion.html')

if __name__ == "__main__":
    app.run()
