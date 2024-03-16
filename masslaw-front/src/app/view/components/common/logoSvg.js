import {SVG_PATHS} from "../../config/svgPaths";

export function LogoSvg() {
    return <svg viewBox={"0 -346.4 2000 2000"}>
        <path d={SVG_PATHS.logoTop}/>
        <path d={SVG_PATHS.logoRight}/>
        <path d={SVG_PATHS.logoLeft}/>
        <path d={SVG_PATHS.logoBottom}/>
    </svg>
}