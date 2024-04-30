from flask import Flask, request, jsonify
from flask_cors import CORS
from models import ModelLoader
import os
import tempfile
import requests
import audio_transcription as at
import fer
import cv2

app = Flask(__name__)
CORS(app)
model_loader = ModelLoader()


@app.route('/s&p_prediction', methods=['GET'])
def s_and_p_prediction():
    """
        Predicts the value of S&P index for a given date.

        This function retrieves the input date from the request arguments
        and passes it to the `model_loader.process_SARIMAX` function along
        with the model name ('s&p'). The prediction result is then returned
        as a JSON object.

        Returns:
        - prediction (float): Predicted value of S&P index.
        """
    model = 's&p'
    input_date = request.args.get('input_date')
    prediction = model_loader.process_SARIMAX(model, input_date)
    return jsonify(prediction=prediction)


@app.route('/ethereum_prediction', methods=['GET'])
def ethereum_prediction():
    """
       Predicts the value of Ethereum cryptocurrency for a given date.

       This function retrieves the input date from the request arguments
       and passes it to the `model_loader.process_SARIMAX` function along
       with the model name ('ethereum'). The prediction result is then returned
       as a JSON object.

       Returns:
       - prediction (float): Predicted value of Ethereum cryptocurrency.
       """
    model = 'ethereum'
    input_date = request.args.get('input_date')
    prediction = model_loader.process_SARIMAX(model, input_date)
    return jsonify(prediction=prediction)


@app.route('/bitcoin_prediction', methods=['GET'])
def bitcoin_prediction():
    """
       Predicts the value of Bitcoin cryptocurrency for a given date.

       This function retrieves the input date from the request arguments
       and passes it to the `model_loader.process_SARIMAX` function along
       with the model name ('bitcoin'). The prediction result is then returned
       as a JSON object.

       Returns:
       - prediction (float): Predicted value of Bitcoin cryptocurrency.
       """
    model = 'bitcoin'
    input_date = request.args.get('input_date')
    prediction = model_loader.process_SARIMAX(model, input_date)
    return jsonify(prediction=prediction)


@app.route('/avocado_prediction', methods=['GET'])
def avocado_prediction():
    """
        Predicts the price of avocados for a given date.

        This function retrieves the input date from the request arguments
        and passes it to the `model_loader.process_SARIMAX` function along
        with the model name ('avocado'). The prediction result is then returned
        as a JSON object.

        Returns:
        - prediction (float): Predicted price of avocados.
        """
    model = 'avocado'
    input_date = request.args.get('input_date')
    prediction = model_loader.process_SARIMAX(model, input_date)
    return jsonify(prediction=prediction)


@app.route('/wine_prediction', methods=['GET'])
def wine_prediction():
    """
      Predicts the quality of wine based on its attributes.

      This function retrieves the volatile acidity, density, and alcohol
      content from the request arguments and passes them to the
      `model_loader.wine_prediction` function. The prediction result
      is then returned as a JSON object.

      Returns:
      - prediction (str): Predicted quality of wine (e.g., 'Good', 'Bad').
      """
    volatile_acidity = float(request.args.get('volatile_acidity'))
    density = float(request.args.get('density'))
    alcohol = float(request.args.get('alcohol'))
    prediction = model_loader.wine_prediction(volatile_acidity, density, alcohol)
    return jsonify(prediction=prediction)


@app.route('/stroke_prediction', methods=['GET'])
def stroke_prediction():
    """
    Predicts the likelihood of stroke based on health parameters.

    This function retrieves age, hypertension, heart disease, and average
    glucose level from the request arguments and passes them to the
    `model_loader.stroke_prediction` function. The prediction result
    is a boolean value indicating whether the likelihood of stroke is high
    (True) or low (False).

    Returns:
    - prediction (bool): True if the likelihood of stroke is high,
                         False otherwise.
    """
    age = int(request.args.get('age'))
    print(age)
    hypertension = int(request.args.get('hypertension'))
    heart_disease = int(request.args.get('heart_disease'))
    avg_glucose_level = float(request.args.get('avg_glucose_level'))
    prediction = model_loader.stroke_prediction(age, hypertension, heart_disease, avg_glucose_level)
    return jsonify(prediction=prediction)


