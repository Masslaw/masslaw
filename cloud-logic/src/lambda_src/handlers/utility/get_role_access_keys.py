from lambda_srcshared_packages.iam_manager.iam_manager import *
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def handler(event, context):
    role_names = (event.get('role_name') or '').split("|")

    for role_name in role_names:
        logger.info(str('|'.join(IAMManager.get_role_access_keys(role_name))))
