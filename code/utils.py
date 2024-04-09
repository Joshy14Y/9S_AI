import whisper


def transcribe_audio(audio_url):
    try:
        # Download the audio file from the URL to a temporary file
        response = requests.get(audio_url)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name

        # Transcribe the content of the audio
        model = whisper.load_model("base")
        result = model.transcribe(temp_file_path)

        # Extract the transcription
        transcription = result["text"]

        # Clean up the temporary file
        os.unlink(temp_file_path)

        return transcription

    except Exception as e:
        print(f"Error processing audio: {audio_url}. {e}")
        return None