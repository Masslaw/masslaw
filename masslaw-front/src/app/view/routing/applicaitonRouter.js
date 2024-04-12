import {ApplicationRoutes} from "../../config/applicaitonRoutes";
import {Route, Routes, BrowserRouter, useNavigate} from "react-router-dom";
import {Home} from "../pages/public/home/home";
import {Signup} from "../pages/identity/signup/singup";
import {Login} from "../pages/identity/login/login";
import {Verification} from "../pages/identity/verification/verification";
import {Navigator} from "./_navigator";
import {Profile} from "../pages/account/profile/profile";
import {EditProfile} from "../pages/account/profile/edit/editProfile";
import {MyCases} from "../pages/app/cases/myCases";
import {Case} from "../pages/app/cases/case/case";
import {CaseFileDisplay} from "../pages/app/cases/case/file/file";
import {CaseSearch} from "../pages/app/cases/case/search/caseSearch";
import {CaseKnowledge} from "../pages/app/cases/case/knowledge/caseKnowledge";
import {CaseDashboard} from "../pages/app/cases/case/dashboard/caseDashboard";
import {CaseSubjects} from "../pages/app/cases/case/subjects/caseSubjects";
import {CaseUsers} from "../pages/app/cases/case/users/caseUsers";
import {CaseTimelineDisplay} from "../components/caseTimelineDisplay";

const RedirectHome = () => {
    window.location.href = ApplicationRoutes.HOME;
    return <></>
}

export function ApplicationRouter(props) {
    return <>
        <BrowserRouter>
            <Navigator>
                <Routes>
                    <Route path={ApplicationRoutes.HOME} element={<Home/>}/>
                    <Route path={ApplicationRoutes.SIGNUP} element={<Signup/>}/>
                    <Route path={ApplicationRoutes.LOGIN} element={<Login/>}/>
                    <Route path={ApplicationRoutes.VERIFICATION} element={<Verification/>}/>
                    <Route path={ApplicationRoutes.MY_PROFILE} element={<Profile/>}/>
                    <Route path={ApplicationRoutes.USER_PROFILE} element={<Profile/>}/>
                    <Route path={ApplicationRoutes.EDIT_PROFILE} element={<EditProfile/>}/>
                    <Route path={ApplicationRoutes.MY_CASES} element={<MyCases/>}/>
                    <Route path={ApplicationRoutes.CASE} element={<Case/>}>
                        <Route path={ApplicationRoutes.CASE_SETTINGS} element={<div></div>}/>
                        <Route path={ApplicationRoutes.CASE_DASHBOARD} element={<CaseDashboard/>}/>
                        <Route path={ApplicationRoutes.FILE_DISPLAY} element={<CaseFileDisplay/>}/>
                        <Route path={ApplicationRoutes.CASE_SEARCH} element={<CaseSearch/>}/>
                        <Route path={ApplicationRoutes.CASE_KNOWLEDGE} element={<CaseKnowledge/>}/>
                        <Route path={ApplicationRoutes.CASE_SUBJECTS} element={<CaseSubjects/>}/>
                        <Route path={ApplicationRoutes.CASE_TIMELINE} element={<CaseTimelineDisplay />}/>
                        <Route path={ApplicationRoutes.CASE_KNOWLEDGE_ENTITY} element={<div></div>}/>
                        <Route path={ApplicationRoutes.CASE_USERS} element={<CaseUsers />}/>
                    </Route>
                    <Route path={'*'} element={<RedirectHome/>}/>
                </Routes>
            </Navigator>
        </BrowserRouter>
    </>
}
