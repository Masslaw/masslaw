import styled from "styled-components";
import {HomeFace} from "./_homeFace";
import {HomeBody} from "./_homeBody";
import {model} from "../../../../model/model";

const Background = styled.div`
        width: 100%;
        height: 100%;
        background-color: black;
        overflow-y: scroll;
        overflow-x: hidden;
        &::-webkit-scrollbar { display: none; }
    `

const FaceSection = styled.div`
        position: relative;
        width: 100%;
        height: 100%;
        background-color: black;
    `

const BodySection = styled.div`
        position: relative;
        width: 100%;
        
    `

export function Home(props) {

    model.application.view.state.header.shown = true;
    model.application.pages.currentPage.minimumUserStatus = null;
    model.application.pages.currentPage.maximumUserStatus = 0;
    model.application.pages.currentPage.name = 'Home';

    return <>
        <Background>
            <FaceSection>
                <HomeFace/>
            </FaceSection>
            <BodySection>
                <HomeBody/>
            </BodySection>
        </Background>
    </>
}