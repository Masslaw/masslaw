import boto3
from botocore.exceptions import ClientError

iam = boto3.client('iam')
sts = boto3.client('sts')


class IAMManager:
    
    @staticmethod
    def create_role(role_name, description, assume_role_policy_document, max_session_duration, tags=None):
        """
        Create a new IAM role.

        Parameters:
            role_name (str): The name of the role.
            description (str): The description of the role.
            assume_role_policy_document (str): The JSON policy document that grants permission to assume the role.
            max_session_duration (int): The maximum session duration for the role, in seconds.
            tags (dict): A dictionary of key-value pairs that are attached to the role.

        Returns:
            None

        Raises:
            ClientError: If there was an error creating the role.
        """

        if IAMManager.check_role_exists(role_name):
            return False

        response = iam.create_role(
            RoleName=role_name,
            Description=description,
            AssumeRolePolicyDocument=assume_role_policy_document,
            MaxSessionDuration=max_session_duration,
            Tags=tags or []
        )
        return True

    @staticmethod
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

    @staticmethod
    def delete_role(role_name):
        """
        Delete an existing IAM role.

        Parameters:
            role_name (str): The name of the role.

        Returns:
            None

        Raises:
            ClientError: If there was an error deleting the role.
        """
        try:
            response = iam.delete_role(RoleName=role_name)

            print('Role deleted successfully')

        except ClientError as e:
            return None

    @staticmethod
    def list_roles():
        """
        List all IAM roles in the current account.

        Parameters:
            None

        Returns:
            List: A list of IAM roles.
        """
        try:
            response = iam.list_roles()
            roles = response['Roles']

            while 'Marker' in response:
                response = iam.list_roles(Marker=response['Marker'])
                roles.extend(response['Roles'])

            return roles

        except ClientError as e:
            return None

    @staticmethod
    def check_role_exists(role_name):
        """
        Check if an IAM role with the given name exists.

        Parameters:
            role_name (str): The name of the IAM role to check.

        Returns:
            bool: True if the role exists, False otherwise.
        """
        try:
            response = iam.get_role(RoleName=role_name)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchEntity':
                return False
            else:
                print(e)
                return False

    @staticmethod
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