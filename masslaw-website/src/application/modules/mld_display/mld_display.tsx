import {DocumentMLDContent, MLDContent} from "./config/mld_structure";
import React, {useEffect} from "react";
import {MLDRenderer} from "./rendering/mld_renderer";

import './css.css'
import axios from "axios";
import LoadingIcon from "../../shared/components/loading_icon/loading_icon";

export class MLDDisplay extends React.Component<MLDDisplayProps, MLDDisplayState> {

    constructor(props: MLDDisplayProps) {
        super(props);
        this.state = {
            mldContent: null,
        } as MLDDisplayState;
    }

    componentDidMount() {
        if (this.props.sourceURL) {
            this._loadMLDFile().then();
        }
    }

    componentDidUpdate(prevProps: MLDDisplayProps) {
        if (prevProps.sourceURL !== this.props.sourceURL) {
            this._loadMLDFile().then();
        }
    }

    componentWillUnmount() {

    }

    public render = () : JSX.Element => {
        return <this._renderInternal />
    }

    private _renderInternal = () :JSX.Element => {
        return (
            <>
                <div className={'mld-display-container'}>
                    <div className={'mld-display-frame'} />
                    <div className={'mld-display-content-rendering-area'}>
                        {   this.state.mldContent != null ?
                            <MLDRenderer renderContent={this.state.mldContent}/>
                            :
                            <><LoadingIcon width={100} color={'#000000'} /></>
                        }
                    </div>
                </div>
            </>
        )
    }

    private _loadMLDFile = async (): Promise<any> => {
        try {
            new URL(this.props.sourceURL);
            let content = (await axios.get(this.props.sourceURL)).data as DocumentMLDContent;
            this.setState({mldContent: content});
        } catch (error) {
            return;
        }
    }
}

export interface MLDDisplayProps {
    sourceURL: string,
}
export interface MLDDisplayState {
    mldContent: MLDContent | null,
}