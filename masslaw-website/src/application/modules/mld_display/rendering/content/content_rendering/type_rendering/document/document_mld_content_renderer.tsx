import React from "react";
import {DocumentMLDContent} from "../../../../../config/mld_structure";

const documentContentDisplaySettings = {
    backgroundColor: '#343434',
    pageGap: 20,
    contentPadding: 15,
    zoomSensitivity: 0.96,
    scrollSensitivity: {
        horizontal: 40,
        vertical: 80,
    },
    scrollFriction: 1000,
};

export class DocumentMLDContentRenderer extends React.Component<DocumentMLDContentRendererProps, DocumentMLDContentRendererState> {

    private readonly canvasRef: React.RefObject<HTMLCanvasElement>;
    private canvasInstance?: HTMLCanvasElement | null;
    private canvasContext?: CanvasRenderingContext2D | null;

    private renderingValues = {
        documentSize: {
            x: 0,
            y: 0
        },
        canvasSize: {
            x: 0,
            y: 0
        },
        scrollMomentum: {
            x: 0,
            y: 0,
        },
        displayZoom: 1,
        previousUpdate: performance.now(),
        loadedImages: {} as { [key: string]: HTMLImageElement },
    }

    private flags = {
        recordScrollForMomentum: false,
        applyScrollMomentum: false,
        draggingDisplay: false,
    };

    private displayTransform = {
        edit: {
            scale: 1,
            translate: {
                x: 0,
                y: 0,
            }
        },
        current: {
            scale: 1,
            translate: {
                x: 0,
                y: 0,
            }
        },
        previous: {
            scale: 1,
            translate: {
                x: 0,
                y: 0,
            }
        }
    };

    private inputValues = {
        mouse: {
            buttons: {
                left: 0,
                middle: 0,
                right: 0,
            },
            position: {
                current: {
                    x: 0,
                    y: 0,
                },
                previous: {
                    x: 0,
                    y: 0,
                },
            },
            wheelDelta: {
                new: {
                    x: 0,
                    y: 0,
                },
                current: {
                    x: 0,
                    y: 0,
                },
            }
        },
        keyboard: {
            keysDown: {} as { [key: string]: boolean },
        }
    }

    private currentSelection = {
        from: {
            page: -1,
            line: -1,
            word: -1,
            character: -1,
        },
        to: {
            page: -1,
            line: -1,
            word: -1,
            character: -1,
        },
        active: false,
    }

    constructor(props: DocumentMLDContentRendererProps) {
        super(props);
        this.state = {
            displayZoom: 1,
        } as DocumentMLDContentRendererState;

        this.canvasRef = React.createRef();
    }

    public render = () : JSX.Element => {
        return <this._renderInternal />
    }

    private _renderInternal = () :JSX.Element => {
        return (
            <>
                <canvas className={'mlc-content-renderer-canvas'} ref={this.canvasRef}/>
            </>
        )
    }

    public componentDidMount = (): void => {
        this._initiateInputListeners();
        this._handleCanvasRef();

        this.renderingValues.previousUpdate = performance.now();
        requestAnimationFrame(this._frame);

        this._refreshCanvas();
        this._setZoom(1);
    }

    public componentWillUnmount() {
        this._releaseInputListeners();
    }

    private _frame = () => {
        const currentTime = performance.now();
        const deltaTime = (currentTime - this.renderingValues.previousUpdate) / 1000;
        this.renderingValues.previousUpdate = performance.now();

        this._updateInputHandlers();

        this._applyScrollMomentum(deltaTime);

        this._updateScrollMomentum(deltaTime);

        this._updateDisplayTransform();

        this._refreshCanvas();

        requestAnimationFrame(this._frame);
    }

    private _handleCanvasRef() {
        this.canvasInstance = this.canvasRef.current;
        this.canvasContext = this.canvasInstance?.getContext('2d');
    }

