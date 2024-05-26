import tempfile
import tensorflow as tf
from tensorflow import keras
import ffmpeg
import numpy as np
import os
import logging

# Set TensorFlow logging level to only display errors
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 0 = all messages, 1 = info, 2 = warnings, 3 = errors


def CTCLoss(y_true, y_pred):
    # Compute the training-time loss value
    batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
    input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
    label_length = tf.cast(tf.shape(y_true)[1], dtype="int64")

    input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
    label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")

    loss = keras.backend.ctc_batch_cost(y_true, y_pred, input_length, label_length)
    return loss


model = tf.keras.models.load_model(r'deep_learning_models/weights/tts.keras', custom_objects={'CTCLoss': CTCLoss})
# An integer scalar Tensor. The window length in samples.
frame_length = 256
# An integer scalar Tensor. The number of samples to step.
frame_step = 160
# An integer scalar Tensor. The size of the FFT to apply.
fft_length = 384
# The set of characters accepted in the transcription.
characters = [x for x in "abcdefghijklmnopqrstuvwxyz "]
# Mapping characters to integers
char_to_num = keras.layers.StringLookup(vocabulary=characters, oov_token="")
# Mapping integers back to original characters
num_to_char = keras.layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), oov_token="", invert=True
)


def decode_batch_predictions(pred):
    input_len = np.ones(pred.shape[0]) * pred.shape[1]
    # Use greedy search. For complex tasks, you can use beam search
    results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0]
    # Iterate over the results and get back the text
    output_text = []
    for result in results:
        result = tf.strings.reduce_join(num_to_char(result)).numpy().decode("utf-8")
        output_text.append(result)
    return output_text


def transform_audio(input_file):
    # Create a temporary file to store the output
    temp_output = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    # Perform the transformation
    ffmpeg.input(input_file).output(temp_output.name, ar=22050, ac=1, af="aresample=async=1:min_hard_comp=0.100000:first_pts=0", loglevel="quiet").run(overwrite_output=True, )
    # Return the temporary file object
    return temp_output


def transcribe_audio(audio_file):
    # Read the audio file
    file = tf.io.read_file(audio_file)
    audio, _ = tf.audio.decode_wav(file, desired_channels=1)
    audio = tf.squeeze(audio, axis=-1)
    audio = tf.cast(audio, tf.float32)

    # Compute the spectrogram
    spectrogram = tf.signal.stft(
        audio, frame_length=frame_length, frame_step=frame_step, fft_length=fft_length
    )
    spectrogram = tf.abs(spectrogram)
    spectrogram = tf.math.pow(spectrogram, 0.5)

    # Normalization
    means = tf.math.reduce_mean(spectrogram, 1, keepdims=True)
    stddevs = tf.math.reduce_std(spectrogram, 1, keepdims=True)
    spectrogram = (spectrogram - means) / (stddevs + 1e-10)

    # Add batch dimension
    spectrogram = tf.expand_dims(spectrogram, axis=0)

    # Pass through the model
    prediction = model.predict(spectrogram)

    # Decode the transcription
    transcription = decode_batch_predictions(prediction)

    return transcription


if __name__ == "__main__":
    # Test with an audio file
    input_audio_file = r"test.wav"  # Replace with the path to your input WAV file
    print("Transforming audio...")
    transformed_file = transform_audio(input_audio_file)
    print("Transcribing audio...")
    transcription = transcribe_audio(transformed_file.name)
    print("Transcription:", transcription)

    # Close and delete the temporary file
    transformed_file.close()