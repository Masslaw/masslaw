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
    CASE_CREATE = "/app/cases/create",
    CASE = "/app/cases/:caseId",
    CASE_MAIN = "/app/cases/:caseId/main",
    CASE_DASHBOARD = "/app/cases/:caseId/dashboard",
    CASE_FILES = "/app/cases/:caseId/files",
    FILE_DISPLAY = "/app/cases/:caseId/files/display/:fileId",
    CASE_SEARCH = "/app/cases/:caseId/files/search",
    CASE_ANNOTATIONS = "/app/cases/:caseId/files/highlights",
    CASE_KNOWLEDGE = "/app/cases/:caseId/knowledge",
    CASE_SUBJECTS = "/app/cases/:caseId/subjects",
    CASE_TIMELINE = "/app/cases/:caseId/timeline",
    CASE_KNOWLEDGE_ENTITY = "/app/cases/:caseId/knowledge/entity/:entityId",
}