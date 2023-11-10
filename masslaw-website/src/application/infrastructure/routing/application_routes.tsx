import {Outlet, useLocation, useNavigate} from "react-router-dom";
import React, {useEffect} from "react";

export enum ApplicationRoutes {
    _ = "/",

    HOME = "/home",
    IDENTITY = "/identity",
    VERIFICATION = "/verification",
    LOGOUT = "/logout",
    PASSWORD = "/password",

    MASSLAWYER = "/masslawyer",
    PROFILE = "/masslawyer/profile",

    APP = "/app",
    DASHBOARD = "/app/dashboard",
    CASES = "/app/cases",
    CASE_CREATE = "/app/cases/create",
    CASE = "/app/cases/:caseId",
    CASE_MAIN = "/app/cases/:caseId/main",
    CASE_FILES = "/app/cases/:caseId/files",
    FILE_DISPLAY = "/app/cases/:caseId/files/display/:fileId",
}