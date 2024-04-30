import React, { useState } from "react";

export const SpeechToText = ({ handleSendAudio }) => {
  const [audioURL, setAudioURL] = useState(null);
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);

  const startRecording = () => {
    if (!navigator.mediaDevices) {
      alert("Media devices not supported in your browser");
      return;
    }

    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then(stream => {
        const recorder = new MediaRecorder(stream);
        recorder.addEventListener("dataavailable", e => {
          const audio = new Blob([e.data], { type: "audio/wav" });
          setAudioBlob(audio);
          const url = URL.createObjectURL(audio);
          setAudioURL(url);
        });

        const maxRecordingTime = 6000;
        setTimeout(() => {
          recorder.stop();
          setRecording(false);
        }, maxRecordingTime);

        recorder.start();
        setRecording(true);
        setMediaRecorder(recorder);
      })
      .catch(error => {
        console.error("Error accessing microphone:", error);
        alert("Error accessing microphone");
      });
  };


  const stopRecording = () => {
    if (mediaRecorder && recording) {
      mediaRecorder.stop();
      setRecording(false);
    }
  };

  const clearRecording = () => {
    if (audioURL) {
      URL.revokeObjectURL(audioURL);
      setAudioURL(null);
    }
  };

  return (
    <div className="flex items-center gap-4 mt-4">
      {
        audioURL &&
        <div className="flex items-center gap-2">
          <button onClick={clearRecording}>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-8 text-red-500">
              <path strokeLinecap="round" strokeLinejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
            </svg>
          </button>

          <audio controls src={audioURL} />
        </div>
      }
      <button onClick={recording ? stopRecording : startRecording}>
        <div className="bg-white w-16 h-16 rounded-full flex
       items-center justify-center">
          {
            recording
              ? <img src="/icons/microphone.gif" width={28} height={28} />
              : <img src="/icons/mute-unmute.png" width={28} height={28} />
          }
        </div>
      </button>

      {
        audioURL &&
        <button
          className="text-cyan-600 text-lg rounded-lg font-bold p-2"
          onClick={() => handleSendAudio(audioBlob)}>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-8">
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5" />
          </svg>
        </button>
      }
    </div>
  );
};
