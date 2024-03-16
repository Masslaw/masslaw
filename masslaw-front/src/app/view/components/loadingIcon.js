import styled from "styled-components";
import {useEffect, useMemo, useState} from "react";
import {useUpdate} from "../../controller/functionality/time-utils/updateHook";

const LoadingIconContainer = styled.div`
    position: absolute;
    width: ${({width}) => width ? width : "100%"};
    height: ${({height}) => height ? height : "100%"};
    display: flex;
    justify-content: center;
    align-items: center;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    
    svg {
        width: 100%;
        height: 100%;
        background: none;
    }
    
    path {
        fill: ${({color}) => color ? color : "white"};
    }
`

export function LoadingIcon(props) {

    const [s_time, setTime] = useState(0);

    const m_path = useMemo(() => {
        const period = props.period ? props.period : 2000;
        const thickness = props.thickness ? props.thickness : 0.1;
        const normalizedTime = (s_time % period) / period;
        const theta1 = 6 * Math.PI * normalizedTime;
        const thetaDelta = 1.5 * Math.PI * Math.pow(Math.sin(theta1 / 6), 2);
        const theta2 = theta1 + thetaDelta;
        const dot1 = [Math.cos(theta1), Math.sin(theta1)];
        const dot2 = [Math.cos(theta2), Math.sin(theta2)];
        const largeArc = thetaDelta > Math.PI ? 1 : 0;
        return `M ${dot1[0]} ${dot1[1]} 
                L ${dot1[0] - (thickness * Math.cos(theta1))} ${dot1[1] - (thickness * Math.sin(theta1))}
                A ${1 - thickness} ${1 - thickness} 0 ${largeArc} 1 ${dot2[0] - (thickness * Math.cos(theta2))} ${dot2[1] - (thickness * Math.sin(theta2))}
                L ${dot2[0]} ${dot2[1]}
                A 1 1 0  ${largeArc} 0 ${dot1[0]} ${dot1[1]}`;
    }, [s_time, props.period, props.thickness]);

    useUpdate((dt) => setTime(t => t + dt), []);

    return <>
        <LoadingIconContainer width={props.width} height={props.height} color={props.color}>
            <svg viewBox={"-1 -1 2 2"}>
                <path d={m_path}/>
            </svg>
        </LoadingIconContainer>
    </>
}