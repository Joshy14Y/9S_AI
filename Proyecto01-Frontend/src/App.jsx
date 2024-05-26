import { Canvas } from "@react-three/fiber";
import { Suspense, useState } from "react";
import Loader from "./components/Loader";
import { Assitant } from "./models/Assitant";
import { RecordVideo } from "./components/RecordVideo";
import { SpeechToText } from "./components/SpeechToText";
import { Modal } from "./components/Modal";
import { handleEndPointToCall, transcribeAudio } from "./client/client";
import { Spinner } from "./components/Spinner";
import { formatWord } from "./utilities/formatWord";
import { Toaster } from "react-hot-toast";
import { notifyError } from "./utilities/notifyError";
import { notifyResult } from "./utilities/notifyResult";

const App = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [spinner, setSpinner] = useState(false);
    const [formData, setFormData] = useState({});
    const [endPointToCall, setEndPointToCall] = useState("");

    const adjustAssistantForScreenSize = () => {
        let screenScale, screenPosition;

        if (window.innerWidth < 380) {
            screenScale = [1.5, 1.5, 1.5];
            screenPosition = [0, -2, 0];
        }
        else if (window.innerWidth < 768) {
            screenScale = [2, 2, 2];
            screenPosition = [0, -2, 0];
        } else {
            screenScale = [7, 7, 7];
            screenPosition = [1, -6.5, -20];
        }

        return [screenScale, screenPosition];
    }

    const [assistantScale, assistantPosition] =
        adjustAssistantForScreenSize();

    const handleOnChange = (field, value) => {
        setFormData(prevData => ({
            ...prevData,
            [field]: {
                ...prevData[field],
                value: value
            }
        }));
    }

    const openModal = (word) => {
        switch (word) {
            case "sandp" || "s&p" || "sp500":
                setFormData({
                    date: {
                        type: "date",
                        value: "",
                        placeholder: ""
                    }
                });
                setEndPointToCall("snp");
                break;
            case "ethereum":
                setFormData({
                    date: {
                        type: "date",
                        value: "",
                        placeholder: ""
                    }
                });
                setEndPointToCall("ethereum");
                break;
            case "bitcoin":
                setFormData({
                    date: {
                        type: "date",
                        value: "",
                        placeholder: ""
                    }
                });
                setEndPointToCall("bitcoin");
                break;
            case "avocado":
                setFormData({
                    date: {
                        type: "date",
                        value: "",
                        placeholder: ""
                    }
                });
                setEndPointToCall("avocado");
                break;
            case "wine":
                setFormData({
                    volatileAcidity: {
                        type: "text",
                        value: "",
                        placeholder: "Enter the volatile acidity"
                    },
                    density: {
                        type: "text",
                        value: "",
                        placeholder: "Enter the density"
                    },
                    alcohol: {
                        type: "text",
                        value: "",
                        placeholder: "Enter the alcohol"
                    }
                });
                setEndPointToCall("wine");
                break;
            case "stroke":
                setFormData({
                    age: {
                        type: "number",
                        value: "",
                        placeholder: "Enter the age"
                    },
                    hypertension: {
                        type: "number",
                        value: "",
                        placeholder: "Enter the hypertension"
                    },
                    heartDisease: {
                        type: "number",
                        value: "",
                        placeholder: "Enter the heart disease"
                    },
                    avgGlucoseLevel: {
                        type: "number",
                        value: "",
                        placeholder: "Enter the average glucose level"
                    }
                });
                setEndPointToCall("stroke");
                break;
            case "pokemon":
                setFormData({
                    baseEggSteps: {
                        type: "number",
                        value: "",
                        placeholder: "Enter the base egg steps"
                    },
                    percentageMale: {
                        type: "number",
                        value: "",
                        placeholder: "Enter the percentage of male"
                    }
                });
                setEndPointToCall("pokemon");
                break;
            case "failure":
                setFormData({
                    ejectionFraction: {
                        type: "number",
                        value: "",
                        placeholder: "Enter the ejection fraction"
                    },
                    time: {
                        type: "number",
                        value: "",
                        placeholder: "Enter the time"
                    }
                });
                setEndPointToCall("failure");
                break;
            case "drug":
                setFormData({
                    age: {
                        type: "number",
                        value: "",
                        placeholder: "Enter the age"
                    },
                    sex: {
                        type: "number",
                        value: "",
                        placeholder: "Enter the sex"
                    },
                    bp: {
                        type: "text",
                        value: "",
                        placeholder: "Enter the bp"
                    },
                    cholesterol: {
                        type: "number",
                        value: "",
                        placeholder: "Enter the cholesterol"
                    },
                    naToK: {
                        type: "number",
                        value: "",
                        placeholder: "Enter the naToK"
                    }
                });
                setEndPointToCall("drug");
                break;
            case "cancer":
                setFormData({
                    concavePointsWorst: {
                        type: "number",
                        value: "",
                        placeholder: "Enter the concave points worst"
                    },
                    perimeterWorst: {
                        type: "number",
                        value: "",
                        placeholder: "Enter the perimeter worst"
                    }
                });
                setEndPointToCall("cancer");
                break;

            default:
                notifyError(word);

                return;
        }
        setIsOpen(true);
    }

    const handleSendAudio = async (audioFile) => {
        setSpinner(true);
        const transcription = await transcribeAudio(audioFile);
        const word = formatWord(transcription);
        setSpinner(false);
        openModal(word);
    }

    const handleSubmit = async () => {
        const result = await handleEndPointToCall(endPointToCall, formData);
        let msg = new SpeechSynthesisUtterance(result);
        speechSynthesis.speak(msg);
        notifyResult(result);
    }

    return (
        <section className="w-full h-screen absolute top-0 z-[-2] bg-neutral-950 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(120,119,198,0.3),rgba(255,255,255,0))]
        flex flex-col md:flex-row">
            <Canvas
                style={{
                    width: window.innerWidth < 768 ? "100%" : "50%",
                    height: "100%"
                }}
                camera={{ near: 0.1, far: 1000 }}
                className="w-full h-screen bg-transparent">
                <Suspense fallback={<Loader />}>
                    <directionalLight position={[1, 1, 1]} intensity={2} />
                    <ambientLight intensity={0.5} />
                    <hemisphereLight skyColor="#b1e1ff" groundColor="#000000"
                        intensity={1} />
                    <Assitant
                        scale={assistantScale}
                        position={assistantPosition}
                        rotation={[0, 0, 0]}
                    />
                </Suspense>
            </Canvas>

            <RecordVideo>
                <SpeechToText
                    handleSendAudio={handleSendAudio}
                />
            </RecordVideo>

            <Modal
                isOpen={isOpen}
                setIsOpen={setIsOpen}
                formData={formData}
                handleOnChange={handleOnChange}
                handleSubmit={handleSubmit}
            />

            <Spinner
                isOpen={spinner}
            />

            <Toaster />
        </section>
    )
}

export default App;