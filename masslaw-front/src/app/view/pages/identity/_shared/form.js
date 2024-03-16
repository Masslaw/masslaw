import styled from "styled-components";

const Container = styled.div`
        position: absolute;
        width: ${({width}) => width};
        height: ${({height}) => height};
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: linear-gradient(132deg, rgba(222,169,0,1) 0%, rgba(255,229,84,1) 40%, rgba(222,169,0,1) 100%);
        border: none;
        border-radius: ${({border_radius}) => border_radius};
        overflow: visible;
        filter: drop-shadow(0 0 5px white);
        display: flex;
        flex-direction: column;
        align-items: center;
        color: white;
        font-size: 1.7vh;
        
        & > div:first-child {
            position: absolute;
            width: calc(${({width}) => width} - 6px);
            height: calc(${({height}) => height} - 4px);
            left: 3px;
            top: 2px;
            border-radius: calc(${({border_radius}) => border_radius} - 2px);
            overflow: hidden;
            background: black;
        }
    `

export function IdentityForm(props) {
    return <Container
        width={"45vh"}
        height={"60vh"}
        border_radius={"2.5vh"}
    >
        <div/>
        {props.children}
    </Container>
}