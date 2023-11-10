import React from "react";
import {MLDContentRenderer} from "./content_rendering/mld_content_renderer";
import {MLDContent} from "../../config/mld_structure";


export class MLDContentDisplay extends React.Component<MLDContentDisplayProps, MLDContentDisplayState> {

    constructor(props: MLDContentDisplayProps) {
        super(props);
        this.state = {} as MLDContentDisplayState;
    }

    public render = () : JSX.Element => {
        return <this._renderInternal />
    }

    private _renderInternal = () :JSX.Element => {
        return (
            <>
                <div className={'mld-display-content-render-area'}>
                    <MLDContentRenderer renderContent={this.props.renderContent}/>
                </div>
            </>
        )
    }
}
export interface MLDContentDisplayProps {
    renderContent: MLDContent
}
export interface MLDContentDisplayState {
}