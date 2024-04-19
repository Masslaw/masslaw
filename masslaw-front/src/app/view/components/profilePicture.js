import {useEffect, useMemo, useState} from "react";
import styled from "styled-components";
import {Color} from "../../controller/functionality/visual-utils/color";
import {SVG_PATHS} from "../config/svgPaths";
import {useModelValueAsReactState} from "../../controller/functionality/model/modelReactHooks";
import {LoadingIcon} from "./loadingIcon";

const ProfilePictureContainer = styled.div`
    width: 100%;
    height: 100%;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
    padding: 0;
    
    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
`

export function ProfilePicture(props) {

    const [s_failedToLoad, setFailedToLoad] = useState(false);

    const [s_modificationTimes, setModificationTimes] = useModelValueAsReactState('$.users.profilePictureModificationTimes', {});

    const m_profilePictureUrl = useMemo(() => {
        if (!props.userId) return null;
        if (!props.size) return null;
        const modificationTime = s_modificationTimes[props.userId];
        if (!modificationTime) return setModificationTimes(m => ({...(m || {}), [props.userId]: Date.now()}));
        return 'https://masslaw-profile-pictures.s3.amazonaws.com/' + props.userId + '/' + props.size + '.jpg?t=' + modificationTime;
    }, [props.userId, props.size, s_modificationTimes]);

    return <>
        <ProfilePictureContainer>
            {
                m_profilePictureUrl == null ? <>
                    <LoadingIcon width={'50%'} height={'50%'}/>
                </> : s_failedToLoad ? <>
                    <DefaultPicture userId={props.userId}/>
                </> : <img
                    src={m_profilePictureUrl}
                    onLoad={() => props.onLoad && props.onLoad()}
                    onError={() => setFailedToLoad(true)}
                />
            }
        </ProfilePictureContainer>
    </>
}

const UserDefaultPicture = styled.div`
    width: 100%;
    height: 100%;
    background: ${({background}) => background};
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.5em;
    overflow: hidden;
    
    svg {
        width: 100%;
        height: 80%;
        margin-top: 20%;
    }
    
    path {
        fill: white;
    }
`;

export function DefaultPicture(props) {

    const m_backgroundColor = useMemo(() => {
        const color = new Color();
        color.fromString(props.userId);
        const hsv = color.getHSV();
        hsv.s = 0.5;
        hsv.v = 0.5;
        color.setHSV(hsv.h, hsv.s, hsv.v);
        return color.getHex();
    }, [props.userId]);

    return <>
        <UserDefaultPicture background={m_backgroundColor}>
            <svg viewBox={"0 0 1 1"}>
                <path d={SVG_PATHS.person}/>
            </svg>
        </UserDefaultPicture>
    </>
}
