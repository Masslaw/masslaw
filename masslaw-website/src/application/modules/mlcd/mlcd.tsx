import React, {useEffect, useRef, useState} from "react";
import './css.css'
import {CaseFileAnnotationData, CaseFileData} from "../../infrastructure/cases_management/data_structures";
import {IconProp} from "@fortawesome/fontawesome-svg-core";
import {OpticalDocumentRenderer} from "./renderers/optical_document_renderer/optical_document_renderer";


export interface MLCDProps  {
    fileData: CaseFileData,
    fileAnnotations: CaseFileAnnotationData[],
    selectionToolkitButtons: MLCDSelectionButton[],
    onAnnotationClicked: (annotation: CaseFileAnnotationData) => void,
    scrollToChar?: number,
    onSelection?: (fromChar: number, toChar: number, text: string) => void,
}

export function MasslawContentDisplay(props: MLCDProps) {

    const displayContentAreaRef = useRef<HTMLDivElement>(null);

    const getAppropriateRenderer = (type: string): MLCDContentRenderingComponent => {
        let RendererComponent: MLCDContentRenderingComponent = ((props: MLCDProps) => (<></>));

        switch (type) {
            case ('pdf'):
            case ('bmp'):
            case ('pbm'):
            case ('pgm'):
            case ('ppm'):
            case ('sr'):
            case ('ras'):
            case ('jpeg'):
            case ('jpg'):
            case ('jpe'):
            case ('jp2'):
            case ('tiff'):
            case ('tif'):
            case ('png'):
            case ('exr'):
            case ('hdr'):
            case ('pic'):
            case ('webp'):
            case ('doc'):
            case ('docx'):
                RendererComponent = OpticalDocumentRenderer;
                break;
        }

        return  (props: MLCDProps) => {
            return <RendererComponent {...props} />
        }
    }

    return (
        <>
            <div className={'mlcd-display-container'}>
                <div className={'mlcd-display-frame'} />
                <div className={'mlcd-display-content-rendering-area'}>
                    <div
                        className={'mlcd-display-content-render-area'}
                        ref={displayContentAreaRef}
                    >
                        {getAppropriateRenderer(props.fileData.type)(props)}
                    </div>
                </div>
            </div>
        </>
    )
}

export interface MLCDSelectionButton {
    icon: IconProp,
    name: string,
    callback: (fromChar: number, toChar: number, text: string) => void,
}

export type MLCDContentRenderingComponent = React.FC<MLCDProps & any>;