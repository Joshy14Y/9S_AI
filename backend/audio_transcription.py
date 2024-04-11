import whisper
import tempfile
import os

def transcribe_audio(audio_file):
    """
    Transcribes the audio file.

    This function takes an audio file and transcribes its content
    using a speech-to-text model. It saves the audio file to a
    temporary file, transcribes it, and returns the transcription.

    Parameters:
    - audio_file: Audio file to transcribe.

    Returns:
    - transcription (str): Transcription of the audio file.
    """
    try:
        # Save the audio file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(audio_file.read())
            temp_file_path = temp_file.name

        # Transcribe the content of the audio
        model = whisper.load_model("base")
        result = model.transcribe(temp_file_path)

        # Extract the transcription
        transcription = result["text"]

        # Clean up the temporary file
        os.unlink(temp_file_path)

        # Print transcription for debugging
        print(transcription)

        return transcription

    except Exception as e:
        # Handle exceptions and print error message
        print(f"Error processing audio: {e}")
        return None