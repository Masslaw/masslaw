import React, {useEffect, useState} from "react";

import './css.css';


export const Timeline = function (props: {
    events: {
        [event_id: string]: {
            title: string, onclick: () => void, date: Date,
        }
    },
}) {

    const [event_display_positions, setEventDisplayPositions] = useState({} as { [event_id: string]: [number, number] });

    const [hovered_event_id, setHoveredEventId] = useState('');

    useEffect(() => {
        let min_date = NaN;
        let max_date = NaN;
        for (let event_id in props.events) {
            const event = props.events[event_id];
            if (!event) continue;
            if (event.date.getTime() > 2524608000000 || event.date.getTime() < -2208988800000) {
                delete props.events[event_id];
                continue
            }
            if (Number.isNaN(min_date) || event.date.getTime() < min_date) min_date = event.date.getTime();
            if (Number.isNaN(max_date) || event.date.getTime() > max_date) max_date = event.date.getTime();
        }
        let date_range = max_date - min_date;

        let occupied_title_ranges_by_row: number[] = [];
        let event_display_positions = {} as { [event_id: string]: [number, number] };
        for (let event_id of Object.keys(props.events).sort((a, b) => props.events[a].date.getTime() - props.events[b].date.getTime())) {
            const event = props.events[event_id];
            if (!event) continue;
            const event_date = event.date.getTime();
            if (Number.isNaN(event_date)) continue;
            const event_x = (event_date - min_date) / date_range * 700 + 50;
            let row_number = 0;
            for (let occupied_title_range of occupied_title_ranges_by_row) {
                if (event_x > occupied_title_range) break;
                row_number++;
            }
            occupied_title_ranges_by_row[row_number] = event_x + 200;
            let event_y = 100 + (30 * row_number);
            event_display_positions[event_id] = [event_x, event_y];
        }
        setEventDisplayPositions(event_display_positions);
    }, [props.events]);

    return <>
        <svg
            className="timeline"
            viewBox={`0 0 1000 ${Math.max(...Object.values(event_display_positions).map((position) => position[1])) + 100}`}
        >
            <line x1="20" y1="20" x2="980" y2="20" stroke="var(--masslaw-primary-main)" strokeWidth="1" />
            <polygon points="990,20 980,15 980,25" fill="var(--masslaw-primary-main)" />
            <circle cx="15" cy="20" r="1" fill="var(--masslaw-primary-main)" />
            <circle cx="10" cy="20" r="1" fill="var(--masslaw-primary-main)" />
            {Object.keys(props.events)
                .sort((a, b) => (event_display_positions[a] || [0])[0] - (event_display_positions[b] || [0])[0])
                .map((event_id, index) => {
                    if (!event_display_positions[event_id]) return <></>;
                    const display_x = event_display_positions[event_id][0];
                    const display_y = event_display_positions[event_id][1];
                    return <>
                        <line
                            key={index}
                            x1={display_x}
                            y1="20"
                            x2={display_x}
                            y2={display_y}
                            stroke="grey"
                            strokeWidth="1"
                        />
                        <circle
                            key={index}
                            cx={display_x}
                            cy="20"
                            r={hovered_event_id === event_id ? '10' : '5'}
                            fill="white"
                            stroke="var(--masslaw-primary-main)"
                            style={{'cursor': 'pointer'}}
                            onMouseEnter={(e) => setHoveredEventId(event_id)}
                            onMouseLeave={(e) => setHoveredEventId('')}
                        />
                    </>
                })
            }
            {Object.keys(props.events)
                .sort((a, b) =>  (event_display_positions[a] || [0])[0] - (event_display_positions[b] || [0])[0])
                .map((event_id, index) => {
                    if (!event_display_positions[event_id]) return <></>;
                    const display_x = event_display_positions[event_id][0];
                    const display_y = event_display_positions[event_id][1];
                    return <>
                        <rect
                            key={index}
                            x={display_x}
                            y={display_y - (hovered_event_id === event_id ? 10 : 7.5)}
                            width="200"
                            height={hovered_event_id === event_id ? '30' : '25'}
                            rx={"5"}
                            fill={hovered_event_id === event_id ? '#e8e8e8' : 'white'}
                            stroke="var(--masslaw-primary-main)"
                            style={{'cursor': 'pointer'}}
                            onClick={props.events[event_id].onclick}
                            onMouseEnter={(e) => setHoveredEventId(event_id)}
                            onMouseLeave={(e) => setHoveredEventId('')}
                        />
                        <text
                            key={index}
                            x={display_x + 5}
                            y={(display_y + 11)}
                            textAnchor="topLeft"
                            style={{'cursor': 'pointer'}}
                            onClick={props.events[event_id].onclick}
                            onMouseEnter={(e) => setHoveredEventId(event_id)}
                            onMouseLeave={(e) => setHoveredEventId('')}
                        >{props.events[event_id].date.toLocaleString()}</text>
                    </>
                })
            }
        </svg>
    </>
}
