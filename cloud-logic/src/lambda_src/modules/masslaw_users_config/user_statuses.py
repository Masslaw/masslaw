class UserStatuses:
    UNKNOWN = -1
    GUEST = 0
    LOGGED_IN = 10
    UNVERIFIED = 30
    MISSING_CREDENTIALS = 50
    FULLY_APPROVED = 100


REQUIRED_CREDENTIALS = [
    'first_name',
    'last_name',
    'email'
]