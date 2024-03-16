import {Color} from "./color";


const _cachedColors = {};
export function stringToColor(str) {
    if (_cachedColors[str]) return _cachedColors[str];
    const color = new Color();
    color.fromString(str);
    _cachedColors[str] = color;
    return color;
}

export function setColorSV(color, s=null, v=null) {
    const hsv = color.getHSV();
    hsv.s = s != null && s || hsv.s;
    hsv.v = v != null && v || hsv.v;
    color.setHSV(hsv.h, hsv.s, hsv.v);
    return color;
}
