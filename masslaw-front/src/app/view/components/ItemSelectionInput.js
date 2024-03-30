import styled from "styled-components";
import React, {useCallback, useMemo, useState} from "react";
import {SVG_PATHS} from "../config/svgPaths";
import {VerticalGap} from "./verticalGap";

const FormContainer = styled.div`
    width: ${({containerwidth}) => containerwidth || '100%'};
    margin: ${({containermargin}) => containermargin || '0'};
`

const Label = styled.label`
    display: block;
    position: relative;
    width: calc(100% - 0.25em);
    overflow: hidden;
    font-size: 14px;
    margin-left: 2px;
    color: white;
    height: ${({height}) => height};
    line-height: ${({height}) => height};
`;

const SubLabel = styled.label`
    display: block;
    position: relative;
    width: calc(100% - 0.25em);
    overflow: hidden;
    font-size: 12px;
    margin-left: 4px;
    color: #808080;
    height: ${({height}) => height};
    line-height: ${({height}) => height};
`;

const ItemSelectionContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: row-reverse;
    background: none;
    border-radius: 8px;
    border: 1px solid white;
    height: max-content;
    overflow: visible;
`

const ItemSelectionItemsArea = styled.div`
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    align-items: center;
    height: max-content;
    overflow: hidden;
    color: white;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
    padding: 8px;
`

const ItemSelectionShowListButton = styled.button`
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    background: none;
    border: 0 solid transparent;
    border-left: 1px solid white;
    svg {
        fill: white;
        width: 16px;
        height: 16px;
    }
`

const ItemSelectionItem = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    overflow: hidden;
    color: white;
    background: #707070;
    border: none;
    height: 16px;
    border-radius: 8px;
    line-height: 16px;
    font-size: 12px;
    width: max-content;
    padding: 4px;
    margin-right: 6px;

    button {
        display: flex;
        align-items: center;
        justify-content: center;
        height: 10px;
        width: 10px;
        margin-left: 4px;
        padding: 0;
        background: none;
        border: none;
        cursor: pointer;

        svg {
            width: 100%;
            height: 100%;
            fill: white;
        }
    }
`

const ItemSelectionTextInput = styled.input`
    height: 16px;
    line-height: 16px;
    font-size: 14px;
    border: none;
    background: none;
    outline: none;
    user-select: none;
    color: white;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
    padding: 0;

    &:-internal-autofill-selected {
        background: none !important;
        color: white !important;
    }
`

const ItemsListContainer = styled.div`
    position: absolute;
    display: flex;
    flex-direction: column;
    top: 100%;
    left: 0;
    background: #303030;
    border: 1px solid #808080;
    height: max-content;
    max-height: 256px;
    width: calc(100% - 2px);
    border-radius: 8px;
    overflow-x: hidden;
    overflow-y: auto;
    margin-top: 8px;
    z-index: 50;
    
    & > div {
        padding: 6px 8px;
        width: calc(100% - 8px);
        height: 18px;
        font-size: 14px;
        line-height: 18px;
        cursor: pointer;
        background: none;
        border: none;
    }
    
    & > div:hover {
        background: #505050;
    }
`

export function ItemSelectionInput(props) {

    const [s_inputText, setInputText] = useState('');

    const [s_itemsListShown, setItemsListShown] = useState(false);

    const m_availableOptions = useMemo(() => {
        return (props.optionsList || []).filter(item => !(props.selectedItems || []).includes(item))
    }, [props.optionsList, props.selectedItems])

    const c_addItem = useCallback((item) => {
        if (!m_availableOptions.includes(item)) return;
        props.setSelectedItems([...props.selectedItems, item]);
        setInputText('');
    }, [m_availableOptions, props.setSelectedItems, props.selectedItems])

    const c_removeItem = useCallback((item) => {
        if (!props.selectedItems.includes(item)) return;
        props.setSelectedItems(props.selectedItems.filter(itm => itm !== item));
    }, [props.setSelectedItems, props.selectedItems])

    const m_availableOptionsFilteredByInput = useMemo(() => {
        if (!s_inputText) return m_availableOptions;
        return m_availableOptions.filter((option) => option.toLowerCase().includes(s_inputText.toLowerCase()));
    }, [m_availableOptions, s_inputText])

    const m_itemsList = useMemo(() => {
        return m_availableOptionsFilteredByInput.map((optionName, index) => <>
            <div
                key={`selectableitem-${index}`}
                onClick={() => c_addItem(optionName)}
            >{optionName}</div>
        </>)
    }, [m_availableOptionsFilteredByInput, c_addItem]);

    const m_selectedItemsList = useMemo(() => {
        return (props.selectedItems || []).map((itemName, index) => <>
            <ItemSelectionItem
                key={`selecteditem-${index}`}
            >
                {itemName}
                <button onClick={() => c_removeItem(itemName)}>
                    <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.crossMark}/></svg>
                </button>
            </ItemSelectionItem>
        </>)
    }, [props.selectedItems, c_removeItem, s_inputText])

    return <>
        <FormContainer
            containerwidth={props.containerWidth}
            containermargin={props.containerMargin}
        >
            {props.label && <>
                <Label height="2em">{props.label}</Label>
                <VerticalGap gap="0.2em"/>
            </>}
            {props.subLabel && <>
                <SubLabel height="1em">{props.subLabel}</SubLabel>
                <VerticalGap gap="0.8em"/>
            </>}
            <ItemSelectionContainer>
                <ItemSelectionShowListButton onClick={() => setItemsListShown(p => !p)}>
                    <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.arrowDown}/></svg>
                </ItemSelectionShowListButton>
                <ItemSelectionItemsArea>
                    {m_selectedItemsList}
                    <ItemSelectionTextInput
                        type={'text'}
                        placeholder={''}
                        value={s_inputText}
                        onChange={e => {
                            e.preventDefault();
                            e.stopPropagation();
                            setInputText(e.target.value);
                        }}
                        onKeyDown={e => {
                            if (e.key === "Enter") {
                                s_inputText &&
                                m_availableOptionsFilteredByInput &&
                                c_addItem(m_availableOptionsFilteredByInput[0])
                                return;
                            }
                            if (e.key === 'Backspace') {
                                !s_inputText &&
                                props.selectedItems &&
                                c_removeItem(props.selectedItems[props.selectedItems.length - 1])
                                return;
                            }
                            if (e.key === 'Escape') {
                                setItemsListShown(false);
                                return;
                            }
                        }}
                    />
                </ItemSelectionItemsArea>
                {(s_inputText || s_itemsListShown) && m_itemsList.length ? <>
                    <ItemsListContainer>
                        {m_itemsList}
                    </ItemsListContainer>
                </> : <></>}
            </ItemSelectionContainer>
        </FormContainer>
    </>
}