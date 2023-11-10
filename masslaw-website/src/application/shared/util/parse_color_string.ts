export function parseColor(colorString: string): { r: number, g: number, b: number } {
    colorString.replace('#', '');
    const r = parseInt(colorString.slice(1, 3), 16);
    const g = parseInt(colorString.slice(3, 5), 16);
    const b = parseInt(colorString.slice(5, 7), 16);
    return { r, g, b };
}

export function rgbToHex(color: { r: number, g: number, b: number }) {
    const componentToHex = (c: number) => {
        const hex = c.toString(16);
        return hex.length === 1 ? "0" + hex : hex;
    };
    return "#" + componentToHex(color.r) + componentToHex(color.g) + componentToHex(color.b);
}