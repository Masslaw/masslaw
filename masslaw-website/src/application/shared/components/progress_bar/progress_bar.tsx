import {useEffect, useState} from "react";

export function ProgressBar(props: {
    progress: number }) {

    const [progress, setProgress] = useState(0);

    useEffect(() => {
        setProgress(Math.max(0, Math.min(1, props.progress)));
    }, [props.progress])

    return (
        <div style={{
            width: '100%',
            height: '100%',
            position: 'relative',
            background: 'none',
            borderRadius: '3px',
            border: '1px solid var(--masslaw-light-border-color)',
            overflow: `hidden`,
        }}>
            <div style={{
                width: `${progress * 100}%`,
                height: `100%`,
                position: `absolute`,
                overflow: `hidden`,
                transition: `0.2s width ease-out`,
            }}>
                <div style={{
                    width: `100%`,
                    height: `100%`,
                    position: `absolute`,
                    background: `linear-gradient(90deg, var(--masslaw-primary-main) 0%, var(--masslaw-secondary-main) ${1/progress*100}%)`
                }}/>
            </div>
        </div>
    )
}