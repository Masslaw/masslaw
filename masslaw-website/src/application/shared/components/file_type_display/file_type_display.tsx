import React, {useState} from "react";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {
    faFile,
    faFileAlt,
    faFileArchive,
    faFileAudio,
    faFileCsv,
    faFileExcel,
    faFileImage,
    faFilePdf,
    faFilePowerpoint,
    faFileVideo,
    faFileWord
} from "@fortawesome/free-solid-svg-icons";

import "./css.css"

export function FileTypeDisplay(props: { type: string }) {

    const [isPasswordVisible, setPasswordVisible] = useState(false);

    const togglePasswordVisibility = () => {
        setPasswordVisible(!isPasswordVisible);
    };

    return (<div
            className={'files-list-file-type-container'}>
                            <span>{(() => {
                                switch (props.type.toLowerCase()) {
                                    case 'pdf':
                                        return <FontAwesomeIcon icon={faFilePdf}/>;
                                    case 'png':
                                    case 'jpeg':
                                    case 'jpg':
                                        return <FontAwesomeIcon icon={faFileImage}/>;
                                    case 'doc':
                                    case 'docx':
                                        return <FontAwesomeIcon icon={faFileWord}/>;
                                    case 'xls':
                                    case 'xlsx':
                                        return <FontAwesomeIcon icon={faFileExcel}/>;
                                    case 'ppt':
                                    case 'pptx':
                                        return <FontAwesomeIcon icon={faFilePowerpoint}/>;
                                    case 'zip':
                                    case 'rar':
                                        return <FontAwesomeIcon icon={faFileArchive}/>;
                                    case 'txt':
                                        return <FontAwesomeIcon icon={faFileAlt}/>;
                                    case 'csv':
                                        return <FontAwesomeIcon icon={faFileCsv}/>;
                                    case 'mp3':
                                    case 'wav':
                                        return <FontAwesomeIcon icon={faFileAudio}/>;
                                    case 'mp4':
                                    case 'avi':
                                    case 'mkv':
                                        return <FontAwesomeIcon icon={faFileVideo}/>;
                                    default:
                                        return <FontAwesomeIcon icon={faFile}/>;
                                }
                            })()}
                            </span>
            <span>{props.type}</span>
        </div>
    )
}