    private _initiateInputListeners() {
        this.canvasInstance = this.canvasRef.current;
        if (this.canvasInstance == null) return;

        this.canvasInstance.addEventListener("mousedown", event => {
            if (event.button === 0) this.inputValues.mouse.buttons.left = 1;
            else if (event.button === 1) this.inputValues.mouse.buttons.middle = 1;
            else if (event.button === 2) this.inputValues.mouse.buttons.right = 1;
        });

        window.addEventListener("mouseup", event => {
            if (event.button === 0) this.inputValues.mouse.buttons.left = 0;
            else if (event.button === 1) this.inputValues.mouse.buttons.middle = 0;
            else if (event.button === 2) this.inputValues.mouse.buttons.right = 0;
        });

        window.addEventListener("keydown", event => {
            this.inputValues.keyboard.keysDown[event.key] = true;
        });

        window.addEventListener("keyup", event => {
            this.inputValues.keyboard.keysDown[event.key] = false;
        });

        this.canvasInstance.addEventListener("contextmenu", event => {
            event.preventDefault();
        });

        this.canvasInstance.addEventListener("wheel", event => {
            this.inputValues.mouse.wheelDelta.new = {
                x: event.deltaX,
                y: event.deltaY,
            };
            event.preventDefault();
        });

        this.canvasInstance.addEventListener("mousemove", event => {
            if (this.canvasInstance == null) return;
            const canvasClientRect = this.canvasInstance.getBoundingClientRect();
            this.inputValues.mouse.position.current = {
                x: event.clientX - canvasClientRect.x,
                y: event.clientY - canvasClientRect.y
            };
        });
    }

    private _releaseInputListeners() {

    }

    private _refreshCanvas = () => {
        this._draw();
    }

    private _draw() {
        this._prepareDisplayData();
        this._prepareCanvas();

        this._drawPages().then();
    }

    private _prepareDisplayData() {
        let maxPageWidth = 0;
        let totalPagesHeight = 0;
        let page_num = 0;
        while (true) {
            const pageData = this.props.renderContent.data.pages[page_num];
            if (!pageData) break;

            maxPageWidth = Math.max(maxPageWidth, pageData.width || 0);
            totalPagesHeight += pageData.height + documentContentDisplaySettings.pageGap;

            page_num += 1
        }
        totalPagesHeight -= documentContentDisplaySettings.pageGap;

        this.renderingValues.documentSize.x = maxPageWidth + (2 * documentContentDisplaySettings.contentPadding);
        this.renderingValues.documentSize.y = totalPagesHeight + (2 * documentContentDisplaySettings.contentPadding);
    }

    private _prepareCanvas() {
        if (this.canvasInstance == null) return;
        if (this.canvasContext == null) return;

        this.renderingValues.canvasSize.x = this.canvasInstance.width = this.canvasInstance.clientWidth;
        this.renderingValues.canvasSize.y = this.canvasInstance.height = this.canvasInstance.clientHeight;

        this.canvasContext.fillStyle = documentContentDisplaySettings.backgroundColor;
        this.canvasContext.fillRect(0, 0, this.canvasInstance.width, this.canvasInstance.height);
    }

