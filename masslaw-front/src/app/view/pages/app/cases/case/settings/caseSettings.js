import styled from "styled-components";

const PageContainer = styled.div`
    width: 100%;
    height: 100%;
    overflow: auto;
    background: #303030;
`

const Label = styled.label`
    display: block;
    position: relative;
    width: calc(100% - 0.25em);
    overflow: hidden;
    font-size: 1em;
    margin-left: 0.25em;
    color: white;
    height: ${({height}) => height};
    line-height: ${({height}) => height};
`;

const SubLabel = styled.label`
    display: block;
    position: relative;
    width: calc(100% - 0.25em);
    overflow: hidden;
    font-size: 0.7em;
    margin-left: 0.3em;
    color: #999999;
    height: ${({height}) => height};
    line-height: ${({height}) => height};
`;

export function CaseSettings(props) {
    return <>
        <PageContainer>

        </PageContainer>
    </>
}