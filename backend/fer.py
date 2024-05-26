import cv2
from PIL import Image
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import tempfile
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Set TensorFlow logging level to only display errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 0 = all messages, 1 = info, 2 = warnings, 3 = errors

model = tf.keras.models.load_model(r'deep_learning_models/weights/fer.keras')


def detectFaces(img):
    """
    Detects faces in the provided image.

    This function takes an image file and detects faces using
    the Haar cascade classifier. It extracts the detected face
    regions without any resizing or color conversion.

    Parameters:
    - image: Image file containing faces.

    Returns:
    - face_regions (list): List of face images.
    """
    # Load the face cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(48, 48))

    # Initialize a list to store face images
    face_regions = []

    # Extract the face regions from the original image
    for (x, y, w, h) in faces:
        face_region = img[y:y + h, x:x + w]
        face_regions.append(face_region)

    return face_regions

def preprocess_images(images, target_size=(48, 48)):
    processed_images = []
    for image in images:
        # Convert to grayscale
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Resize the image
        resized_image = cv2.resize(grayscale_image, target_size)

        # Normalize the image
        normalized_image = resized_image / 255.0

        # Convert image to a tensor and expand dimensions to match the input shape of the model
        expanded_image = tf.expand_dims(tf.convert_to_tensor(normalized_image, dtype=tf.float32), axis=-1)

        processed_images.append(expanded_image)

    return tf.stack(processed_images)


def emotionRecognition(faces):
    # Define your label mapping based on your dataset
    label_mapping = {0: 'angry', 1: 'fear', 2: 'happy', 3: 'neutral', 4: 'sad', 5: 'surprise'}

    # Preprocess the faces
    preprocessed_faces = preprocess_images(faces)

    # Make predictions for each face
    predictions = model.predict(preprocessed_faces)

    # Convert predictions to emotion labels using the label mapping
    predicted_emotions = [label_mapping[idx] for idx in np.argmax(predictions, axis=1)]

    return predicted_emotions


if __name__ == "__main__":
    # Path to the image file containing faces
    image_path = r"C:\Users\Joshua\Downloads\ezgif.com-gif-maker-3.jpg"  # Update this with your image path

    # Read the image file
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Image at path {image_path} could not be read.")

    # Detect faces in the image
    face_regions = detectFaces(image)

    if not face_regions:
        print("No faces detected in the image.")
    else:
        # Perform emotion recognition on detected faces
        emotions = emotionRecognition(face_regions)

        # Print the detected emotions
        print("Detected Emotions:", emotions)