    private async _drawPages() {
        if (this.canvasInstance == null) return;
        if (this.canvasContext == null) return;

        const ctx = this.canvasRef.current?.getContext('2d');
        if (ctx == null) return;

        let currentRenderHeight = documentContentDisplaySettings.contentPadding;

        for (let pageNum = 0; pageNum <  this.props.renderContent.data.pages.length; pageNum++) {
            let page = this.props.renderContent.data.pages[pageNum]

            const currentPageLeft = 0.5 * (this.renderingValues.documentSize.x - page.width);

            const pageRectDocumentSpace = {
                x: currentPageLeft,
                y: currentRenderHeight,
                w: page.width,
                h: page.height
            }

            const pageRectCanvasSpace =
                this._documentRectToCanvasRect(
                    this._xywh_to_p1p2(
                        pageRectDocumentSpace));

            if (this._isRectInsideCanvas(pageRectCanvasSpace)) {
                const pageRectCanvasSpaceXYWH = this._p1p2_to_xywh(pageRectCanvasSpace);

                this.canvasContext.fillStyle = 'rgb(255,255,255)';
                this.canvasContext.fillRect(
                    pageRectCanvasSpaceXYWH.x,
                    pageRectCanvasSpaceXYWH.y,
                    pageRectCanvasSpaceXYWH.w,
                    pageRectCanvasSpaceXYWH.h
                );

                const pageBGImageData = page.bg;
                if (pageBGImageData) {
                    let page_image = await this._getImageFromData(pageBGImageData)
                    this.canvasContext.drawImage(
                        page_image,
                        pageRectCanvasSpaceXYWH.x,
                        pageRectCanvasSpaceXYWH.y,
                        pageRectCanvasSpaceXYWH.w,
                        pageRectCanvasSpaceXYWH.h
                    );
                }

                this._setCursor('default', true);

                for (let lineNum = 0; lineNum <  page.lines.length; lineNum++) {
                    let line = page.lines[lineNum]
                    for (let wordNum = 0; wordNum <  line.words.length; wordNum++) {
                        let word = line.words[wordNum]
                        for (let characterNum = 0; characterNum <  word.characters.length; characterNum++) {
                            let character = word.characters[characterNum]

                            const characterRect = {
                                p1: {
                                    x: character.x1 + currentPageLeft,
                                    y: character.y1 + currentRenderHeight,
                                },
                                p2: {
                                    x: character.x2 + currentPageLeft,
                                    y: character.y2 + currentRenderHeight,
                                },
                            };

                            let characterRectCanvasSpace =
                                this._documentRectToCanvasRect(
                                    characterRect);

                            let characterRectCanvasSpaceXYWH = this._p1p2_to_xywh(characterRectCanvasSpace);

                            const mouseOnElement =
                                this.inputValues.mouse.position.current.x >= characterRectCanvasSpace.p1.x &&
                                this.inputValues.mouse.position.current.x <= characterRectCanvasSpace.p2.x &&
                                this.inputValues.mouse.position.current.y >= characterRectCanvasSpace.p1.y &&
                                this.inputValues.mouse.position.current.y <= characterRectCanvasSpace.p2.y;

                            if (mouseOnElement ||
                                (this.currentSelection.active && this.inputValues.mouse.buttons.left > 0)) {
                                this._setCursor('text', true);
                            }

                            const characterPointer = {
                                page: pageNum,
                                line: lineNum,
                                word: wordNum,
                                character: characterNum
                            }

                            if (mouseOnElement && this.inputValues.mouse.buttons.left > 0 && this.currentSelection.active) {
                                this.currentSelection.to = characterPointer;
                            } else if (mouseOnElement && this.inputValues.mouse.buttons.left > 0 && !this.currentSelection.active) {
                                this.currentSelection.from = characterPointer;
                                this.currentSelection.to = characterPointer;
                                this.currentSelection.active = true;
                            }

                            if (this.currentSelection.active &&
                                this._compareCharacterPointers(this.currentSelection.from, characterPointer) < 1 &&
                                this._compareCharacterPointers(this.currentSelection.to, characterPointer) > -1) {

                                this.canvasContext.fillStyle = 'rgba(0,166,255,0.45)';
                                this.canvasContext.fillRect(
                                    characterRectCanvasSpaceXYWH.x,
                                    characterRectCanvasSpaceXYWH.y,
                                    characterRectCanvasSpaceXYWH.w,
                                    characterRectCanvasSpaceXYWH.h
                                );
                            }

                            if (this.inputValues.mouse.buttons.left > 0 && this.inputValues.mouse.buttons.left < 3) {
                                this.currentSelection.active = false;
                            }
                        }
                    }
                }
            }

            currentRenderHeight += page.height + documentContentDisplaySettings.pageGap;
        }
    }

