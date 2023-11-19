import boto3
from botocore.exceptions import ClientError

iam = boto3.client('iam')
sts = boto3.client('sts')


def create_role(role_name, description, assume_role_policy_document, max_session_duration, tags=None):
    if check_role_exists(role_name):
        return False
    response = iam.create_role(
        RoleName=role_name,
        Description=description,
        AssumeRolePolicyDocument=assume_role_policy_document,
        MaxSessionDuration=max_session_duration,
        Tags=tags or []
    )
    return True


def put_role_policy(role_name, policy_name, policy):
    try:
        response = iam.put_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
            PolicyDocument=policy
        )
        return True
    except ClientError as e:
        return False


def delete_role(role_name):
    try:
        response = iam.delete_role(RoleName=role_name)
        print('Role deleted successfully')
    except ClientError as e:
        return None


def list_roles():
    try:
        response = iam.list_roles()
        roles = response['Roles']
        while 'Marker' in response:
            response = iam.list_roles(Marker=response['Marker'])
            roles.extend(response['Roles'])
        return roles
    except ClientError as e:
        return None


def check_role_exists(role_name):
    try:
        response = iam.get_role(RoleName=role_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'NoSuchEntity':
            return False
        else:
            print(e)
            return False


def get_role_access_keys(role_name, _for='temporary_role_access'):
    account_id = sts.get_caller_identity().get('Account')
    response = sts.assume_role(
        RoleArn=f'arn:aws:iam::{account_id}:role/{role_name}',
        RoleSessionName=f'session--{_for}'
    )
    credentials = response.get('Credentials') or {}
    return (
        credentials.get('AccessKeyId'),
        credentials.get('SecretAccessKey'),
        credentials.get('SessionToken'),
    )


__all__ = [
    'create_role',
    'put_role_policy',
    'delete_role',
    'list_roles',
    'check_role_exists',
    'get_role_access_keys',
]
