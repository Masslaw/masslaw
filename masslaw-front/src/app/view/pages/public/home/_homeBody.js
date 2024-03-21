import styled from "styled-components";
import {VerticalGap} from "../../../components/verticalGap";
import {SVG_PATHS} from "../../../config/svgPaths";

const Separator = styled.div`
    width: 100%;
    height: 2px;
    background: rgb(0, 0, 0);
    background: linear-gradient(90deg, rgba(0, 0, 0, 1) 10%, rgba(222, 169, 0, 1) 29%, rgba(255, 229, 84, 1) 40%, rgba(222, 169, 0, 1) 60%, rgba(0, 0, 0, 1) 90%);
`

const Title1 = styled.div`
    width: 100%;
    font-size: 2vw;
    font-weight: bold;
    letter-spacing: 4px;
    color: white;
    margin: 2vw;
    text-align: center;
    filter: drop-shadow(0 0 10px gold);
`

const FlyingPaper = styled.svg`
    position: absolute;
    background: none;

    & path:nth-child(1) {
        stroke: gold;
        fill: none;
        stroke-width: 10;
        filter: drop-shadow(0 0 50px yellow);
    }

    & path:nth-child(2) {
        stroke: white;
        fill: none;
        stroke-width: 2;
        filter: drop-shadow(0 0 50px white);
    }
`

export function HomeBody(props) {
    return <>
        <Separator/>
        <VerticalGap gap="3vw"/>
        <Title1>A Tool Built For People That Make Law Happen.</Title1>

        <FlyingPaper viewBox={"-25 -25 1050 1050"} style={{width: "8vw", top: "16vw", left: "16vw", transform: "rotate(32deg)"}}>
            <path d={SVG_PATHS.paperFlying1}/>
            <path d={SVG_PATHS.paperFlying1}/>
        </FlyingPaper>
        <FlyingPaper viewBox={"-25 -25 1050 1500"} style={{width: "5vw", top: "11vw", left: "12vw", transform: "rotate(90deg)"}}>
            <path d={SVG_PATHS.paperFlying2}/>
            <path d={SVG_PATHS.paperFlying2}/>
        </FlyingPaper>
        <FlyingPaper viewBox={"-25 -25 1050 1500"} style={{width: "6vw", top: "19vw", left: "14vw", transform: "rotate(145deg)"}}>
            <path d={SVG_PATHS.paperFlying5}/>
            <path d={SVG_PATHS.paperFlying5}/>
        </FlyingPaper>
        <FlyingPaper viewBox={"-25 -25 1050 1500"} style={{width: "4vw", top: "27vw", left: "11vw", transform: "rotate(145deg)"}}>
            <path d={SVG_PATHS.paperFlying6}/>
            <path d={SVG_PATHS.paperFlying6}/>
        </FlyingPaper>
        <FlyingPaper viewBox={"-25 -25 1050 1500"} style={{width: "7vw", top: "26vw", left: "15vw", transform: "rotate(145deg)"}}>
            <path d={SVG_PATHS.paperFlying4}/>
            <path d={SVG_PATHS.paperFlying4}/>
        </FlyingPaper>
    </>
}
