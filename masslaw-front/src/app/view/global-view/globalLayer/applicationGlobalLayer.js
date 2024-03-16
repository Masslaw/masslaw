import styled from "styled-components";
import {LoadingScreen} from "./_global-layer-components/loadingScreen";
import {ApplicationNotifications} from "./_global-layer-components/notifications";
import {HomeHeader} from "./_header/header";
import {useModelValueAsReactState} from "../../../controller/functionality/model/modelReactHooks";
import {UserMenu} from "./_userMenu/userMenu";
import {ApplicationPopups} from "./_global-layer-components/popups";

const GlobalLayer = styled.div`
    position: absolute;
    width: 100%;
    height: 100%;
    background: none;
    color: white;
    display: block;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 100;
    overflow: hidden;
    margin: 0;
    padding: 0;
    pointer-events: none;
`

const Application = styled.div`
    position: absolute;
    width: 100%;
    height: 100%;
    background: none;
    display: flex;
    flex-direction: column;
    pointer-events: auto;
`

const HeaderSection = styled.div`
    position: relative;
    display: ${({headerShown}) => headerShown ? 'flex' : 'none'};
    width: 100vw;
    background: black;
    z-index: 10;
`

const ApplicationViewport = styled.div`
    position: relative;
    width: 100vw;
    background: black;
    z-index: 1;
    overflow: auto;
    margin: 0;
    padding: 0;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
`

export function ApplicationGlobalLayer(props) {

    const [s_headerShown, setHeaderShown] = useModelValueAsReactState('$.application.view.state.header.shown');

    return <GlobalLayer>
        <Application>
            <HeaderSection headerShown={s_headerShown}>
                <HomeHeader/>
            </HeaderSection>
            <ApplicationViewport>
                {props.children}
            </ApplicationViewport>
        </Application>
        <UserMenu/>
        <ApplicationNotifications/>
        <ApplicationPopups/>
        <LoadingScreen/>
    </GlobalLayer>
}