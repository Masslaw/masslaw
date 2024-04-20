import styled from "styled-components";

const IconSpan = styled.span`
    position: relative;
    padding: 0;
    display: inline-block;
    vertical-align: middle;
    height: 100%;
`

const IconSvg = styled.svg`
    position: relative;
    width: 1em;
    height: 100%;
    min-height: 100%;
    fill: currentColor;
`

export function Icon({children}) {
    return <IconSpan><IconSvg viewBox={'0 0 1 1'}><path d={children}/></IconSvg></IconSpan>
}