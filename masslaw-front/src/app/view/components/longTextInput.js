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
    padding: 8px;
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
    font-size: 14px;
    line-height: 16px;
    
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
`;

export function LongTextInput(props) {

    return (<>
            <FormContainer id={props.id} fontsize={props.fontSize} width={props.width}>
                {props.label && (<Label height="2em">{props.label}</Label>)}
                {props.subLabel && (<SubLabel height="1em">{props.subLabel}</SubLabel>)}
                <VerticalGap gap="0.8em"/>
                <InputContainer
                    color={props.color}
                    borderColor={props.borderColor}
                    borderRadius={props.borderRadius}
                    backgroundColor={props.backgroundColor}
                    height={props.height}
                >
                    <Input
                        color={props.color}
                        placeholder={props.placeholder}
                        value={props.value}
                        backgroundColor={props.backgroundColor}
                        onChange={e => {
                            e.preventDefault();
                            e.stopPropagation();
                            props.setValue(e.target.value);
                        }}
                    />
                    <ValidIndicator color={(props.value || '').length > (props.maxLength || 0) ? 'red' : 'forestgreen'}>
                        {`${(props.value || '').length}/${props.maxLength || 0}`}
                    </ValidIndicator>
                </InputContainer>
            </FormContainer>
        </>);
}
