import {useCallback, useEffect} from "react";

export function useUpdate(callback, dependencies) {
    const m_callback = useCallback(callback, dependencies);
    useEffect(() => {
        let previousTime = Date.now();
        let animationRequest = null;
        const frame = () => {
            const currentTime = Date.now();
            const deltaTime = currentTime - previousTime;
            previousTime = currentTime;
            m_callback(deltaTime);
            animationRequest = requestAnimationFrame(frame);
        }
        animationRequest = requestAnimationFrame(frame);
        return () => cancelAnimationFrame(animationRequest);
    }, dependencies);
}