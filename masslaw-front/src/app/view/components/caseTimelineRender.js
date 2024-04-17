import React, {useMemo, useState} from "react";
import styled from "styled-components";
import {VerticalGap} from "./verticalGap";
import {formatDateToDayDateString, formatDateToTimeString, unixTimeToDayDateString} from "../../controller/functionality/time-utils/dateTimeUtils";

const MAX_TIME = 2524608000000;
const MIN_TIME = -2208988800000;

const Timeline = styled.div`
    position: relative;
    width: max-content;
    height: max-content;
    min-height: 100%;
    overflow-x: visible;
`

const TimelineVisualLine = styled.div`
    position: absolute;
    width: 2px;
    height: 100%;
    background: #b0b0b0;
    top: 0;
    left: calc(6px - 1px + 8px);
`

const TimelineEventElement = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    font-size: 16px;
    font-weight: bold;
    color: white;
    margin-left: 8px;

    & > span:nth-child(1) {
        margin-right: 8px;
        width: 12px;
        height: 12px;
        border-radius: 6px;
        background: white;
        filter: drop-shadow(0 0 4px white);
    }

    & > span:nth-child(2) {
        padding: 8px;
        background: none;
        border-radius: 8px;
        cursor: pointer;
        background: ${({highlighted}) => highlighted ? '#303030' : 'none'};
        > span:nth-child(2) {
            font-size: 14px;
            font-weight: normal;
            color: #808080;
            margin-left: 8px;
        }
    }
    
    & > span:nth-child(2):hover {
        background: #353535;
    }
`

export const CaseTimelineRender = function (props) {

    const [s_gapMultiplier, setGapMultiplier] = useState(256);

    const m_events = useMemo(() => {
        const eventsAndTimes = [];
        for (let eventId in props.events) {
            const event = props.events[eventId];
            if (!event) continue;
            const eventTime = event.date.getTime();
            if (Number.isNaN(eventTime)) continue;
            if (eventTime > MAX_TIME || eventTime < MIN_TIME) continue;
            eventsAndTimes.push([event, eventTime]);
        }
        if (!eventsAndTimes.length) return <></>;
        eventsAndTimes.sort((a, b) => a[1] - b[1]);
        const gaps = [];
        for (let idx = 1; idx < eventsAndTimes.length; idx++) {
            const event1 = eventsAndTimes[idx - 1];
            const event2 = eventsAndTimes[idx];
            const event1time = event1[1];
            const event2time = event2[1];
            const eventGap = event2time - event1time;
            gaps.push(eventGap);
        }
        const gapSum = gaps.reduce((a, b) => a + b, 0);
        const gapMean = gapSum / gaps.length;
        const MAX_GAP = gaps.reduce((a, b) => Math.max(a, b), gaps[0]);
        const MIN_GAP = gaps.reduce((a, b) => Math.min(a, b), gaps[0]);
        const gapMeanRatio = (gapMean - MIN_GAP) / (MAX_GAP - MIN_GAP);
        const eventElements = [];
        eventElements.push(<VerticalGap key={`g-${0}`} gap={`64px`}/>);
        eventElements.push(<EventElement key={`evt-${0}`} event={eventsAndTimes[0][0]}/>);
        for (let idx = 0; idx < gaps.length; idx++) {
            const eventGap = gaps[idx];
            const eventGapRatio = (eventGap - MIN_GAP) / (MAX_GAP - MIN_GAP);
            const distanceFromMean = gapMeanRatio - eventGapRatio;
            const gapMultiplier = Math.exp(distanceFromMean);
            eventElements.push(<VerticalGap key={`g-${idx}`} gap={`16px`}/>)
            eventElements.push(<VerticalGap key={`dg-${idx+1}`} gap={`${gapMultiplier * Math.sqrt(eventGapRatio) * s_gapMultiplier}px`}/>)
            eventElements.push(<EventElement key={`evt-${idx+1}`} event={eventsAndTimes[idx+1][0]}/>)
        }
        eventElements.push(<VerticalGap key={`g--1`} gap={`64px`}/>);
        return eventElements;
    }, [props.events, s_gapMultiplier]);

    return <>
        <Timeline>
            <TimelineVisualLine/>
            {m_events}
        </Timeline>
    </>
}


function EventElement(props) {
    const m_dateString = useMemo(() => {
        return formatDateToDayDateString(props.event.date);
    }, [props.event]);
    const m_timeString = useMemo(() => {
        if (props.event.dateData.hasOwnProperty('h')) return ` ${formatDateToTimeString(props.event.date)}`;
        return '';
    }, [props.event]);
    return <>
        <TimelineEventElement
            highlighted={props.event.highlighted}
            onClick={props.event.onClick}
        >
            <span/>
            <span>
                <span>{m_dateString}</span>
                <span>{m_timeString}</span>
            </span>
        </TimelineEventElement>
    </>
}
