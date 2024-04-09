import { Canvas } from "@react-three/fiber";
import { Suspense } from "react";
import Loader from "./components/Loader";
import { Assitant } from "./models/Assitant";
import { RecordVideo } from "./components/RecordVideo";
import { SpeechToText } from "./components/SpeechToText";

const App = () => {
    const adjustPlaneForScreenSize = () => {
        let screenScale, screenPosition;

        if (window.innerWidth < 380) {j
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

    const [planeScale, planePosition] =
        adjustPlaneForScreenSize();

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
                        scale={planeScale}
                        position={planePosition}
                        rotation={[0, 0, 0]}
                    />
                </Suspense>
            </Canvas>

            <RecordVideo>
                <SpeechToText />
            </RecordVideo>
        </section>
    )
}

export default App;