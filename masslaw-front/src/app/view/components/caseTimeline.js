import React, {useEffect, useMemo, useState} from "react";
import styled from "styled-components";
import {VerticalGap} from "./verticalGap";
import {unixTimeToDayDateString} from "../../controller/functionality/time-utils/dateTimeUtils";

const MAX_TIME = 2524608000000;
const MIN_TIME = -2208988800000;

const Timeline = styled.div`
    width: calc(100% - 64px);
    height: max-content;
    padding: 32px;
    font-size: ${({zoom}) => zoom}px;
`

const TimelineEventElement = styled.div`
    background: white;
    padding: 8px;
    border-radius: 8px;
    font-size: 14px;
    color: black;
`

export const CaseTimeline = function (props) {

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
        eventsAndTimes.sort((a, b) => b[1] - a[1]);
        let MAX_GAP = NaN;
        let MIN_GAP = NaN;
        for (let idx = 1; idx < eventsAndTimes.length; idx++) {
            const event1 = eventsAndTimes[idx-1];
            const event2 = eventsAndTimes[idx];
            const event1time = event1[1];
            const event2time = event2[1];
            const eventGap = event2time - event1time;
            if (Number.isNaN(MAX_GAP) || eventGap > MAX_GAP) MAX_GAP = eventGap;
            if (Number.isNaN(MIN_GAP) || eventGap > MIN_GAP) MIN_GAP = eventGap;
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
            eventElements.push(<VerticalGap gap={`${eventGapRatio}em`} />)
            eventElements.push(<EventElement event={event2[0]} />)
        }
        return eventElements;
    }, [props.events]);

    const [s_zoom, setZoom] = useState(24);

    return <>
        <Timeline zoom={s_zoom}>
            {m_events}
        </Timeline>
    </>
}


function EventElement(props) {
    return <>
        <TimelineEventElement>
            {unixTimeToDayDateString(props.event.date.getTime() / 1000)}
        </TimelineEventElement>
    </>
}
