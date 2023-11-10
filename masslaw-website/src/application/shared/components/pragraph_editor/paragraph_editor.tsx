import React, {useEffect, useRef, useState} from 'react';
import {MasslawButton, MasslawButtonTypes} from "../masslaw_button/masslaw_button";
import {LoadingButton} from "../loading_button/loading_button";
import {faPencil} from "@fortawesome/free-solid-svg-icons";


import './css.css'

export function ParagraphEditor(props:{
    text: string;
    editable: boolean;
    maxCharacters?: number;
    size?: {w?: number, h?: number};
    fontSize?: number;
    onFinish: (newText: string) => void;
}){
    const [finish_loading, setFinishLoading] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [currentText, setCurrentText] = useState(props.text);

    useEffect(() => {
        setCurrentText(props.text);
    }, [props.text])

    const handleEdit = () => {
        setIsEditing(true);
    };

    const handleFinish = async () => {
        setFinishLoading(true);
        await props.onFinish(currentText);
        setFinishLoading(false);
        setIsEditing(false);
    };

    const handleCancel = () => {
        setCurrentText(props.text);
        setIsEditing(false);
    };

    return (
        <div style={{ position: 'relative' }}>
            <>
                <div
                    className={'paragraph-editor-container'}
                >
                    <textarea
                        className={'paragraph-editor-text-content'}
                        readOnly={!isEditing}
                        dir={'auto'}
                        value={currentText}
                        style={{
                            width: `${props.size?.w || '-'}px`,
                            height: `${props.size?.h || '-'}px`,
                            fontSize: `${props.fontSize || '-'}px`,
                        }}
                        onChange={e => setCurrentText(e.target.value)}
                    />
                    {isEditing &&
                    <>
                        {
                            props.maxCharacters &&
                            <div className={`max-characters-text ${currentText.length > props.maxCharacters && 'invalid' || ''}`}>
                                {currentText.length}/{props.maxCharacters}
                            </div>
                        }
                        <div className={'paragraph-editor-finish-editing-buttons'}>
                            <div>
                                <LoadingButton
                                    clickable={!(props.maxCharacters && currentText.length > props.maxCharacters)}
                                    onClick={handleFinish}
                                    caption={'Finish'}
                                    loading={finish_loading}
                                    size={{w: 60, h:25}}
                                />
                            </div>
                            <div>
                                <MasslawButton
                                    buttonType={MasslawButtonTypes.SECONDARY}
                                    onClick={handleCancel}
                                    caption={'Cancel'}
                                    size={{w: 50, h:25}}
                                />
                            </div>
                        </div>
                    </>
                    ||
                    <>
                        {
                            props.editable &&
                            <div className={'paragraph-editor-edit-button'}>
                                <MasslawButton
                                    buttonType={MasslawButtonTypes.CLEAR}
                                    caption={''}
                                    onClick={handleEdit}
                                    icon={faPencil}
                                    size={{w: 30, h: 30}}
                                />
                            </div>
                        }
                    </>}
                </div>
            </>
        </div>
    );
};
