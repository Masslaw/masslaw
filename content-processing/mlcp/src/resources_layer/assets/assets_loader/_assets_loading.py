import os.path
from typing import IO

assets_root = os.path.dirname(os.path.dirname(__file__))


def get_asset_full_path(asset_local_path: str) -> str:
    return os.path.join(assets_root, asset_local_path)
