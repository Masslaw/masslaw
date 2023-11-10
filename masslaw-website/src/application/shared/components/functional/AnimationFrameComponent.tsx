// AnimationFrameComponent.tsx
import React, { useEffect, useRef } from 'react';

interface AnimationFrameComponentProps {
    onFrame: (deltaTime: number) => void;
}

const AnimationFrameComponent: React.FC<AnimationFrameComponentProps> = ({ onFrame }) => {
    const frameRef = useRef<number>();
    const lastTimestampRef = useRef<number>();

    const animate = (timestamp: number) => {
        if (lastTimestampRef.current !== undefined) {
            const deltaTime = (timestamp - lastTimestampRef.current) / 1000;
            onFrame(deltaTime);
        }

        lastTimestampRef.current = timestamp;
        frameRef.current = requestAnimationFrame(animate);
    };

    useEffect(() => {
        frameRef.current = requestAnimationFrame(animate);
        return () => {
            if (frameRef.current !== undefined) {
                cancelAnimationFrame(frameRef.current);
            }
        };
    }, []);

    return <></>;
};

export default AnimationFrameComponent;