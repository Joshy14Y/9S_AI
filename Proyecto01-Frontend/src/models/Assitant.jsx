
import { useAnimations, useGLTF } from "@react-three/drei";
import { useEffect, useRef } from "react";

import assitantScene from "../assets/3d/robot_playground.glb";

export const Assitant = ({...props}) => {
    const ref = useRef();
    const { scene, animations } = useGLTF(assitantScene);
    const { actions } = useAnimations(animations, ref);

    useEffect(() => {
        actions.Experiment.play();
    }, [actions]);

    return (
        <mesh {...props} ref={ref}>
            <primitive object={scene} />
        </mesh>
    )
}