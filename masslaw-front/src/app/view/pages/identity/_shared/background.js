import styled from "styled-components";
import {SVG_PATHS} from "../../../config/svgPaths";

const BackgroundContainer = styled.div`
    position: absolute;
    width: 100%;
    height: 100%;
    background-color: black;
    overflow: hidden;
`

const BackgroundSvg = styled.svg`
    position: absolute;
    height: 100%;
    left: 50%;
    transform: translateX(-50%);
    background-color: black;
`

const FaceSvgGoldFilamentPath = styled.path`
    stroke: gold;
    fill: none;
    stroke-width: 1;
    filter: drop-shadow(0 0 10px yellow);
`

const FaceSvgHighlightFilamentPath = styled.path`
    stroke: white;
    opacity: 0.5;
    fill: none;
    stroke-width: 0.5;
    filter: drop-shadow(0 0 10px white);
`

export function IdentityBackground(props) {
    return <>
        <BackgroundContainer>
            <BackgroundSvg viewBox={"-500 0 3000 1000"}>
                <g transform="translate(1000 0)">
                    <FaceSvgGoldFilamentPath d={SVG_PATHS.genericFilament1}/>
                    <FaceSvgHighlightFilamentPath d={SVG_PATHS.genericFilament1}/>
                    <FaceSvgGoldFilamentPath d={SVG_PATHS.genericFilament1}/>
                    <FaceSvgHighlightFilamentPath d={SVG_PATHS.genericFilament1}/>
                </g>
                <g transform="translate(1000 1000) scale(-1)">
                    <FaceSvgGoldFilamentPath d={SVG_PATHS.genericFilament1}/>
                    <FaceSvgHighlightFilamentPath d={SVG_PATHS.genericFilament1}/>
                    <FaceSvgGoldFilamentPath d={SVG_PATHS.genericFilament1}/>
                    <FaceSvgHighlightFilamentPath d={SVG_PATHS.genericFilament1}/>
                </g>
            </BackgroundSvg>
        </BackgroundContainer>
    </>
}