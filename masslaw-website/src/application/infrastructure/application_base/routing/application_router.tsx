import React from 'react';
import {BrowserRouter, Navigate, Route, Routes} from 'react-router-dom';
import {ApplicationGlobalRouting} from "./application_global_routing";
import {Home} from "../../../pages/public/home/home";
import {MainApplication} from "../../../pages/main_application/main_application";
import {Identity} from "../../../pages/authentication/identity/identity";
import {Verification} from "../../../pages/authentication/verification/verification";
import {Dashboard} from "../../../pages/main_application/dashboard/dashboard";
import {Profile} from "../../../pages/masslawyer/profile/profile";
import {Masslawyer} from "../../../pages/masslawyer/masslawyer";
import {ApplicationRoutes} from "./application_routes";
import {LogOut} from "../../../pages/authentication/log_out/log_out";
import {CaseDisplay} from "../../../pages/main_application/cases/case/case_display";
import {CreateCase} from "../../../pages/main_application/cases/create/create_case";
import {CaseFiles} from "../../../pages/main_application/cases/case/files/case_files";
import {Password} from "../../../pages/authentication/password/password";
import {CaseMain} from "../../../pages/main_application/cases/case/main/case_main";
import {FileDisplay} from "../../../pages/main_application/cases/case/files/display/file_display";
import {CaseSearch} from "../../../pages/main_application/cases/case/search/case_search";
import {ApplicationPageRenderer} from "./application_page_renderer";
import {UserStatus} from "../../user_management/user_status";
import {CaseAnnotations} from "../../../pages/main_application/cases/case/annotations/case_annotations";
import {CaseKnowledge} from "../../../pages/main_application/cases/case/knowledge/case_knowledge";
import {NodeDisplay} from "../../../pages/main_application/cases/case/knowledge/node_display/node_display";


export function ApplicationRouter() {
    return (
        <>
            <BrowserRouter>
                <Routes>
                    <Route path={''} element={<ApplicationGlobalRouting/>}>
                        <Route path={''} element={<Navigate to={ApplicationRoutes.HOME} />} />
                        <Route
                            path={ApplicationRoutes.HOME}
                            element={
                                <ApplicationPageRenderer
                                    pageComponent={Home}
                                    statusPolicy={{
                                        maximumStatus: UserStatus.GUEST,
                                    }}
                                />
                            }
                        />
                        <Route
                            path={ApplicationRoutes.IDENTITY}
                            element={
                                <ApplicationPageRenderer
                                    pageComponent={Identity}
                                    statusPolicy={{
                                        maximumStatus: UserStatus.GUEST,
                                    }}
                                />
                            }
                        />
                        <Route
                            path={ApplicationRoutes.VERIFICATION}
                            element={
                                <ApplicationPageRenderer
                                    pageComponent={Verification}
                                    statusPolicy={{
                                        maximumStatus: UserStatus.GUEST,
                                    }}
                                />
                            }
                        />
                        <Route
                            path={ApplicationRoutes.LOGOUT}
                            element={
                                <ApplicationPageRenderer
                                    pageComponent={LogOut}
                                    statusPolicy={{
                                        minimumStatus: UserStatus.LOGGED_IN,
                                    }}
                                />
                            }
                        />
                        <Route
                            path={ApplicationRoutes.PASSWORD}
                            element={
                                <ApplicationPageRenderer
                                    pageComponent={Password}
                                    statusPolicy={{
                                        minimumStatus: UserStatus.GUEST,
                                    }}
                                />
                            }
                        />
                        <Route
                            path={ApplicationRoutes.MASSLAWYER}
                            element={
                                <ApplicationPageRenderer
                                    pageComponent={Masslawyer}
                                    statusPolicy={{
                                        minimumStatus: UserStatus.LOGGED_IN,
                                    }}
                                />
                            }
                        >
                            <Route
                                path={ApplicationRoutes.PROFILE}
                                element={
                                    <ApplicationPageRenderer
                                        pageComponent={Profile}
                                    />
                                }
                            />
                        </Route>
                        <Route
                            path={ApplicationRoutes.APP}
                            element={
                                <ApplicationPageRenderer
                                    pageComponent={MainApplication}
                                    statusPolicy={{
                                        minimumStatus: UserStatus.FULLY_APPROVED,
                                    }}
                                />
                            }
                        >
                            <Route
                                path={ApplicationRoutes.DASHBOARD}
                                element={
                                    <ApplicationPageRenderer
                                        pageComponent={Dashboard}
                                    />
                                }
                            />
                            <Route
                                path={ApplicationRoutes.CASE_CREATE}
                                element={
                                    <ApplicationPageRenderer
                                        pageComponent={CreateCase}
                                    />
                                }
                            />
                            <Route
                                path={ApplicationRoutes.CASE}
                                element={
                                    <ApplicationPageRenderer
                                        pageComponent={CaseDisplay}
                                    />
                                }
                            >
                                <Route
                                    path={ApplicationRoutes.CASE_MAIN}
                                    element={
                                        <ApplicationPageRenderer
                                            pageComponent={CaseMain}
                                        />
                                    }
                                />
                                <Route
                                    path={ApplicationRoutes.CASE_FILES}
                                    element={
                                        <ApplicationPageRenderer
                                            pageComponent={CaseFiles}
                                        />
                                    }
                                />
                                <Route
                                    path={ApplicationRoutes.FILE_DISPLAY}
                                    element={
                                        <ApplicationPageRenderer
                                            pageComponent={FileDisplay}
                                        />
                                    }
                                />
                                <Route
                                    path={ApplicationRoutes.CASE_SEARCH}
                                    element={
                                        <ApplicationPageRenderer
                                            pageComponent={CaseSearch}
                                        />
                                    }
                                />
                                <Route
                                    path={ApplicationRoutes.CASE_ANNOTATIONS}
                                    element={
                                        <ApplicationPageRenderer
                                            pageComponent={CaseAnnotations}
                                        />
                                    }
                                />
                                <Route
                                    path={ApplicationRoutes.CASE_KNOWLEDGE}
                                    element={
                                        <ApplicationPageRenderer
                                            pageComponent={CaseKnowledge}
                                        />
                                    }
                                />
                                <Route
                                    path={ApplicationRoutes.CASE_KNOWLEDGE_ENTITY}
                                    element={
                                        <ApplicationPageRenderer
                                            pageComponent={NodeDisplay}
                                        />
                                    }
                                />
                            </Route>
                        </Route>
                    </Route>
                </Routes>
            </BrowserRouter>
        </>
    )
}

