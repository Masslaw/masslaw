import React from "react";
import {MLDContent} from "../config/mld_structure";
import {MLDDisplayToolbar} from "./toolbar/mld_toolbar";
import {MLDContentDisplay} from "./content/mld_content_display";


export class MLDRenderer extends React.Component<MLDRendererProps, MLDRendererState> {

    constructor(props: MLDRendererProps) {
        super(props);
        this.state = {} as MLDRendererState;
    }

    public render = () : JSX.Element => {
        return <this._renderInternal />
    }

    private _renderInternal = () :JSX.Element => {
        return (
            <>
                <div className={'mld-display-toolbar-container'}>
                    <MLDDisplayToolbar />
                </div>
                <div className={'mld-display-content-container'}>
                    <MLDContentDisplay renderContent={this.props.renderContent}/>
                </div>
            </>
        )
    }
}
export interface MLDRendererProps {
    renderContent: MLDContent
}
export interface MLDRendererState {
}