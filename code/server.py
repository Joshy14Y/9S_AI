from flask import Flask, request, jsonify
from models import ModelLoader
import os
import tempfile
import requests
import whisper

app = Flask(__name__)

model_loader = ModelLoader()


@app.route('/s&p_prediction', methods=['GET'])
def s_and_p_prediction():
    model = 's&p'
    input_date = request.args.get('input_date')
    prediction = model_loader.process_SARIMAX(model, input_date)
    return jsonify(prediction=prediction)


@app.route('/ethereum_prediction', methods=['GET'])
def ethereum_prediction():
    model = 'ethereum'
    input_date = request.args.get('input_date')
    prediction = model_loader.process_SARIMAX(model, input_date)
    return jsonify(prediction=prediction)


@app.route('/bitcoin_prediction', methods=['GET'])
def bitcoin_prediction():
    model = 'bitcoin'
    input_date = request.args.get('input_date')
    prediction = model_loader.process_SARIMAX(model, input_date)
    return jsonify(prediction=prediction)


@app.route('/avocado_prediction', methods=['GET'])
def avocado_prediction():
    model = 'avocado'
    input_date = request.args.get('input_date')
    prediction = model_loader.process_SARIMAX(model, input_date)
    return jsonify(prediction=prediction)


@app.route('/process_SARIMAX', methods=['GET'])
def process_SARIMAX():
    model = request.args.get('model')
    input_date = request.args.get('input_date')
    prediction = model_loader.process_SARIMAX(model, input_date)
    return jsonify(prediction=prediction)


@app.route('/wine_prediction', methods=['GET'])
def wine_prediction():
    volatile_acidity = float(request.args.get('volatile_acidity'))
    density = float(request.args.get('density'))
    alcohol = float(request.args.get('alcohol'))
    prediction = model_loader.wine_prediction(volatile_acidity, density, alcohol)
    return jsonify(prediction=prediction)


@app.route('/stroke_prediction', methods=['GET'])
def stroke_prediction():
    age = int(request.args.get('age'))
    hypertension = int(request.args.get('hypertension'))
    heart_disease = int(request.args.get('heart_disease'))
    avg_glucose_level = float(request.args.get('avg_glucose_level'))
    prediction = model_loader.stroke_prediction(age, hypertension, heart_disease, avg_glucose_level)
    return jsonify(prediction=prediction)


@app.route('/pokemon_prediction', methods=['GET'])
def pokemon_prediction():
    base_egg_steps = int(request.args.get('base_egg_steps'))
    percentage_male = float(request.args.get('percentage_male'))
    prediction = model_loader.pokemon_prediction(base_egg_steps, percentage_male)
    return jsonify(prediction=prediction)


@app.route('/heart_failure_prediction', methods=['GET'])
def heart_failure_prediction():
    ejection_fraction = int(request.args.get('ejection_fraction'))
    time = int(request.args.get('time'))
    prediction = model_loader.heart_failure_prediction(ejection_fraction, time)
    return jsonify(prediction=prediction)


@app.route('/drug_prediction', methods=['GET'])
def drug_prediction():
    age = int(request.args.get('age'))
    sex = int(request.args.get('sex'))
    bp = int(request.args.get('bp'))
    cholesterol = int(request.args.get('cholesterol'))
    na_to_k = float(request.args.get('na_to_k'))
    prediction = model_loader.drug_prediction(age, sex, bp, cholesterol, na_to_k)
    return jsonify(prediction=prediction)


@app.route('/breast_cancer_prediction', methods=['GET'])
def breast_cancer_prediction():
    concave_points_worst = float(request.args.get('concave_points_worst'))
    perimeter_worst = float(request.args.get('perimeter_worst'))
    prediction = model_loader.breast_cancer_prediction(concave_points_worst, perimeter_worst)
    return jsonify(prediction=prediction)


@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        # Get the audio file from the request
        audio_file = request.files['audio']

        # Save the audio file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            audio_file.save(temp_file.name)
            temp_file_path = temp_file.name

        # Transcribe the content of the audio
        model = whisper.load_model("base")
        result = model.transcribe(temp_file_path)

        # Extract the transcription
        transcription = result["text"]

        # Clean up the temporary file
        os.unlink(temp_file_path)

        return jsonify({'transcription': transcription})

    except Exception as e:
        print(f"Error processing audio: {e}")
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
