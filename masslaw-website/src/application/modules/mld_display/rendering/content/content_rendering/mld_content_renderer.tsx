import React from "react";
import {DocumentMLDContent, MLDContent} from "../../../config/mld_structure";
import {DocumentMLDContentRenderer} from "./type_rendering/document/document_mld_content_renderer";


export class MLDContentRenderer extends React.Component<MLDContentRendererProps, MLDContentRendererState> {

    constructor(props: MLDContentRendererProps) {
        super(props);
        this.state = {} as MLDContentRendererState;
    }

    public render = () : JSX.Element => {
        return <this._renderInternal />
    }

    private _renderInternal = () : JSX.Element => {
        return (
            <>
                <div className={'mld-contend-render-container'} >
                    <this._renderContentRenderer />
                </div>
            </>
        )
    }

    private _renderContentRenderer = () : JSX.Element => {
        switch (this.props.renderContent.type) {
            case 'document':
                return (<DocumentMLDContentRenderer renderContent={this.props.renderContent as DocumentMLDContent} />);
            default:
                return (<></>);
        }
    }
}
export interface MLDContentRendererProps {
    renderContent: MLDContent
}
export interface MLDContentRendererState {
}