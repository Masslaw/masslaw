import styled from "styled-components";
import {CaseTextSearch} from "../../../../../components/caseTextSearch";
import {model} from "../../../../../../model/model";
import {ApplicationRoutes} from "../../../../../../config/applicaitonRoutes";
import {useParams} from "react-router-dom";
import {constructUrl} from "../../../../../../controller/functionality/navigation/urlConstruction";

const PageContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    overflow-y: auto;
`

const PageTitle = styled.div`
    font-size: 24px;
    font-weight: bold;
    margin: 16px 16px 8px 16px;
    color: white;
`

const PageSubTitle = styled.div`
    font-size: 16px;
    font-weight: normal;
    margin: 8px 16px;
    color: #808080;
`

const SearchTextInputContainer = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    margin: 16px;
    width: calc(100% - 32px);
`

const SearchButton = styled.button`
    position: relative;
    margin-left: 16px;
    width: 96px;
    height: 34px;
    background: ${({enabled}) => enabled ? "white" : "none"};
    color: ${({enabled}) => enabled ? "black" : "white"};
    border: 1px solid white;
    border-radius: 8px;
    pointer-events: ${({enabled}) => enabled ? "all" : "none"};
    font-size: 14px;
    cursor: pointer;
    &:hover {
        ${({enabled}) => enabled ? "filter: drop-shadow(0 0 5px white)" : ""}
    }
}
`

const SearchResultsStickySection = styled.div`
    position: sticky;
    top: 0;
    display: flex;
    flex-direction: row;
    padding: 16px;
    width: calc(100% - 32px);
    background: black;
`

const SearchResultsContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 100%;
`

const NoSearchResults = styled.div`
    width: 100%;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: #808080;
`

export function CaseSearch(props) {
    const {caseId} = useParams();

    model.application.pages.currentPage.name = "CaseSearch";

    return <>
        <PageContainer>
            <PageTitle>Search Case</PageTitle>
            <PageSubTitle>Search for text in this case's files</PageSubTitle>
            <CaseTextSearch
                files={null}
                onResultClicked={(searchText, result) => {
                    model.application.navigate(constructUrl(
                        ApplicationRoutes.FILE_DISPLAY,
                        {caseId: caseId, fileId: result.file_id},
                        {s: searchText},
                    ));
                }}
            />
        </PageContainer>
    </>
}
