import React, {useEffect, useRef, useState} from "react";
import "./css.css";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faAngleDown, faAngleUp, faMinus} from "@fortawesome/free-solid-svg-icons";

export function DataTable(props: {
    data: { [key: string]: any }[];
    keys: [string, string][];
    elementDisplayMap?: { [key: string]: (arg: any) => JSX.Element },
    onItemClicked?: (item_data: any) => void;
}) {
    const tableContainerRef = useRef<HTMLDivElement>(null);
    const tableRef = useRef<HTMLTableElement>(null);

    const [display_data, setDisplayData] = useState(props.data);

    const [order_column, setOrderColumn] = useState(props.keys[0][0] || "");
    const [order_direction, setOrderDirection] = useState("down");

    const [columnWidths, setColumnWidths] = useState<number[]>([]);

    const onColumnSortButtonClicked = (columnName: string) => {
        if (order_column === columnName) {
            setOrderDirection(order_direction === "down" ? "up" : "down");
        } else {
            setOrderColumn(columnName);
            setOrderDirection("down");
        }
    };

    const getMaxColumnItemsWidth = (columnIndex: number, tableRef: React.RefObject<HTMLTableElement>) => {
        if (!tableRef.current) return;

        const th = tableRef.current.querySelector(`th:nth-child(${columnIndex + 1})`);
        const tds = tableRef.current.querySelectorAll(`td:nth-child(${columnIndex + 1})`);

        if (!th) return;

        let maxColumnWidth = th.getBoundingClientRect().width;

        tds.forEach((td) => {
            const tdWidth = td.getBoundingClientRect().width;
            maxColumnWidth = Math.max(maxColumnWidth, tdWidth);
        });

        return maxColumnWidth;
    }

    useEffect(() => {
        const handleResize = () => {
            let totalWidths = 0;
            let widths: number[] = [];
            props.keys.forEach((_, index) => {
                const width = getMaxColumnItemsWidth(index, tableRef) || 300;
                widths[index] = width;
                totalWidths += width;
            });

            const tableWidth = tableContainerRef.current?.getBoundingClientRect().width || 0;

            if (totalWidths < tableWidth) {
                const ratio = tableWidth / totalWidths;
                widths = widths.map((width) => width * ratio);
            }
            setColumnWidths(widths);
        };

        handleResize();

        window.addEventListener('resize', handleResize);

        return () => window.removeEventListener('resize', handleResize);
    }, [props.keys]);

    useEffect(() => {
        const sorted = [...props.data].sort((a, b) => {
            let valueA = a[order_column];
            try {
                valueA = JSON.stringify(valueA);
            } catch (e) {
                valueA = `${valueA}`;
            }
            let valueB = b[order_column];
            try {
                valueB = JSON.stringify(valueB);
            } catch (e) {
                valueB = `${valueB}`;
            }

            if (valueA < valueB) {
                return order_direction === "down" ? -1 : 1;
            }
            if (valueA > valueB) {
                return order_direction === "down" ? 1 : -1;
            }
            return 0;
        });
        setDisplayData(sorted);
    }, [order_column, order_direction, props.data]);

    return (<>
            <div className={"data-table-container"} ref={tableContainerRef}>
                <table className={"data-table"} ref={tableRef}>
                    <thead>
                    <tr>
                        {props.keys.map((key, index) => {
                            return (<th key={index + Math.random()} style={{width: `${columnWidths[index]}px`}}>
                                    <div
                                        className={`${key[0]} table-column-header-container`}
                                        onClick={(e) => {
                                            onColumnSortButtonClicked(key[0]);
                                        }}
                                    >
                                        <div className={`${key[0]} table-column-header-title`}>
                                            {key[1]}
                                        </div>
                                        <div
                                            className={`${key[0]} table-column-header-sorting-arrow`}
                                        >
                                            {order_column === key[0] ? (<FontAwesomeIcon
                                                icon={order_direction === "down" ? faAngleDown : faAngleUp}
                                            />) : (<FontAwesomeIcon icon={faMinus}/>)}
                                        </div>
                                    </div>
                                </th>);
                        })}
                    </tr>
                    <tr className={"data-table-head-border"}/>
                    <tr className={"table-head-bg"}/>
                    </thead>
                    <tbody>
                        {display_data.map((item, index) => (
                        <tr key={index + Math.random()}>
                            {
                                props.keys.map((key, keyIndex) => {
                                    const itemContent = (props.elementDisplayMap && props.elementDisplayMap[key[0]] && props.elementDisplayMap[key[0]](item[key[0]])) || (<>{`${item[key[0]]}`}</>);
                                    return (
                                        <td key={key[0]} style={{width: `${columnWidths[keyIndex]}px`}}>
                                            <div className={`${key[0]} table-column-content-container`}>
                                                <div className={`${key[0]} table-item-content`}>
                                                    {(props.elementDisplayMap && props.elementDisplayMap.hasOwnProperty(key[0])) ? props.elementDisplayMap[key[0]](item[key[0]]) : <>{itemContent}</>}
                                                </div>
                                            </div>
                                        </td>
                                    );
                                })
                            }
                            <td
                                className={'data-table-row-bounding-rect-layer'}
                                onClick={() => { if (props.onItemClicked) props.onItemClicked(item) }}
                            />
                        </tr>))}
                    </tbody>
                </table>
            </div>
        </>);
}