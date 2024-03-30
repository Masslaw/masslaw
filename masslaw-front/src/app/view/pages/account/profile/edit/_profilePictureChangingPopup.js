import styled from "styled-components";
import React, {useCallback, useEffect, useState} from "react";
import Cropper from 'react-easy-crop';

const ChangeProfilePictureContainer = styled.div`
    position: relative;
    width: 512px;
    background: #1f1f1f;
    display: flex;
    flex-direction: column;
`

const ChangeProfilePicturePopupTitle = styled.div`
    font-size: 24px;
    font-weight: bold;
    color: white;
    margin: 16px 32px 16px 32px;
`

const ChangeProfilePicturePopupSubTitle = styled.div`
    font-size: 14px;
    font-weight: 500;
    margin: 0 32px 16px 32px;
    color: #808080;
`

const ChooseImageInput = styled.button`
    position: relative;
    width: 100%;
    height: 32px;
    background: none;
    border: none;
    color: cornflowerblue;
    font-size: 16px;

    &:hover {
        background: #4b4b4b;
    }
`

const ChooseImageContainer = styled.div`
    position: relative;
    width: 400px;
    height: 400px;
    left: 50%;
    transform: translateX(-50%);
    overflow: hidden;
    pointer-events: all;
    
`;

const ImageInput = styled.input`
    display: none;
`;

const CropContainer = styled.div`
    position: relative;
    width: 100%;
    height: 100%;
`;

const FinishButtonSection = styled.div`
    position: relative;
    width: 100%;
    display: flex;
    flex-direction: row-reverse;
    align-self: flex-end;

    & button {
        position: relative;
        border: 1px solid white;
        height: 32px;
        margin: 16px 16px 16px 0;
        width: 72px;
        border-radius: 8px;
        font-size: 14px;
    }
`

const FinishButton = styled.button`
    color: black;
    background: white;
`

const CancelButton = styled.button`
    color: white;
    background: none;
`

export function ProfilePictureChangingPopup(props) {

    const [s_imageSrc, setImageSrc] = useState(null);
    const [s_crop, setCrop] = useState({ x: 0, y: 0 });
    const [s_zoom, setZoom] = useState(1);
    const [s_croppedAreaPixels, setCroppedAreaPixels] = useState(null);
    const inputRef = React.useRef();

    const onFileChange = async (e) => {
        if (e.target.files && e.target.files.length > 0) {
            const file = e.target.files[0];
            let imageDataUrl = await readFile(file);
            setImageSrc(imageDataUrl);
        }
    };

    const onCropComplete = useCallback((croppedArea, croppedAreaPixels) => {
        setCroppedAreaPixels(croppedAreaPixels);
    }, []);

    const onFinish = useCallback(async () => {
        if (!s_imageSrc) return;
        const imageData = await getCroppedImg(s_imageSrc, s_croppedAreaPixels, 720, 85);
        props.setImageData(imageData);
        props.dismiss();
    }, [s_imageSrc, s_croppedAreaPixels]);

    const triggerFileSelectPopup = () => inputRef.current.click();

    return <>
        <ChangeProfilePictureContainer>
            <ChangeProfilePicturePopupTitle>
                Set Profile Picture
            </ChangeProfilePicturePopupTitle>
            <ChangeProfilePicturePopupSubTitle>
                Set a new Profile Picture for your account
            </ChangeProfilePicturePopupSubTitle>
            <ChooseImageInput onClick={triggerFileSelectPopup}>Choose Image</ChooseImageInput>
            <ImageInput
                type="file"
                accept="image/*"
                ref={inputRef}
                onChange={onFileChange}
            />
            {
                !s_imageSrc ? <></> :
                <ChooseImageContainer>
                    <CropContainer>
                        <Cropper
                            image={s_imageSrc}
                            crop={s_crop}
                            zoom={s_zoom}
                            aspect={1}
                            onCropChange={setCrop}
                            onZoomChange={setZoom}
                            onCropComplete={onCropComplete}
                        />
                    </CropContainer>
                </ChooseImageContainer>
            }
            <FinishButtonSection>
                <FinishButton onClick={onFinish}>Finish</FinishButton>
                <CancelButton onClick={props.dismiss}>Cancel</CancelButton>
            </FinishButtonSection>
        </ChangeProfilePictureContainer>
    </>
}

const readFile = (file) => {
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.addEventListener('load', () => resolve(reader.result), false);
        reader.readAsDataURL(file);
    });
};

const getCroppedImg = async (imageSrc, pixelCrop, maxSize, quality) => {
    const image = new Image();
    image.src = imageSrc;
    await new Promise((resolve) => {
        image.onload = resolve;
    });

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    const scale = Math.min(maxSize / pixelCrop.width, maxSize / pixelCrop.height, 1);
    canvas.width = pixelCrop.width * scale;
    canvas.height = pixelCrop.height * scale;

    ctx.drawImage(
        image,
        pixelCrop.x,
        pixelCrop.y,
        pixelCrop.width,
        pixelCrop.height,
        0,
        0,
        canvas.width,
        canvas.height
    );

    return new Promise((resolve) => {
        canvas.toBlob((blob) => {
            const fileReader = new FileReader();
            fileReader.onloadend = () => {
                const base64data = fileReader.result;
                resolve(base64data);
            };
            fileReader.readAsDataURL(blob);
        }, 'image/jpeg', quality / 100);
    });
};
