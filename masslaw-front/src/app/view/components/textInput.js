import styled from "styled-components";
import React, {useMemo, useState} from "react";
import {SVG_PATHS} from "../config/svgPaths";
import {VerticalGap} from "./verticalGap";

const FormContainer = styled.div`
    position: relative;
    width: ${({width}) => width || "100%"};
`;

const Label = styled.label`
    display: block;
    position: relative;
    width: calc(100% - 2px);
    overflow: hidden;
    font-size: 14px;
    color: white;
`;

const SubLabel = styled.label`
    display: block;
    position: relative;
    width: calc(100% - 4px);
    overflow: hidden;
    font-size: 12px;
    color: #808080;
`;

const InputContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    border: 1px solid ${({borderColor}) => borderColor};
    border-radius: ${({borderRadius}) => borderRadius || "8px"};
    overflow: hidden;
    color: ${({color}) => color};
    width: calc(100% - 16px - 2px);
    padding: 8px;
`;

const Input = styled.input`
    width: 100%;
    color: white;
    outline: none;
    background: none;
    border: none;
    padding: 0;
    caret-color: white;
    font-size: 14px;
    height: 16px;
    line-height: 16px;

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
    margin-left: 0.5em;

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
    height: 8px;
    color: cornflowerblue;
    cursor: pointer;
    font-size: 12px;
    margin: 8px;
`

export function TextInput(props) {
    const {indicatorGoodPath = "checkMark", indicatorBadPath = "crossMark"} = props;
    const indicatorLogoPath = useMemo(() => SVG_PATHS[props.valid === true ? indicatorGoodPath : indicatorBadPath], [props.valid]);
    const indicatorLogoColor = useMemo(() => props.indicatorColor || (props.valid === true ? "forestgreen" : "red"), [props.valid, props.indicatorColor]);

    const [showPassword, setShowPassword] = useState(false);

    const inputType = useMemo(() => {
        if (props.type === "password") return showPassword ? "text" : "password";
        return props.type;
    }, [props.type, showPassword]);

    return (<>
        <FormContainer id={props.id} width={props.width}>
            {props.label && <>
                <Label>{props.label}</Label>
                <VerticalGap gap="8px"/>
            </>}
            {props.subLabel && <>
                <SubLabel>{props.subLabel}</SubLabel>
                <VerticalGap gap="8px"/>
            </>}
            <InputContainer
                color={props.color}
                borderColor={props.borderColor}
                borderRadius={props.borderRadius}
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
                {props.hasIndicator && (<ValidIndicator size={`calc(${props.height} * 0.33)`} logoColor={indicatorLogoColor}>
                    <svg viewBox={"0 0 1 1"}>
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