@app.route('/pokemon_prediction', methods=['GET'])
def pokemon_prediction():
    """
      Predicts whether a Pokémon is legendary based on its attributes.

      This function retrieves the base egg steps and male percentage
      from the request arguments and passes them to the
      `model_loader.pokemon_prediction` function. The prediction
      result is then returned as a JSON object indicating whether
      the Pokémon is legendary or not.

      Returns:
      - prediction (bool): True if the Pokémon is predicted to be legendary,
                           False otherwise.
      """
    base_egg_steps = int(request.args.get('base_egg_steps'))
    percentage_male = float(request.args.get('percentage_male'))
    prediction = model_loader.pokemon_prediction(base_egg_steps, percentage_male)
    return jsonify(prediction=prediction)


@app.route('/heart_failure_prediction', methods=['GET'])
def heart_failure_prediction():
    """
    Predicts the likelihood of heart failure based on health parameters.

    This function retrieves ejection fraction and time from the request
    arguments and passes them to the `model_loader.heart_failure_prediction`
    function. The prediction result is a boolean value indicating whether
    the likelihood of heart failure is high (True) or low (False).

    Returns:
    - prediction (bool): True if the likelihood of heart failure is high,
                         False otherwise.
    """
    ejection_fraction = int(request.args.get('ejection_fraction'))
    time = int(request.args.get('time'))
    prediction = model_loader.heart_failure_prediction(ejection_fraction, time)
    return jsonify(prediction=prediction)


@app.route('/drug_prediction', methods=['GET'])
def drug_prediction():
    """
        Predicts the recommended drug based on patient parameters.

        This function retrieves age, sex, blood pressure, cholesterol,
        and sodium-to-potassium ratio from the request arguments and passes
        them to the `model_loader.drug_prediction` function. The prediction
        result is then returned as a JSON object.

        Returns:
        - prediction (str): Recommended drug for the patient.
        """
    age = int(request.args.get('age'))
    sex = int(request.args.get('sex'))
    bp = int(request.args.get('bp'))
    cholesterol = int(request.args.get('cholesterol'))
    na_to_k = float(request.args.get('na_to_k'))
    prediction = model_loader.drug_prediction(age, sex, bp, cholesterol, na_to_k)
    return jsonify(prediction=prediction)


@app.route('/breast_cancer_prediction', methods=['GET'])
def breast_cancer_prediction():
    """
    Predicts the likelihood of breast cancer based on tumor attributes.

    This function retrieves concave points worst and perimeter worst
    from the request arguments and passes them to the
    `model_loader.breast_cancer_prediction` function. The prediction
    result is a boolean value indicating whether the likelihood of
    breast cancer is high (True) or low (False).

    Returns:
    - prediction (bool): True if the likelihood of breast cancer is high,
                         False otherwise.
    """
    concave_points_worst = float(request.args.get('concave_points_worst'))
    perimeter_worst = float(request.args.get('perimeter_worst'))
    prediction = model_loader.breast_cancer_prediction(concave_points_worst, perimeter_worst)
    return jsonify(prediction=prediction)


@app.route('/transcribe_audio', methods=['POST'])
def transcribe_audio_route():
    """
       Transcribes the audio file provided in the request.

       This function extracts the audio file from the request and
       passes it to the `at.transcribe_audio` function for transcription.
       The transcription result is then returned as a JSON object.

       Returns:
       - transcription (str): Transcription of the audio file.
       """
    try:
        # Get the audio file from the request
        audio_file = request.files['audio']

        # Transcribe the audio file
        transcription = at.transcribe_audio(audio_file)

        # Return the transcription as JSON response
        return jsonify({'transcription': transcription})

    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return jsonify({'error': str(e)})


@app.route('/recognize_emotion', methods=['POST'])
def process_image():
    """
       Recognizes emotions in the provided image.

       This function extracts the image file from the request and
       passes it to the `fer.detectFaces` function to detect faces.
       Then, it utilizes the `fer.emotionRecognition` function to recognize
       emotions in the detected faces. Finally, it returns the detected
       emotions as a JSON object.

       Returns:
       - emotions (list): List of dictionaries containing emotions recognized
                          in each detected face.
       """
    try:
        # Get the image file from the request
        image_file = request.files['file']  # Use 'file' instead of 'image'

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            image_file.save(temp_file)
            temp_file_path = temp_file.name

        img = cv2.imread(temp_file_path)
        cv2.imshow('Uploaded Photo', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Detect faces in the image
        #faces = fer.detectFaces(image_file)

        # Recognize emotions in detected faces
        #emotions = fer.emotionRecognition(faces)
        #print(emotions)

        #return jsonify({'emotions': emotions})

    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
