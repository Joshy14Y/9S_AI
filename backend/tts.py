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
    """
    Computes the Connectionist Temporal Classification (CTC) loss.

    This function calculates the CTC loss, which is useful for training sequence-to-sequence models where the alignment between input and output sequences is unknown. It is commonly used in tasks like speech recognition and handwriting recognition.

    Args:
        y_true (tf.Tensor): A tensor of shape (batch_size, max_label_length) containing the ground truth labels.
        y_pred (tf.Tensor): A tensor of shape (batch_size, time_steps, num_classes) containing the predicted logits.

    Returns:
        tf.Tensor: A tensor of shape (batch_size, 1) containing the CTC loss for each sequence in the batch.

    Example:
        y_true = tf.constant([[1, 2, 3], [1, 2, 0]])
        y_pred = tf.random.uniform((2, 10, 5))
        loss = CTCLoss(y_true, y_pred)
        print(loss)

    Notes:
        - The ground truth labels `y_true` should be padded with zeros if they have different lengths.
        - The predicted logits `y_pred` should be the raw output of the network before applying softmax.
        - The `input_length` and `label_length` are automatically computed based on the shapes of `y_pred` and `y_true`.
    """
    # Compute the training-time loss value
    batch_len = tf.cast(tf.shape(y_true)[0], dtype="int64")
    input_length = tf.cast(tf.shape(y_pred)[1], dtype="int64")
    label_length = tf.cast(tf.shape(y_true)[1], dtype="int64")

    input_length = input_length * tf.ones(shape=(batch_len, 1), dtype="int64")
    label_length = label_length * tf.ones(shape=(batch_len, 1), dtype="int64")

    loss = keras.backend.ctc_batch_cost(y_true, y_pred, input_length, label_length)
    return loss


model = tf.keras.models.load_model(r'deep_learning_models/weights/tts.keras', custom_objects={'CTCLoss': CTCLoss})
# The set of characters accepted in the transcription.
characters = [x for x in "abcdefghijklmnopqrstuvwxyz "]
# Mapping characters to integers
char_to_num = keras.layers.StringLookup(vocabulary=characters, oov_token="")
# Mapping integers back to original characters
num_to_char = keras.layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), oov_token="", invert=True
)


def decode_batch_predictions(pred):
    """
    Decodes the output predictions of a CTC-based model into readable text.

    This function takes the raw predictions from a model trained with Connectionist Temporal Classification (CTC) loss
     and decodes them into text sequences. It uses a greedy search by default, but can be modified to use beam search
      for more complex tasks.

    Args:
        pred (numpy.ndarray): A 3D array of shape (batch_size, time_steps, num_classes) containing the output predictions
         from the model.

    Returns:
        list of str: A list of decoded text sequences for each batch element.

    Example:
        pred = np.random.rand(2, 10, 5)  # Example predictions
        decoded_texts = decode_batch_predictions(pred)
        print(decoded_texts)  # Output: ['text1', 'text2']

    Notes:
        - The function assumes the presence of a `num_to_char` mapping function, which converts numerical predictions to
         their corresponding characters.
        - Greedy search is used for decoding by default. For better accuracy, especially on complex tasks, consider
        using beam search.
    """
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
    """
    Transforms an audio file to a specific format suitable for further processing.

    This function takes an input audio file, resamples it to 22050 Hz, converts it to mono (single channel), and applies
     an asynchronous resampling filter. The transformed audio is saved to a temporary WAV file, which is returned for
     further use.

    Args:
        input_file (str): The path to the input audio file.

    Returns:
        tempfile._TemporaryFileWrapper: A temporary file object containing the transformed audio.

    Example:
        temp_output = transform_audio('input.mp3')
        print(temp_output.name)  # Output: Path to the temporary WAV file

    Notes:
        - The function uses `ffmpeg` for audio processing, which must be installed and available in the system path.
        - The temporary file is not deleted automatically when closed. The caller is responsible for deleting it when
         no longer needed.

    Dependencies:
        - ffmpeg-python: Install with `pip install ffmpeg-python`
        - ffmpeg: Install from https://ffmpeg.org/download.html
    """
    # Create a temporary file to store the output
    temp_output = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    # Perform the transformation
    ffmpeg.input(input_file).output(temp_output.name, ar=22050, ac=1, af="aresample=async=1:min_hard_comp=0.100000:first_pts=0",
                                    loglevel="quiet").run(overwrite_output=True)
    # Return the temporary file object
    return temp_output


def transcribe_audio(audio_file):
    """
    Transcribes an audio file to text using a pre-trained model.

    This function reads an audio file, computes its spectrogram, normalizes it, and passes it through a pre-trained
     model to get the transcription. It returns the decoded transcription of the audio.

    Args:
        audio_file (str): The path to the input audio file.

    Returns:
        str: The transcribed text from the audio file.

    Example:
        transcription = transcribe_audio('input.wav')
        print(transcription)  # Output: Transcribed text

    Notes:
        - The `decode_batch_predictions` function should be defined to decode the model predictions into readable text.
    """
    # Read the audio file
    file = tf.io.read_file(audio_file)
    audio, _ = tf.audio.decode_wav(file, desired_channels=1)
    audio = tf.squeeze(audio, axis=-1)
    audio = tf.cast(audio, tf.float32)

    # Compute the spectrogram
    spectrogram = tf.signal.stft(audio, frame_length=256, frame_step=160, fft_length=384)
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