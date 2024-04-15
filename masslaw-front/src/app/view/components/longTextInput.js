import styled from "styled-components";
import React from "react";
import {SVG_PATHS} from "../config/svgPaths";
import {VerticalGap} from "./verticalGap";

const FormContainer = styled.div`
    position: relative;
    width: ${({width}) => width};
`;

const Label = styled.label`
    display: block;
    position: relative;
    width: calc(100% - 2px);
    overflow: hidden;
    font-size: 14px;
    color: white;
    height: ${({height}) => height};
    line-height: ${({height}) => height};
`;

const SubLabel = styled.label`
    display: block;
    position: relative;
    width: calc(100% - 4px);
    overflow: hidden;
    font-size: 12px;
    color: #808080;
    height: ${({height}) => height};
    line-height: ${({height}) => height};
`;

const InputContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: ${({backgroundColor}) => backgroundColor || 'none'};
    border: 1px solid ${({borderColor}) => borderColor};
    border-radius: 8px;
    overflow: hidden;
    color: ${({color}) => color};
    width: calc(100% - 16px - 2px);
    height: ${({height}) => height};
    padding: ${({padding}) => padding || '8px'};
`;

const Input = styled.textarea`
    width: 100%;
    height: 100%;
    color: ${({color}) => color || 'white'};
    background: ${({backgroundColor}) => backgroundColor || 'none'};
    caret-color: ${({color}) => color || 'white'};
    outline: none;
    border: none;
    padding: 0;
    resize: none;
    overflow-y: scroll;
    overflow-x: hidden;
    font: inherit;
    font-size: ${({fontsize}) => fontsize || '14px'};
    line-height: ${({fontsize}) => `calc(${fontsize || '14px'} + 4px)`};
    
    &:-internal-autofill-selected {
        background: none !important;
        color: white !important;
    }

    &::-webkit-scrollbar { display: none; }
`;

const ValidIndicator = styled.div`
    position: absolute;
    bottom: 0;
    color: ${({color}) => color};
    width: calc(100% - 1em);
    background: none;
    border: none;
    padding: 0;
    margin: 4px;
    text-align: right;
    font-size: 12px;
`;

export function LongTextInput(props) {

    return (<>
            <FormContainer id={props.id} fontsize={props.fontSize} width={props.width}>
                {props.label ? <>
                    <Label>{props.label}</Label>
                    <VerticalGap gap="8px"/>
                </> : <></>}
                {props.subLabel ? <>
                    <SubLabel>{props.subLabel}</SubLabel>
                    <VerticalGap gap="8px"/>
                </> : <></>}
                <InputContainer
                    color={props.color}
                    borderColor={props.borderColor}
                    borderRadius={props.borderRadius}
                    backgroundColor={props.backgroundColor}
                    height={props.height}
                    padding={props.padding}
                >
                    <Input
                        color={props.color}
                        placeholder={props.placeholder}
                        value={props.value}
                        backgroundColor={props.backgroundColor}
                        fontsize={props.fontSize}
                        onChange={e => {
                            e.preventDefault();
                            e.stopPropagation();
                            props.setValue(e.target.value);
                        }}
                    />
                    {props.hideValidIndicator ? <></> : <>
                        <ValidIndicator color={(props.value || '').length > (props.maxLength || 0) ? 'red' : 'white'}>
                            {`${(props.value || '').length}/${props.maxLength || 0}`}
                        </ValidIndicator>
                    </>}
                </InputContainer>
            </FormContainer>
        </>);
}