    private async _getImageFromData(imageData: {format: string, data: string}, reload?: boolean): Promise<HTMLImageElement> {
        let _image = this.renderingValues.loadedImages[imageData.data]

        if (reload || !_image) {
            return new Promise((resolve, reject) => {
                _image = new Image();
                _image.onload = () => resolve(_image);
                _image.onerror = reject;
                _image.src = `data:image/${imageData.format};base64,${imageData.data}`;
                this.renderingValues.loadedImages[imageData.data] = _image;
            });
        }

        return _image
    }

    private _updateInputHandlers() {
        this._updateDraggingHandler();
        this._updateMouseWheelHandler();

        this._updateMouseHandler();
    }

    private _updateMouseHandler() {
        if (this.inputValues.mouse.buttons.left > 0) this.inputValues.mouse.buttons.left += 1;
        if (this.inputValues.mouse.buttons.middle > 0) this.inputValues.mouse.buttons.middle += 1;
        if (this.inputValues.mouse.buttons.right > 0) this.inputValues.mouse.buttons.right += 1;
        this.inputValues.mouse.position.previous = {...this.inputValues.mouse.position.current};
        this.inputValues.mouse.wheelDelta.current = {...this.inputValues.mouse.wheelDelta.new};
        this.inputValues.mouse.wheelDelta.new = {x:0,y:0};
    }

    private _updateDraggingHandler() {
        const documentPreviousPosition = this._canvasSpaceToDocumentSpace(this.inputValues.mouse.position.previous);
        const documentCurrentPosition = this._canvasSpaceToDocumentSpace(this.inputValues.mouse.position.current);

        const documentDelta = {
            x: documentCurrentPosition.x - documentPreviousPosition.x,
            y: documentCurrentPosition.y - documentPreviousPosition.y,
        }

        if ((this.inputValues.mouse.buttons.left && this.inputValues.keyboard.keysDown["Control"]) ||
            this.inputValues.mouse.buttons.middle) {
            this._doScroll({
                x: documentDelta.x * this.displayTransform.current.scale,
                y: documentDelta.y * this.displayTransform.current.scale,
            });
            this._setCursor("grabbing");
            this.flags.recordScrollForMomentum = true;
            this.flags.applyScrollMomentum = false;
            this.flags.draggingDisplay = true;
        } else {
            this.flags.recordScrollForMomentum = false;
            this.flags.applyScrollMomentum = true;
            this.flags.draggingDisplay = false;
            this._setCursor("default");
        }
    }

    private _updateMouseWheelHandler() {
        if (this.inputValues.mouse.wheelDelta.current.y === 0 && this.inputValues.mouse.wheelDelta.current.x === 0) return;
        if (this.inputValues.keyboard.keysDown["Control"] &&
            this.inputValues.mouse.wheelDelta.current.y !== 0) {

            const factor = Math.pow(documentContentDisplaySettings.zoomSensitivity,
                this.inputValues.mouse.wheelDelta.current.y / 100);

            this._zoomAboutACanvasPoint(factor, this.inputValues.mouse.position.current);
            this._stopScrollMomentum();
            return;
        }
        if (this.inputValues.keyboard.keysDown["Shift"] &&
            this.inputValues.mouse.wheelDelta.current.y !== 0) {
            this._doScroll({
                    x: (-this.inputValues.mouse.wheelDelta.current.y / 100 *
                        documentContentDisplaySettings.scrollSensitivity.horizontal),
                    y: 0,
                }
            );
            this._stopScrollMomentum();
            return;
        }
        this._doScroll({
                x: (-this.inputValues.mouse.wheelDelta.current.x / 100 *
                    documentContentDisplaySettings.scrollSensitivity.horizontal),
                y: (-this.inputValues.mouse.wheelDelta.current.y / 100 *
                    documentContentDisplaySettings.scrollSensitivity.vertical),
            }
        );
        this._stopScrollMomentum();
    }

