import {Link} from "react-router-dom";

export function RedirectButtonWrapper(props) {
    return (
        <Link to={props.href}>
            {props.children}
            <a href={props.href} />
        </Link>
    );
}