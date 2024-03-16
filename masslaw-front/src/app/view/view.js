import React from "react";
import ReactDOM from "react-dom/client";
import {ApplicationView} from "./_applicationView";


export function initView() {
    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(
        <React.StrictMode>
            <ApplicationView />
        </React.StrictMode>
    );
}
