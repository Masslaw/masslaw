import {HeaderLogo} from "./_headerLogo";
import styled from "styled-components";
import {HeaderInteractiveSection} from "./_interactiveSection";

const Container = styled.div`
    width: 100%;
    height: 55px;
    background-color: black;
    display: flex;
    flex-direction: row;
    align-items: center;
    border: 0 solid transparent;
    border-bottom: 1px solid #606060;
`

const LogoContainer = styled.div`
    position: relative;
    height: 100%;
    margin: 0;
    padding: 0;
`

const HeaderInteractiveSectionContainer = styled.div`
    height: 100%;
    width: 128px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
    margin-left: 16px;
`

export function HomeHeader(props) {
    return <>
        <Container>
            <LogoContainer>
                <HeaderLogo/>
            </LogoContainer>
            <HeaderInteractiveSectionContainer>
                <HeaderInteractiveSection/>
            </HeaderInteractiveSectionContainer>
        </Container>
    </>
}
