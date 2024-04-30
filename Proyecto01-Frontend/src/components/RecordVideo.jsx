import { useRef, useEffect, useState } from "react"
import { CameraButton } from "./CameraButton"
import { recognizeEmotion } from "../client/client"

export const RecordVideo = ({ children }) => {
    const videoRef = useRef()
    const [iscameraOn, setIsCameraOn] = useState(true)
    useEffect(() => {
        if (iscameraOn) {
            startVideo()
        } else {
            stopVideo();
        }
    }, [iscameraOn])

    useEffect(() => {
        let intervalId;
        if (iscameraOn) {
            intervalId = setInterval(captureFrame, 1000);
        }
        return () => clearInterval(intervalId);
    }, [iscameraOn]);

    const toggleCamera = () => {
        setIsCameraOn(!iscameraOn);
    }

    const startVideo = () => {
        if (iscameraOn) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then((currentStream) => {
                    videoRef.current.srcObject = currentStream
                })
                .catch((err) => {
                    console.log(err)
                })
        }
    }

    const stopVideo = () => {
        const stream = videoRef.current.srcObject;
        if (stream) {
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            videoRef.current.srcObject = null;
        }
    }

    const captureFrame = async () => {
        if (iscameraOn && videoRef.current) {
            const canvas = document.createElement("canvas");
            const ctx = canvas.getContext("2d");
            canvas.width = videoRef.current.videoWidth;
            canvas.height = videoRef.current.videoHeight;
            ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
            canvas.toBlob(async (blob) => {
                const file = new File([blob], "screenshot.jpg", {
                    type: "image/jpg",
                });

                // Llamar a la función recognizeEmotion con el archivo de imagen
                const emotions = await recognizeEmotion(file);
                console.log("Emotions detected:", emotions);
            }, "image/jpg");
        }
    }

    return (
        <div className="flex flex-col justify-center items-center mt-10 w-1/2">
            {/* <button
                onClick={toggleCamera}
                className="flex items-center gap-2 justify-center text-white p-2 border 
          border-white rounded-lg mb-6">
                {iscameraOn ? "Turn off camera" : "Turn on camera"}
                {iscameraOn
                    ? <img src="/video-camera-slash.svg" alt="video-camera" width={24} />
                    : <img src="/video-camera.svg" alt="video-camera" width={24} />
                }
            </button> */}
            <div className="flex gap-10 items-start">
                <div className="flex flex-col items-end">
                    <video crossOrigin="anonymous" width={500} ref={videoRef} autoPlay></video>
                    {children}
                </div>
            </div>
        </div>
    )
}