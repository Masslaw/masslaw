import React, {useEffect, useMemo, useState} from "react";
import styled from "styled-components";
import {VerticalGap} from "./verticalGap";
import {unixTimeToDayDateString} from "../../controller/functionality/time-utils/dateTimeUtils";

const MAX_TIME = 2524608000000;
const MIN_TIME = -2208988800000;

const Timeline = styled.div`
    position: relative;
    width: calc(100% - 64px);
    height: calc(100% - 64px);
    padding: 32px;
    background: #202020;
`

const TimelineVisualLine = styled.div`
    position: absolute;
    width: 2px;
    height: 100%;
    background: #b0b0b0;
    top: 0;
    left: 37px;
`

const TimelineEventElement = styled.div`
    position: relative;
    display: flex;
    flex-direction: row;
    align-items: center;
    font-size: 16px;
    font-weight: bold;
    color: white;
    span:nth-child(1) {
        margin-right: 8px;
        width: 12px;
        height: 12px;
        border-radius: 6px;
        background: white;
        filter: drop-shadow(0 0 4px white);
    }
    span:nth-child(2) {
        padding: 8px;
        background: none;
        border-radius: 8px;
        cursor: pointer;
    }
    span:nth-child(2):hover {
        background: #303030;
    }
`

const TimelineEventInformationContainer = styled.div`
    position: absolute;
    display: flex;
    flex-direction: column;
    background: #303030;
    border-radius: 8px;
`

export const CaseTimelineRender = function (props) {

    const [s_gapMultiplier, setGapMultiplier] = useState(64);

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
        let MAX_GAP = NaN;
        let MIN_GAP = NaN;
        for (let idx = 1; idx < eventsAndTimes.length; idx++) {
            const event1 = eventsAndTimes[idx-1];
            const event2 = eventsAndTimes[idx];
            const event1time = event1[1];
            const event2time = event2[1];
            const eventGap = event2time - event1time;
            if (Number.isNaN(MAX_GAP) || eventGap > MAX_GAP) MAX_GAP = eventGap;
            if (Number.isNaN(MIN_GAP) || eventGap < MIN_GAP) MIN_GAP = eventGap;
        }
        const eventElements = [];
        eventElements.push(<EventElement event={eventsAndTimes[0][0]} />)
        for (let idx = 1; idx < eventsAndTimes.length; idx++) {
            const event1 = eventsAndTimes[idx-1];
            const event2 = eventsAndTimes[idx];
            const event1time = event1[1];
            const event2time = event2[1];
            const eventGap = event2time - event1time;
            const eventGapRatio = (eventGap - MIN_GAP) / (MAX_GAP - MIN_GAP);
            eventElements.push(<VerticalGap gap={`${eventGapRatio * s_gapMultiplier}px`} />)
            eventElements.push(<EventElement event={event2[0]} />)
        }
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
    return <>
        <TimelineEventElement>
            <span />
            <span>{unixTimeToDayDateString(props.event.date.getTime() / 1000)}</span>
        </TimelineEventElement>
    </>
}
