export const modelInitState = {
    services: {},
    users: {
        mine: {
            authentication: {
                tokens: {
                    access: null,
                    refresh: null,
                },
                status: -1,
                login: {
                    email: null,
                    password: null,
                },
                verification: {
                    lastCodeSendingTime: 0,
                }
            },
            data: {},
        },
        data: {},
        profilePictureModificationTimes: {},
    },
    cases: {
        currentOpen: {
            id: null,
            files: {
                currentOpen: {
                    id: null,
                },
                all: {},
                filesToUpload: {},
                filesToCompleteUploading: {},
            },
            comments: {
                data: {},
                targetCommentId: null,
            },
            search: {
                currentSearchText: '',
                results: {},
                history: [],
                targetResultIndex: -1,
            },
            knowledge: {
                entities: [],
                connections: []
            },
            conversations: {
                data: {},
                content: {}
            },
        },
        all: {},
    },
    application: {
        navigate: (p) => {},
        searchParams: {},
        pages: {
            currentPage: {
                name: null,
                maximumUserStatus: null,
                minimumUserStatus: null,
            },
        },
        view: {
            state: {
                header: {
                    shown: true
                },
                loading: {},
                notificationsQueue: [],
                popupsQueue: [],
                userMenuOpen: false,
            }
        }
    },
}
