

class CaseAccessEntities:
    OWNER_CLIENT = "owner"
    MANAGER_CLIENT = "manager"
    EDITOR_CLIENT = "editor"
    READER_CLIENT = "reader"
    EXTERNAL_CLIENT = "external"


class AccessActions:
    EDIT = "edit"
    READ = "read"


ACCESS_PERMITTED_KEYS = {
    AccessActions.EDIT: {
        CaseAccessEntities.OWNER_CLIENT: [
            'information'
        ],
        CaseAccessEntities.MANAGER_CLIENT: [
            'information'
        ],
        CaseAccessEntities.EDITOR_CLIENT: [],
        CaseAccessEntities.READER_CLIENT: [],
        CaseAccessEntities.EXTERNAL_CLIENT: []
    },
    AccessActions.READ: {
        CaseAccessEntities.OWNER_CLIENT: [
            'case_id',
            'information',
            'users',
            'files',
            ['processing', 'stage_information']
        ],
        CaseAccessEntities.MANAGER_CLIENT: [
            'case_id',
            'information',
            'users',
            'files',
            ['processing', 'stage_information']
        ],
        CaseAccessEntities.EDITOR_CLIENT: [
            'case_id',
            'information',
            'users',
            'files',
            ['processing', 'stage_information']
        ],
        CaseAccessEntities.READER_CLIENT: [
            'case_id',
            'information',
            'users',
            'files',
            ['processing', 'stage_information']
        ],
        CaseAccessEntities.EXTERNAL_CLIENT: [
            'case_id',
            'information',
            ['processing', 'stage_information']
        ]
    }
}

CAN_ADD_USERS = [
    CaseAccessEntities.OWNER_CLIENT,
    CaseAccessEntities.MANAGER_CLIENT,
]