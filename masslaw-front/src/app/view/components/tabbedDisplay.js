import styled from "styled-components";
import {useEffect, useMemo, useState} from "react";

const TabbedDisplayContainer = styled.div`
    position: relative;
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    overflow: hidden;
`

const TabbedDisplayTabsSection = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    width: 100%;
    height: 48px;
    min-height: 48px;
    border-bottom: 1px solid #606060;
    overflow-x: auto;
    overflow-y: hidden;
    -ms-overflow-style: none;
    scrollbar-width: none;
    &::-webkit-scrollbar { display: none; }
`

const TabbedDisplayTab = styled.button`
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    padding: 0 32px;
    margin: 0;
    height: 100%;
    color: white;
    background: none;
    border: 0 solid transparent;
    border-bottom: 3px solid ${({selected}) => selected ? 'white' : 'transparent'};
    cursor: pointer;
    user-select: none;
    font-size: 16px;
    &:hover {
        background: #505050;
    }
`

const TabbedDisplayTabContentContainer = styled.div`
    position: relative;
    margin: 0;
    padding: 0;
    width: 100%;
    flex-grow: 1;
    flex-shrink: 0;
    flex-basis: 0;
    overflow: auto;
`

export function TabbedDisplay(props) {

    const [s_selectedTab, setSelectedTab] = useState('');

    const m_tabs = useMemo(() => {
        return Object.keys(props.tabs || {}).map((tabName) => {
            return <TabbedDisplayTab key={tabName} selected={s_selectedTab === tabName} onClick={() => setSelectedTab(tabName)}>{tabName}</TabbedDisplayTab>
        });
    }, [props.tabs, s_selectedTab]);

    useEffect(() => {
        if (!s_selectedTab && props.tabs) setSelectedTab(Object.keys(props.tabs)[0]);
    }, [props.tabs, s_selectedTab]);

    useEffect(() => {
        setSelectedTab(props.selectedTab);
    }, [props.selectedTab]);

    return <>
        <TabbedDisplayContainer>
            <TabbedDisplayTabsSection>{m_tabs}</TabbedDisplayTabsSection>
            <TabbedDisplayTabContentContainer>{props.tabs[s_selectedTab]}</TabbedDisplayTabContentContainer>
        </TabbedDisplayContainer>
    </>
}