    private _zoomAboutACanvasPoint(zoomFactor: number, canvasPoint: {x: number, y: number}) {
        const documentMouseBeforeZoom = {
            x: (canvasPoint.x - this.displayTransform.current.translate.x) / this.displayTransform.edit.scale,
            y: (canvasPoint.y - this.displayTransform.current.translate.y) / this.displayTransform.edit.scale,
        }
        this._doZoom(zoomFactor);
        const documentMouseAfterZoom = {
            x: (canvasPoint.x - this.displayTransform.current.translate.x) / this.displayTransform.edit.scale,
            y: (canvasPoint.y - this.displayTransform.current.translate.y) / this.displayTransform.edit.scale,
        }

        const deltaX = (documentMouseAfterZoom.x - documentMouseBeforeZoom.x);
        const deltaY = (documentMouseAfterZoom.y - documentMouseBeforeZoom.y);

        this._doScroll({
            x: deltaX * this.displayTransform.edit.scale,
            y: deltaY * this.displayTransform.edit.scale,
        });
    }

    private _applyScrollMomentum(dt: number) {
        if (this.renderingValues.scrollMomentum.x === 0 && this.renderingValues.scrollMomentum.y === 0) return;
        if (this.flags.applyScrollMomentum) {
            this._doScroll({
                x: this.renderingValues.scrollMomentum.x * dt,
                y: this.renderingValues.scrollMomentum.y * dt,
            });
        }
    }

    private _updateScrollMomentum(dt: number) {
        if (this.flags.recordScrollForMomentum) {
            this._setScrollMomentum({
                x: (this.displayTransform.current.translate.x - this.displayTransform.previous.translate.x) / dt,
                y: (this.displayTransform.current.translate.y - this.displayTransform.previous.translate.y) / dt,
            });
        }
        this._setScrollMomentum({
            x: this.renderingValues.scrollMomentum.x > 0 ?
                Math.max(0, this.renderingValues.scrollMomentum.x - documentContentDisplaySettings.scrollFriction * dt) :
                Math.min(0, this.renderingValues.scrollMomentum.x + documentContentDisplaySettings.scrollFriction * dt),
            y: this.renderingValues.scrollMomentum.y > 0 ?
                Math.max(0, this.renderingValues.scrollMomentum.y - documentContentDisplaySettings.scrollFriction * dt) :
                Math.min(0, this.renderingValues.scrollMomentum.y + documentContentDisplaySettings.scrollFriction * dt),
        });
    }

    private _addScrollMomentum(momentum: {x?: number, y?: number}) {
        this.renderingValues.scrollMomentum.x += (momentum.x || 0);
        this.renderingValues.scrollMomentum.y += (momentum.y || 0);
    }

    private _stopScrollMomentum() {
        this._setScrollMomentum({x:0,y:0});
    }

    private _setScrollMomentum(momentum: {x?: number, y?: number}) {
        this.renderingValues.scrollMomentum.x = (momentum.x || 0);
        this.renderingValues.scrollMomentum.y = (momentum.y || 0);
    }

    private _updateDisplayTransform() {
        this.displayTransform.previous = {...this.displayTransform.current};
        this.displayTransform.current = {...this.displayTransform.edit};
    }

    private _doZoom(zoomFactor: number) {
        this._setZoom(this.renderingValues.displayZoom * zoomFactor);
    }

    private _doScroll(scrollAmount: { x?: number, y?: number }) {
        this._setScroll({
            x: this.displayTransform.current.translate.x + (scrollAmount.x || 0),
            y: this.displayTransform.current.translate.y + (scrollAmount.y || 0),
        });
    }

    private _setZoom(zoom: number) {
        this.renderingValues.displayZoom = zoom;
        this.displayTransform.edit.scale = this.renderingValues.canvasSize.x / this.renderingValues.documentSize.x * this.renderingValues.displayZoom;
    }

