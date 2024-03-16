import React, {useEffect} from "react";
import {model} from "../../../../model/model";
import {useModelValueAsReactState} from "../../../../controller/functionality/model/modelReactHooks";
import {useParams} from "react-router-dom";
import {UserStatus} from "../../../../config/userStatus";



export function Profile() {

    const {userId} = useParams();

    const modelStateManager = model.services['modelStateManager'];
    const usersManager = model.services['usersManager'];

    model.application.view.state.header.shown = true;
    model.application.pages.currentPage.minimumUserStatus = userId ? 0 : UserStatus.FULLY_APPROVED;
    model.application.pages.currentPage.maximumUserStatus = null;
    model.application.pages.currentPage.name = "Profile";

    const [s_userData, setUserData] = React.useState({});

    useEffect(() => {
        if (userId) {
            usersManager.fetchUserData(userId, true).then(
                () => setUserData(model.users.data[userId])
            );
        } else {
            usersManager.fetchMyUserData(true).then(
                () => setUserData(model.users.mine.data)
            );
        }
    }, [userId]);

    return <>
        {JSON.stringify(s_userData)}
    </>
}