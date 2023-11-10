import React from "react";


export class MLDDisplayToolbar extends React.Component<MLDDisplayToolbarProps, MLDDisplayToolbarState> {

    constructor(props: MLDDisplayToolbarProps) {
        super(props);
        this.state = {} as MLDDisplayToolbarState;
    }

    public render = () : JSX.Element => {
        return <this._renderInternal />
    }

    private _renderInternal = () :JSX.Element => {
        return (
            <>
            </>
        )
    }
}
export interface MLDDisplayToolbarProps {
}
export interface MLDDisplayToolbarState {
}