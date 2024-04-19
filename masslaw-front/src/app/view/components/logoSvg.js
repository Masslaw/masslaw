import {SVG_PATHS} from "../config/svgPaths";
import styled from "styled-components";


const Svg = styled.svg`
    stroke-width: 0;
`

export function LogoSvg() {
    return <Svg viewBox={"0 0 1 1"}>
        <path d={SVG_PATHS.logoTop}/>
        <path d={SVG_PATHS.logoRight}/>
        <path d={SVG_PATHS.logoLeft}/>
        <path d={SVG_PATHS.logoBottom}/>
    </Svg>
}