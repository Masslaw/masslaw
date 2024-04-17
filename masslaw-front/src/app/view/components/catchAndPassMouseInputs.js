import React, {cloneElement, useEffect} from "react";

export function CatchAndPassMouseInputs({ children }) {
    return (
        <>
            {React.Children.map(children, child => {
                if (!React.isValidElement(child)) return child;
                let newProps = {...child.props};
                Object.keys(child.props).forEach(propName => {
                    if (typeof child.props[propName] !== 'function') return;
                    const originalEventHandler = child.props[propName];
                    newProps[propName] = (e) => {
                        const originalPointerEvents = e.target.style.pointerEvents;
                        e.target.style.pointerEvents = 'none';
                        const belowElement = document.elementFromPoint(e.clientX, e.clientY);
                        e.target.style.pointerEvents = originalPointerEvents;
                        if (belowElement && !Array.from(children).includes(belowElement)) belowElement.dispatchEvent(new MouseEvent(e.type, e.nativeEvent));
                        if (originalEventHandler) originalEventHandler(e);
                    };
                });
                return cloneElement(child, newProps);
            })}
        </>
    );
}
