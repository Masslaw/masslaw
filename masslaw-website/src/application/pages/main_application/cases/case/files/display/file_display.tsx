import {useParams} from "react-router-dom";

import './css.css'
import {MLDDisplay} from "../../../../../../modules/mld_display/mld_display";
import {useEffect, useState} from "react";
import {CasesManager} from "../../../../../../infrastructure/cases_management/cases_manager";

export function FileDisplay() {

    const { caseId, fileId } = useParams();

    const [file_url, setFileUrl] = useState('');

    useEffect(() => {
        (async () => {
            setFileUrl(await CasesManager.getInstance().get_file_download(caseId || '',fileId || '', 'display'));
        })().then();
    }, []);

    return (
        <>
            <div className={'file-content-display-area'}>
                <MLDDisplay sourceURL={file_url}/>
            </div>
        </>
    )
}