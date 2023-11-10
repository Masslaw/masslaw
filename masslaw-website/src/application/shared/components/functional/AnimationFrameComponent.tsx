// AnimationFrameComponent.tsx
import React, { useEffect, useRef } from 'react';

export function AnimationFrameComponent(props: { onFrame: (deltaTime: number) => void }) {
    const frameRef = useRef<number>();
    const lastTimestampRef = useRef<number>();

    const animate = (timestamp: number) => {
        if (lastTimestampRef.current !== undefined) {
            const deltaTime = (timestamp - lastTimestampRef.current) / 1000;
            props.onFrame(deltaTime);
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