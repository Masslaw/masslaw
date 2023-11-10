import {useParams} from "react-router-dom";

export function CaseMain() {

    const { caseId } = useParams();

    return (
        <>
            <h1>{`case main ${caseId}`}</h1>
        </>
    )
}