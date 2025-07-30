"""Neuromation auth client."""

from importlib.metadata import version

from .api import check_permissions, get_user_and_kind
from .client import (
    Action,
    AuthClient,
    ClientAccessSubTreeView,
    ClientSubTreeViewRoot,
    Permission,
    Role,
    User,
)
from .security import Kind

__all__ = [
    "Action",
    "AuthClient",
    "ClientAccessSubTreeView",
    "ClientSubTreeViewRoot",
    "Kind",
    "Permission",
    "Role",
    "User",
    "check_permissions",
    "get_user_and_kind",
]
__version__ = version(__package__)
