const isMacOS = navigator.platform.indexOf('Mac') != -1;

const defaultInputState = {
    mouse: {
        buttons: [{
            duration: -1,
            stationary: true,
        },{
            duration: -1,
            stationary: true,
        },{
            duration: -1,
            stationary: true,
        }],
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
        },
    },
    keyboard: {
        keysDown: {} as { [key: string]: boolean },
    }
};


export class InputManager {

    private target?: HTMLElement | null;

    private clipboardTarget?: string;

    private _lastFrameTime?: number;
    private _animationFrameId?: number;

    public state = defaultInputState;

    private eventHooks = {} as {[key:string]:Function};

    private contextmenuPrevented = false;
    
    constructor(target?: HTMLElement | null, selfUpdating?: boolean) {
        this.setTarget(target);
        if (selfUpdating) this.beginFrameUpdates();
    }

    public setTarget(target?: HTMLElement | null) {
        this.target = target;
        this.state = defaultInputState;
        this._initiateInputListeners();
    }

    private _initiateInputListeners() {
        if (!this.target) return;

        this.target.addEventListener("click", event => {
            const hook = this.eventHooks["click"];
            if (hook) hook(event);
        });

        this.target.addEventListener("mousedown", event => {
            this.state.mouse.buttons[event.button].duration = 0;
            this.state.mouse.buttons[event.button].stationary = true;
            const hook = this.eventHooks["mousedown"];
            if (hook) hook(event);
        });

        window.addEventListener("mouseup", event => {
            this.state.mouse.buttons[event.button].duration = -1;
            const hook = this.eventHooks["mouseup"];
            if (hook) hook(event);
        });

        window.addEventListener("keydown", event => {
            this.state.keyboard.keysDown[event.key] = true;

            if (this.clipboardTarget &&
                this.state.keyboard.keysDown[InputManager.getControlKeyName()] &&
                event.key.toLowerCase() === "c") {
                navigator.clipboard.writeText(this.clipboardTarget);
            }
            const hook = this.eventHooks["keydown"];
            if (hook) hook(event);
        });

        window.addEventListener("keyup", event => {
            this.state.keyboard.keysDown[event.key] = false;
            const hook = this.eventHooks["keyup"];
            if (hook) hook(event);
        });

        this.target.addEventListener("wheel", event => {
            this.state.mouse.wheelDelta.new = {
                x: event.deltaX,
                y: event.deltaY,
            };
            const hook = this.eventHooks["wheel"];
            if (hook) hook(event);
        });

        this.target.addEventListener("mousemove", event => {
            if (this.target == null) return;
            const canvasClientRect = this.target.getBoundingClientRect();
            this.state.mouse.position.current = {
                x: event.clientX - canvasClientRect.x,
                y: event.clientY - canvasClientRect.y
            };
            for (let i = 0; i < this.state.mouse.buttons.length; i++)
                if (this.state.mouse.buttons[i].duration >= 0)
                    this.state.mouse.buttons[i].stationary = false;
            const hook = this.eventHooks["mousemove"];
            if (hook) hook(event);
        });

        this.target.addEventListener("contextmenu", event => {
            if (this.contextmenuPrevented) event.preventDefault();
        });
    }

    public static getControlKeyName() {
        return isMacOS && "Meta" || "Control";
    }

    public setClipboardTarget(text?: string) {
        this.clipboardTarget = text;
    }

    public beginFrameUpdates() {
        this._lastFrameTime = performance.now();
        this._frame();
    }

    public stopFrameUpdates() {
        if (this._animationFrameId !== undefined) {
            cancelAnimationFrame(this._animationFrameId);
            this._animationFrameId = undefined;
        }
    }

    private _frame() {
        const currentTime = performance.now();
        const dt = this._lastFrameTime !== undefined ? currentTime - this._lastFrameTime : 0;

        this.update(dt);

        this._lastFrameTime = currentTime;
        this._animationFrameId = requestAnimationFrame(() => this._frame());
    }

    public update(dt: number) {
        this._updateState(dt);
    }

    private _updateState(dt: number) {
        for (let i = 0; i < this.state.mouse.buttons.length; i++)
            if (this.state.mouse.buttons[i].duration >= 0)
                this.state.mouse.buttons[i].duration += dt;
        this.state.mouse.position.previous = {...this.state.mouse.position.current};
        this.state.mouse.wheelDelta.current = {...this.state.mouse.wheelDelta.new};
        this.state.mouse.wheelDelta.new = {x:0,y:0};
    }

    public hookToEvent(eventName: string, callback: Function) {
        this.eventHooks[eventName] = callback;
    }

    public preventContextMenu(doPrevent?: boolean) {
        this.contextmenuPrevented = doPrevent == undefined || doPrevent;
    }
}