import React, { useRef, useState, DragEvent, ChangeEvent } from 'react';
import './css.css';

export function FileUploadRegion(props: {
    onGotFiles: (files: File[]) => void
}) {
    const [dragging, setDragging] = useState(false);
    const fileInputRef = useRef<HTMLInputElement | null>(null);

    const onDragOver = (event: DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        setDragging(true);
    };

    const onDragLeave = () => {
        setDragging(false);
    };

    const onDrop = (event: DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        if (event.dataTransfer.items) {
            handleFilesFromItems(event.dataTransfer.items);
        }
        setDragging(false);
    };

    const handleFilesFromItems = (items: DataTransferItemList) => {
        let files = [] as File[];
        for (let i = 0; i < items.length; i++) {
            if (items[i].kind === 'file') {
                const file = items[i].getAsFile();
                if (!file) continue;
                files.push(file);
            }
        }
        if (files.length > 0)
            props.onGotFiles(files);
    };

    const handleFilesFromFileList = (files: FileList) => {
        if (files.length > 0)
            props.onGotFiles(Object.values(files).map((file) => file));
    };

    const openFileDialog = () => {
        if (fileInputRef.current) {
            fileInputRef.current.click();
        }
    };

    const onFilesAdded = (event: ChangeEvent<HTMLInputElement>) => {
        if (event.target.files) {
            handleFilesFromFileList(event.target.files);
        }
    };

    return (
        <div
            className={`file-upload-region clickable ${dragging ? 'dragging' : ''}`}
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            onClick={openFileDialog}
        >
            <input
                ref={fileInputRef}
                className="FileInput"
                type="file"
                multiple
                onChange={onFilesAdded}
                style={{ display: 'none' }}
            />
            <span>{'Drag your files here or click to select'}</span>
        </div>
    );
}