    private _setScroll(scroll: { x?: number, y?: number }) {
        let canvasMinTransformX = this.renderingValues.canvasSize.x - (this.renderingValues.documentSize.x * this.displayTransform.current.scale);
        let canvasMinTransformY = this.renderingValues.canvasSize.y - (this.renderingValues.documentSize.y * this.displayTransform.current.scale);
        canvasMinTransformX *= (canvasMinTransformX < 0 && 1) || 0.5;
        canvasMinTransformY *= (canvasMinTransformY < 0 && 1) || 0.5;
        this.displayTransform.edit.translate = {
            x: Math.max(canvasMinTransformX, Math.min(0, scroll.x || 0)),
            y: Math.max(canvasMinTransformY, Math.min(0, scroll.y || 0)),
        };
    }

    private _documentRectToCanvasRect(rect: {p1: { x:number, y:number }, p2: { x:number, y:number }}) {
        return {
            p1: this._documentSpaceToCanvasSpace(rect.p1),
            p2: this._documentSpaceToCanvasSpace(rect.p2),
        }
    }

    private _documentSpaceToCanvasSpace(v: {x:number, y:number}): {x:number, y:number}{
        return {
            x: v.x * this.displayTransform.current.scale + this.displayTransform.current.translate.x,
            y: v.y * this.displayTransform.current.scale + this.displayTransform.current.translate.y,
        }
    }

    private _canvasSpaceToDocumentSpace(v: {x:number, y:number}): {x:number, y:number}{
        return {
            x: (v.x - this.displayTransform.current.translate.x) / this.displayTransform.current.scale,
            y: (v.y - this.displayTransform.current.translate.y) / this.displayTransform.current.scale,
        }
    }

    private _isRectInsideCanvas(rect: {p1: { x:number, y:number }, p2: { x:number, y:number }}) {
        const rectTopLeft = { x: Math.min(rect.p1.x, rect.p2.x), y: Math.min(rect.p1.y, rect.p2.y) }
        const rectBottomRight = { x: Math.max(rect.p1.x, rect.p2.x), y: Math.max(rect.p1.y, rect.p2.y) }
        return !(rectBottomRight.x <= 0 || rectTopLeft.x >= this.renderingValues.canvasSize.x ||
            rectBottomRight.y <= 0 || rectTopLeft.y >= this.renderingValues.canvasSize.y);
    }

    private _p1p2_to_xywh(rect: {p1: { x:number, y:number }, p2: { x:number, y:number }}) : {x:number ,y:number, w: number, h:number} {
        return {
            x: rect.p1.x,
            y: rect.p1.y,
            w: rect.p2.x - rect.p1.x,
            h: rect.p2.y - rect.p1.y,
        }
    }

    private _xywh_to_p1p2(rect: {x:number ,y:number, w: number, h:number}) : {p1: { x:number, y:number }, p2: { x:number, y:number }} {
        return {
            p1: {
                x: rect.x,
                y: rect.y,
            },
            p2: {
                x: rect.x + rect.w,
                y: rect.y + rect.h,
            }
        }
    }

    private _setCursor(cursor: string, ifDefault?: boolean) {
        if (this.canvasInstance == null) return;
        if (ifDefault && this.canvasInstance.style.cursor !== "default") return;
        this.canvasInstance.style.cursor = cursor;
    }

    private _compareCharacterPointers(pointer1: {page: number, line: number, word: number, character: number},
                                      pointer2: {page: number, line: number, word: number, character: number}) {
        if (pointer1.page < pointer2.page) return -1;
        if (pointer1.page > pointer2.page) return 1;
        if (pointer1.line < pointer2.line) return -1;
        if (pointer1.line > pointer2.line) return 1;
        if (pointer1.word < pointer2.word) return -1;
        if (pointer1.word > pointer2.word) return 1;
        if (pointer1.character < pointer2.character) return -1;
        if (pointer1.character > pointer2.character) return 1;
        return 0
    }
}
export interface DocumentMLDContentRendererProps {
    renderContent: DocumentMLDContent
}
export interface DocumentMLDContentRendererState {

}
