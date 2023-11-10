
export interface MLDContent {
    type: string,
    data: {
        [key: string] : any
    }
}

export interface DocumentMLDContent extends MLDContent{
    data: {
        pages : {
            bg: {
                data: string,
                format: string
            }
            width: number,
            height: number,
            lines: {
                words: {
                    characters: {
                        x1: number,
                        y1: number,
                        x2: number,
                        y2: number,
                        text: string,
                        language: string,
                    }[]
                }[]
            }[]
        }[]
    }
}
