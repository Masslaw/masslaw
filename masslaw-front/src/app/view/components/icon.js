import styled from "styled-components";

const IconSpan = styled.span`
    padding: 0;
    display: inline-block;
    vertical-align: middle;
`

const IconSvg = styled.svg`
    width: 1em;
    height: 1em;
    fill: currentColor;
`

export function Icon({children}) {
    return <IconSpan><IconSvg viewBox={'0 0 1 1'}><path d={children}/></IconSvg></IconSpan>
}