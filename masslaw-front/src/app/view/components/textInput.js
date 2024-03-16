import styled from "styled-components";
import React from "react";
import {SVG_PATHS} from "../config/svgPaths";
import {VerticalGap} from "./bits-and-pieces/verticalGap";

const FormContainer = styled.div`
    position: relative;
    width: ${({width}) => width || "100%"};
`;

const Label = styled.label`
    display: block;
    position: relative;
    width: calc(100% - 0.25em);
    overflow: hidden;
    font-size: 1em;
    margin-left: 0.25em;
    color: white;
    height: ${({height}) => height};
    line-height: ${({height}) => height};
`;

const SubLabel = styled.label`
    display: block;
    position: relative;
    width: calc(100% - 0.25em);
    overflow: hidden;
    font-size: 0.7em;
    margin-left: 0.3em;
    color: #999999;
    height: ${({height}) => height};
    line-height: ${({height}) => height};
`;

const InputContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    border: 1px solid ${({borderColor}) => borderColor};
    border-radius: ${({borderRadius}) => borderRadius || "0.5em"};
    overflow: hidden;
    color: ${({color}) => color};
    width: 100%;
    height: ${({height}) => height};
`;

const Input = styled.input`
    font-size: 1em;
    width: calc(100% - 1em);
    height: 100%;
    color: white;
    outline: none;
    background: none;
    border: none;
    padding: 0;
    margin: 0.5em;
    caret-color: white;

    &:-internal-autofill-selected {
        background: none !important;
        color: white !important;
    }
`;

const ValidIndicator = styled.div`
    width: ${({size}) => size};
    height: ${({size}) => size};
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0.75;

    svg {
        width: 100%;
        height: 100%;
    }

    path {
        fill: ${({logoColor}) => logoColor};
    }
`;

const ShowPasswordButton = styled.div`
    position: relative;
    height: 0.5em;
    color: cornflowerblue;
    cursor: pointer;
    font-size: 0.75em;
    margin: 0.5em;
`

export function TextInput(props) {
    const {indicatorGoodPath = "checkMark", indicatorBadPath = "crossMark"} = props;
    const indicatorLogoPath = React.useMemo(() => SVG_PATHS[props.valid === true ? indicatorGoodPath : indicatorBadPath], [props.valid]);
    const indicatorLogoColor = React.useMemo(() => props.indicatorColor || (props.valid === true ? "forestgreen" : "red"), [props.valid, props.indicatorColor]);

    const [showPassword, setShowPassword] = React.useState(false);

    const inputType = React.useMemo(() => {
        if (props.type === "password") return showPassword ? "text" : "password";
        return props.type;
    }, [props.type, showPassword]);

    return (<>
        <FormContainer id={props.id} width={props.width}>
            {props.label && <>
                <Label height="2em">{props.label}</Label>
                <VerticalGap gap="0.2em"/>
            </>}
            {props.subLabel && <>
                <SubLabel height="1em">{props.subLabel}</SubLabel>
                <VerticalGap gap="0.8em"/>
            </>}
            <InputContainer
                color={props.color}
                borderColor={props.borderColor}
                borderRadius={props.borderRadius}
                height={props.height}
            >
                <Input
                    type={inputType}
                    placeholder={props.placeholder}
                    value={props.value}
                    onChange={e => {
                        e.preventDefault();
                        e.stopPropagation();
                        props.setValue(e.target.value);
                    }}
                    onKeyUp={e => e.key === "Enter" && props.onEnter && props.onEnter()}
                    list={props.id + "datalist"}
                />
                {props.hasIndicator && (<ValidIndicator size={props.height} logoColor={indicatorLogoColor}>
                    <svg viewBox={"-1000 -1000 3000 3000"}>
                        <path d={indicatorLogoPath}/>
                    </svg>
                </ValidIndicator>)}
            </InputContainer>
            {props.type === "password" && !props.disableShowPassword && <ShowPasswordButton
                onClick={() => setShowPassword(p => !p)}
            >
                {showPassword ? "Hide Password" : "Show Password"}
            </ShowPasswordButton> || <></>}
            <datalist id={props.id + "datalist"}>
                {(props.options || []).map((option, idx) => <option key={idx} value={option}/>)}
            </datalist>
        </FormContainer>
    </>);
}
