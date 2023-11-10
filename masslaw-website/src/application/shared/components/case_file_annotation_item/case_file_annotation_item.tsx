import {
    annotation_type_to_icon,
    annotation_type_to_name,
    CaseFileAnnotationData
} from "../../../infrastructure/cases_management/data_structures";

import './css.css'
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {Accordion} from "../accordion/accordion";
import {unixTimeToPastTimeString} from "../../util/date_time_utiles";


export function CaseFileAnnotationItem(props: {
    annotationData: CaseFileAnnotationData,
    onClick: () => void
}) {
    return <div
        className={'annotation-list-display-item clickable'}
        style={{
            borderColor: props.annotationData.color,
        }}
        onClick={props.onClick}
    >
        <p className={'annotation-display-annotation-type'}><FontAwesomeIcon icon={annotation_type_to_icon[props.annotationData.type]} />  {annotation_type_to_name[props.annotationData.type]}</p>
        <div className={'annotation-display-annotated-text'} dir={'auto'}>
            {`''${props.annotationData.annotated_text}''`}
        </div>
        {
            props.annotationData.annotation_text &&
            <div
                className={'annotation-display-annotation-text'}
                dir={'auto'}
                style={{
                    background: `${props.annotationData.color}50`
                }}
            >
                {props.annotationData.annotation_text}
            </div>
            || <></>
        }
        <Accordion
            title={'info'}
            component={
            <>
                <p className={'annotation-info-item'}> <b>Modified: </b> {
                    unixTimeToPastTimeString(props.annotationData.last_modified)}</p>
                <p className={'annotation-info-item'}> <b>Created By: </b> {props.annotationData.creator}</p>
            </>
            }
        />
    </div>
}