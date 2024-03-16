export const ApplicationRoutes = {
    _:                  "/",

    HOME:                       "/home",
    LOGIN:                      "/identity/login",
    SIGNUP:                     "/identity/signup",
    VERIFICATION:               "/identity/verification",
    LOGOUT:                     "/identity/logout",
    PASSWORD:                   "/identity/password",

    MY_PROFILE:                 "/profile",
    USER_PROFILE:               "/profile/:userId",
    EDIT_PROFILE:               "/profile/edit",

    APP:                        "/app",
    MY_CASES:                   "/app/cases",
    CASE:                       "/app/cases/:caseId",
    CASE_DASHBOARD:             "/app/cases/:caseId/dashboard",
    CASE_FILES:                 "/app/cases/:caseId/files",
    FILE_DISPLAY:               "/app/cases/:caseId/files/:fileId",
    CASE_SEARCH:                "/app/cases/:caseId/search",
    CASE_KNOWLEDGE:             "/app/cases/:caseId/knowledge",
    CASE_SUBJECTS:              "/app/cases/:caseId/subjects",
    CASE_TIMELINE:              "/app/cases/:caseId/timeline",
    CASE_KNOWLEDGE_ENTITY:      "/app/cases/:caseId/knowledge/:entityId",
}
