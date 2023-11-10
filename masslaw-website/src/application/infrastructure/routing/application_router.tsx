import React, {useEffect} from 'react';
import {BrowserRouter, Outlet, Route, Routes, useLocation, useNavigate} from 'react-router-dom';

import {Home} from "../../pages/public/home/home";
import {MainApplication} from "../../pages/main_application/main_application";
import {Identity} from "../../pages/authentication/identity/identity";
import {Verification} from "../../pages/authentication/verification/verification";
import {Dashboard} from "../../pages/main_application/dashboard/dashboard";
import {Profile} from "../../pages/masslawyer/profile/profile";
import {Masslawyer} from "../../pages/masslawyer/masslawyer";
import {ApplicationRoutingManager} from "./application_routing_manager";
import {ApplicationRoutes} from "./application_routes";
import {LogOut} from "../../pages/authentication/log_out/log_out";
import {CaseDisplay} from "../../pages/main_application/cases/case/case_display";
import {CasesList} from "../../pages/main_application/cases/cases_list";
import {CreateCase} from "../../pages/main_application/cases/create/create_case";
import {CaseFiles} from "../../pages/main_application/cases/case/files/case_files";
import {Password} from "../../pages/authentication/password/password";
import {CaseMain} from "../../pages/main_application/cases/case/main/case_main";
import {FileDisplay} from "../../pages/main_application/cases/case/files/display/file_display";

export function ApplicationRouter() {

    let BaseRoute = ApplicationRoutingManager.getInstance().getComponent();

    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route path={''} element={<><BaseRoute /></>} >
                        <Route path={ApplicationRoutes.HOME} element={<Home />} />
                        <Route path={ApplicationRoutes.IDENTITY} element={<Identity />} />
                        <Route path={ApplicationRoutes.VERIFICATION} element={<Verification />} />
                        <Route path={ApplicationRoutes.LOGOUT} element={<LogOut />} />
                        <Route path={ApplicationRoutes.PASSWORD} element={<Password />} />

                        <Route path={ApplicationRoutes.MASSLAWYER} element={<><Masslawyer/></>} >
                            <Route path={ApplicationRoutes.PROFILE} element={<Profile />} />
                        </Route>

                        <Route path={ApplicationRoutes.APP} element={<><MainApplication/></>} >
                            <Route path={ApplicationRoutes.DASHBOARD} element={<Dashboard />} />
                            <Route path={ApplicationRoutes.CASES} element={<CasesList />} />
                            <Route path={ApplicationRoutes.CASE_CREATE} element={<CreateCase />} />
                            <Route path={ApplicationRoutes.CASE} element={<><CaseDisplay/></>} >
                                <Route path={ApplicationRoutes.CASE_MAIN} element={<CaseMain />} />
                                <Route path={ApplicationRoutes.CASE_FILES} element={<CaseFiles />} />
                                <Route path={ApplicationRoutes.FILE_DISPLAY} element={<FileDisplay />} />
                            </Route>
                        </Route>
                    </Route>
                </Routes>
            </BrowserRouter>
        </>
    )
}