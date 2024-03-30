import styled from "styled-components";
import {SVG_PATHS} from "../../../config/svgPaths";
import {constructUrl} from "../../../../controller/functionality/navigation/urlConstruction";
import {ApplicationRoutes} from "../../../../config/applicaitonRoutes";
import {RedirectButtonWrapper} from "../../../components/redirectButtonWrapper";

const FaceSvg = styled.svg`
    width: 100%;
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

const FaceFloatingSection = styled.div`
    position: absolute;
    top: 6vw;
    left: 6vw;
    color: white;
    font-family: sans-serif;
`

const FaceTextTitle = styled.div`
    position: relative;
    font-size: 4.5vw;
    font-weight: bold;
    letter-spacing: 2px;
    height: 5vw;
    line-height: 5vw;
    margin: 1vw;
`

const FaceTextSubTitle = styled.div`
    position: relative;
    font-size: 2.5vw;
    height: 3vw;
    line-height: 3vw;
    margin: 1vw;
    font-weight: bold;
    letter-spacing: 2px;
`

const FaceText = styled.div`
    position: relative;
    font-size: 1.25vw;
    letter-spacing: 2px;
    word-spacing: 2px;
    width: 50vw;
    margin: 1vw;
    line-height: 2vw;
`

const FaceStartNowButton = styled.button`
    position: relative;
    font-size: 1.2vw;
    width: 20vw;
    height: 4vw;
    background: linear-gradient(132deg, rgba(222, 169, 0, 1) 0%, rgba(255, 229, 84, 1) 40%, rgba(222, 169, 0, 1) 100%);
    border: none;
    margin: 1vw;
    border-radius: 2.5vw;
    color: gold;
    overflow: hidden;
    transition-duration: 0.3s;
    letter-spacing: 1px;

    div {
        position: absolute;
        width: calc(20vw - 6px);
        height: calc(4vw - 4px);
        top: 2px;
        left: 3px;
        border-radius: calc(0.5 * (20vw - 4px));
        overflow: hidden;
        z-index: 1;
    }

    div div {
        position: absolute;
        width: 150%;
        height: 150%;
        top: 0;
        left: 0;
        background: black;
        transition: 0.2s linear;
        border-radius: 0;
        transform: skew(45deg);
    }

    span {
        position: relative;
        z-index: 2;
    }

    &:hover div div {
        transform: translateX(100%) skew(45deg);
    }

    &:hover {
        color: black;
    }
`

export function HomeFace(props) {
    return <>
        <FaceSvg viewBox={"0 0 1000 1000"}>
            <FaceSvgGoldFilamentPath d={SVG_PATHS.homeFilament1}/>
            <FaceSvgHighlightFilamentPath d={SVG_PATHS.homeFilament1}/>
            <FaceSvgHighlightFilamentPath d={SVG_PATHS.homeFilament1}/>
        </FaceSvg>
        <FaceFloatingSection>
            <FaceTextTitle>MassLaw</FaceTextTitle>
            <FaceTextSubTitle>Case Analysis Platform.</FaceTextSubTitle>
            <FaceText>{
                "Putting State Of The Art Artificial-Intelligence and " +
                "Machine-Learning solutions into the hands of legal professionals."
            }</FaceText>
            <RedirectButtonWrapper href={constructUrl(ApplicationRoutes.SIGNUP)}>
                <FaceStartNowButton>
                    <div>
                        <div/>
                    </div>
                    <span>Sign Up</span>
                </FaceStartNowButton>
            </RedirectButtonWrapper>
        </FaceFloatingSection>
    </>
}