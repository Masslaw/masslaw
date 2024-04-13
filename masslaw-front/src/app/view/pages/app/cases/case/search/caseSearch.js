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
    background: #202020;
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
