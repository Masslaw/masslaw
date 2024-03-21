import {Outlet, useNavigate} from "react-router-dom";
import {model} from "../../model/model";

export function Navigator(props) {
    model.application.navigate = useNavigate();
    return <>{props.children}</>
}
