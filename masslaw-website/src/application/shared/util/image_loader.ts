export class ImageLoader {
    private static _instance = new ImageLoader();

    public static getInstance() {
        return this._instance;
    }

    constructor() {
        if (ImageLoader._instance) {
            throw new Error("Cannot create a new instance of a manager class. Please use getInstance() instead.");
        }
    }

    private cachedImages = {} as { [key: string]: HTMLImageElement };

    public async _getImageFromData(imageData: {format: string, data: string}, reload?: boolean): Promise<HTMLImageElement> {
        let _image = this.cachedImages[imageData.data]

        if (reload || !_image) {
            return new Promise((resolve, reject) => {
                _image = new Image();
                _image.onload = () => resolve(_image);
                _image.onerror = reject;
                _image.src = `data:image/${imageData.format};base64,${imageData.data}`;
                this.cachedImages[imageData.data] = _image;
            });
        }

        return _image;
    }

    public async _getImageFromUrl(url: string, reload?: boolean): Promise<HTMLImageElement> {
        let _image = this.cachedImages[url]

        if (reload || !_image) {
            return new Promise((resolve, reject) => {
                _image = new Image();
                _image.onload = () => resolve(_image);
                _image.onerror = reject;
                _image.src = url;
                this.cachedImages[url] = _image;
            });
        }

        return _image;
    }

    public _uncacheImage(imageData: {format: string, data: string}) {
        delete this.cachedImages[imageData.data];
    }

    public _uncacheImages() {
        for (const key of Object.keys(this.cachedImages)) delete this.cachedImages[key];
    }

}