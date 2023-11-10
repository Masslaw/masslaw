export function parseColor(colorString: string): { r: number, g: number, b: number } {
    const r = parseInt(colorString.slice(2, 4), 16);
    const g = parseInt(colorString.slice(4, 6), 16);
    const b = parseInt(colorString.slice(6, 8), 16);
    return { r, g, b };
}

export function rgbToHex(color: { r: number, g: number, b: number }) {
    const componentToHex = (c: number) => {
        const hex = c.toString(16);
        return hex.length === 1 ? "0" + hex : hex;
    };
    return "#" + componentToHex(color.r) + componentToHex(color.g) + componentToHex(color.b);
}