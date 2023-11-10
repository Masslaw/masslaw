// LoadingIcon.tsx
import React, {CSSProperties, useState} from 'react';
import AnimationFrameComponent from "../functional/AnimationFrameComponent";
import {parseColor, rgbToHex} from "../../util/parse_color_string";

export function LoadingIcon(props: {
        width?: number,
        color?: string,
        periodDuration?: number,
        ballSize?: number
    }) {

    const width = ((props.width == null) ? 50 : props.width) as number;
    const color = ((props.color == null) ? '#ffffff' : props.color) as string;
    const periodDuration = ((props.periodDuration == null) ? 0.75 : props.periodDuration) as number;
    const ballSize = ((props.ballSize == null) ? 15 : props.ballSize) as number;

    const [ball_position, setBallPosition] = useState(0);
    const [ball_scale_x, setBallScaleX] = useState(1);
    const [ball_scale_y, setBallScaleY] = useState(1);

    let period_delta = 0;

    const onFrame = (deltaTime: number) => {

        period_delta = (period_delta + deltaTime) % periodDuration;

        const periodDeltaFraction = period_delta / periodDuration;

        const periodSectionBounds = [0, 0.35, 0.5, 0.85, 1.0];

        let currentSectionIndex : number = (() : number => {
            for (let i = 0; i < periodSectionBounds.length; i++)
                if (periodDeltaFraction < periodSectionBounds[i]) return i-1
            return 0
        })();

        let sectionDeltaFraction = (periodDeltaFraction - periodSectionBounds[currentSectionIndex]) /
            (periodSectionBounds[currentSectionIndex+1] - periodSectionBounds[currentSectionIndex]);

        let ballScaleX = 0;
        switch (currentSectionIndex) {
            case 0:
                ballScaleX = (sectionDeltaFraction-0.5)**2 + 0.75;
                setBallScaleX(ballScaleX);
                setBallScaleY(2-ballScaleX);
                setBallPosition(0);
                break;
            case 1:
                setBallScaleX(1.2);
                setBallScaleY(0.8);
                setBallPosition((width-ballSize) * (sectionDeltaFraction));
                break;
            case 2:
                ballScaleX = (sectionDeltaFraction-0.5)**2 + 0.75;
                setBallScaleX(ballScaleX);
                setBallScaleY(2-ballScaleX);
                setBallPosition(width - (ballSize * ballScaleX));
                break;
            case 3:
                setBallScaleX(1.2);
                setBallScaleY(0.8);
                setBallPosition((width-ballSize) * (1-sectionDeltaFraction));
                break;
        }
    };

    const ballContainerStyle: CSSProperties = {
        background: `none`,
        width: `${width}px`,
        height: `${ballSize*2}px`,
        position: `relative`,
    }

    const ballStyle: CSSProperties = {
        left: `${ball_position}px`,
        top: `${ballSize/2}px`,
        background: `${color}`,
        width: `${ballSize}px`,
        height: `${ballSize}px`,
        transform: `scale(${ball_scale_x},${ball_scale_y})`,
        position: `absolute`,
        borderRadius: '50%',
    }

    return (
        <>
            <AnimationFrameComponent onFrame={onFrame} />
            <div className="loading-icon-container" style={{ display: 'flex', position: `relative`, justifyContent: 'center', alignItems: 'center', width: '100%', height: '100%'}}>
                <div className="loading-ball-container" style={ballContainerStyle}>
                    <div className="ball" style={ballStyle}></div>
                </div>
            </div>
        </>
    );
};

export default LoadingIcon;
