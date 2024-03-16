export class Color {
    constructor(r = 255, g = 255, b = 255, a = 1) {
        this.setRGBA(r, g, b, a);
    }

    setHex(hex) {
        if (hex.startsWith('#')) hex = hex.slice(1);
        const bigint = parseInt(hex, 16);
        this.r = (bigint >> 16) & 255;
        this.g = (bigint >> 8) & 255;
        this.b = bigint & 255;
        this.a = 1;
    }

    getHex() {
        return `#${((1 << 24) + (this.r << 16) + (this.g << 8) + this.b).toString(16).slice(1)}`;
    }

    setRGB(r, g, b) {
        this.r = r;
        this.g = g;
        this.b = b;
        this.a = 1;
    }

    getRGB() {
        return `rgb(${this.r}, ${this.g}, ${this.b})`;
    }

    setRGBA(r, g, b, a) {
        this.r = r;
        this.g = g;
        this.b = b;
        this.a = a;
    }

    getRGBA() {
        return `rgba(${this.r}, ${this.g}, ${this.b}, ${this.a})`;
    }

    setHSV(h, s, v) {
        let r, g, b, i, f, p, q, t;
        h = h / 360;
        i = Math.floor(h * 6);
        f = h * 6 - i;
        p = v * (1 - s);
        q = v * (1 - f * s);
        t = v * (1 - (1 - f) * s);
        switch (i % 6) {
            case 0:
                r = v;
                g = t;
                b = p;
                break;
            case 1:
                r = q;
                g = v;
                b = p;
                break;
            case 2:
                r = p;
                g = v;
                b = t;
                break;
            case 3:
                r = p;
                g = q;
                b = v;
                break;
            case 4:
                r = t;
                g = p;
                b = v;
                break;
            case 5:
                r = v;
                g = p;
                b = q;
                break;
        }
        this.setRGBA(Math.round(r * 255), Math.round(g * 255), Math.round(b * 255), this.a);
    }

    getHSV() {
        let r = this.r / 255;
        let g = this.g / 255;
        let b = this.b / 255;
        let max = Math.max(r, g, b), min = Math.min(r, g, b);
        let h, s, v = max;
        let d = max - min;
        s = max === 0 ? 0 : d / max;
        if (max === min) {
            h = 0;
        } else {
            switch (max) {
                case r:
                    h = (g - b) / d + (g < b ? 6 : 0);
                    break;
                case g:
                    h = (b - r) / d + 2;
                    break;
                case b:
                    h = (r - g) / d + 4;
                    break;
            }
            h /= 6;
        }
        return {h: Math.round(h * 360), s: s, v: v};
    }
    fromString(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) hash = str.charCodeAt(i) + (hash << 6) + (hash << 16) - hash;
        hash = hash & hash;
        this.r = Math.abs((hash & 0xFF0000) >> 16);
        this.g = Math.abs((hash & 0x00FF00) >> 8);
        this.b = Math.abs(hash & 0x0000FF);
        this.a = 1;
    }
}
