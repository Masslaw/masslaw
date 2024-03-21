import styled from "styled-components";

const GapDiv = styled.div`height: ${({gap}) => gap};`

export function VerticalGap(props) {
    return <GapDiv gap={props.gap || "1em"}/>
}