import styled from "styled-components";
import {useState} from "react";
import {SVG_PATHS} from "../config/svgPaths";

const MeatballsMenuButton = styled.div`
    position: relative;
    width: ${({width}) => width || '100%'};
    height: ${({height}) => height || '100%'};
    cursor: pointer;
    pointer-events: all;
    svg {
        width: 100%;
        height: 100%;
        fill: ${({fill}) => fill || 'black'};
    }
    &:hover svg {
        fill: ${({hoverFill}) => hoverFill || '#707070'};
    }
`;

const MeatballsMenuMenu = styled.div`
    position: absolute;
    display: flex;
    flex-direction: column;
    border-radius: 4px;
    padding: 4px;
    background-color: #303030;
    pointer-events: all;
    z-index: 100;
    ${({position}) => position || 'top: 0; left: 0; transform: translate(-100%, 0)'};
    width: ${({width}) => width || '64px'};
`

const MeatballsMenuItem = styled.button`
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 2px;
    width: calc(100%);
    font-size: 12px;
    color: white;
    background: #303030;
    border: none;
    pointer-events: all;
    &:hover {
        background: #454545;
    }
`

export function MeatballsMenu(props) {

    const [s_open, setOpen] = useState(false);

    return <>
        <MeatballsMenuButton onClick={() => setOpen(o=>!o)}>
            <svg viewBox={'0 0 1000 1000'}><path d={SVG_PATHS.meatballs}/></svg>
            {s_open && <MeatballsMenuMenu
                position={props.menuPosition}
                width={props.menuWidth}
            >
                {props.items.map((item, index) => <MeatballsMenuItem
                    key={index}
                    onClick={() => {item.onClick(); setOpen(false)}}>
                    {item.label}
                </MeatballsMenuItem>)}
            </MeatballsMenuMenu>}
        </MeatballsMenuButton>
    </>
}