import {SVG_PATHS} from "../../../config/svgPaths";
import styled from "styled-components";
import {model} from "../../../../model/model";
import {constructUrl} from "../../../../controller/functionality/navigation/urlConstruction";
import {ApplicationRoutes} from "../../../../config/applicaitonRoutes";
import {LogoSvg} from "../../../components/logoSvg";

const Container = styled.div`
    position: relative;
    display: flex;
    height: 100%;
    cursor: pointer;
    justify-content: center;
    align-items: center;
    
    svg {
        height: calc(100% - 20px);
        margin: 15px;
    }
    
    path {
        stroke: white;
        fill: white;
    }
`

const HeaderWebsiteName = styled.div`
    height: 100%;
    line-height: 100%;
    color: white;
    font-family: sans-serif;
    font-size: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
`

export function HeaderLogo(props) {
    return <>
        <Container onClick={_ => model.application.navigate(constructUrl(ApplicationRoutes.HOME))}>
            <LogoSvg/>
            <HeaderWebsiteName>MassLaw</HeaderWebsiteName>
        </Container>
    </>
}