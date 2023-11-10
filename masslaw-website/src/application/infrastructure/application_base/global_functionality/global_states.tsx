import React, {ReactNode, useCallback, useContext, useEffect, useMemo, useState} from "react";

const GlobalStatesContext = React.createContext<
    [{ [key: string]: any }, React.Dispatch<React.SetStateAction<{ [key: string]: any }>>]>([{}, () => {}]);

export type globalStateDeclaration<T> = [string, T?];

export function useGlobalState<T>(declaration: globalStateDeclaration<T>): [T, (v: T | ((p: T) => T)) => void] {
    const [global_state, setGlobalState] = useContext(GlobalStatesContext);

    const [stateKey, stateDefaultValue] = declaration;

    const stateValue: T = global_state.hasOwnProperty(stateKey) ? global_state[stateKey] : stateDefaultValue;

    const setStateFunction = useCallback((value: T | ((p: T) => T)) => {
        setGlobalState(prevGlobalState => {
            const newValue = (typeof value === 'function' ? (value as ((p: T) => T))(stateValue) : value) as T;
            return {
                ...prevGlobalState,
                [stateKey]: newValue
            };
        });
    }, [stateKey, stateValue]);

    return [stateValue, setStateFunction];
}

export function ApplicationGlobalStates(props: { children: ReactNode }) {
    const [global_states, setGlobalStates] = useState({} as { [key: string]: any });
    const children = useMemo(() => props.children, []);
    return (
        <GlobalStatesContext.Provider value={[global_states, setGlobalStates]}>
            {children}
        </GlobalStatesContext.Provider>
    );
}
