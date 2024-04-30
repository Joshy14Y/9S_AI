import cv2
from PIL import Image
import numpy as np
from transformers import AutoImageProcessor, AutoModelForImageClassification
import matplotlib.pyplot as plt
import tempfile

def detectFaces(image):
    """
    Detects faces in the provided image.

    This function takes an image file and detects faces using
    the Haar cascade classifier. It then resizes each detected
    face to a common size and converts them to RGB format.

    Parameters:
    - image: Image file containing faces.

    Returns:
    - resized_faces_rgb (list): List of resized face images in RGB format.
    """

    # Load the face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert the image to OpenCV format
    img = cv2.imdecode(np.frombuffer(image.read(), np.uint8), -1)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))

    # Initialize a list to store resized face images as RGB images
    resized_faces_rgb = []

    # Resize the faces to a common size and convert each to RGB format
    for (x, y, w, h) in faces:
        # Extract the face region from the original image
        face_roi = img[y:y + h, x:x + w]

        # Resize the face region to 40x40 directly
        resized_face_bgr = cv2.resize(face_roi, (40, 40))

        # Convert the BGR image to RGB format
        resized_face_rgb = cv2.cvtColor(resized_face_bgr, cv2.COLOR_BGR2RGB)

        # Append the resized face image to the list
        resized_faces_rgb.append(resized_face_rgb)

    return resized_faces_rgb

def emotionRecognition(faces):
    """
    Recognizes emotions in the detected faces.

    This function takes a list of detected faces, applies an
    image classification model to recognize emotions, and
    returns the predicted emotions for each face.

    Parameters:
    - faces (list): List of resized face images in RGB format.

    Returns:
    - results (list): List of predicted emotions for each face.
    """
    # Initialize the processor
    processor = AutoImageProcessor.from_pretrained("dima806/facial_emotions_image_detection")
    model = AutoModelForImageClassification.from_pretrained("dima806/facial_emotions_image_detection")

    # Initialize list to store results for each face
    results = []

    # Apply the model to each detected face
    inputs = processor(images=faces, return_tensors="pt")

    # Perform inference
    outputs = model(**inputs)
    logits = outputs.logits

    # Get the predicted emotion labels for all faces
    predicted_class_idxs = logits.argmax(dim=1).tolist()

    # Map class indices to emotion labels
    id2label = {
        "0": "sad",
        "1": "disgust",
        "2": "angry",
        "3": "neutral",
        "4": "fear",
        "5": "surprise",
        "6": "happy"
    }

    # Convert predicted class indices to emotion labels
    predicted_emotions = [id2label[str(idx)] for idx in predicted_class_idxs]

    results.extend(predicted_emotions)
    return results