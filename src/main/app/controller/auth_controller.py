# Copyright (c) 2025 FastWeb and/or its affiliates. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Auth REST Controller"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from fastlib import constants as constant
from fastlib.response import HttpResponse
from fastlib.schema import UserCredential, CurrentUser
from fastlib.security import get_current_user
from src.main.app.utils.tree_util import list_to_tree
from src.main.app.mapper.menu_mapper import menuMapper
from src.main.app.mapper.role_menu_mapper import roleMenuMapper
from src.main.app.mapper.user_mapper import userMapper
from src.main.app.mapper.user_role_mapper import userRoleMapper
from src.main.app.model.role_menu_model import RoleMenuModel
from src.main.app.model.user_model import UserModel
from src.main.app.schema.auth_schema import (
    SignInWithEmailAndPasswordRequest,
    UserInfo,
)
from src.main.app.schema.menu_schema import Menu
from src.main.app.schema.user_role_schema import ListUserRolesRequest
from src.main.app.service.auth_service import AuthService
from src.main.app.service.impl.auth_service_impl import AuthServiceImpl
from src.main.app.service.impl.menu_service_impl import MenuServiceImpl
from src.main.app.service.impl.role_menu_service_impl import RoleMenuServiceImpl
from src.main.app.service.impl.user_role_service_impl import UserRoleServiceImpl
from src.main.app.service.impl.user_service_impl import UserServiceImpl
from src.main.app.service.menu_service import MenuService
from src.main.app.service.role_menu_service import RoleMenuService
from src.main.app.service.user_role_service import UserRoleService
from src.main.app.service.user_service import UserService

auth_router = APIRouter()
auth_service: AuthService = AuthServiceImpl()
menu_service: MenuService = MenuServiceImpl(mapper=menuMapper)
user_service: UserService = UserServiceImpl(mapper=userMapper)
user_role_service: UserRoleService = UserRoleServiceImpl(mapper=userRoleMapper)
role_menu_service: RoleMenuService = RoleMenuServiceImpl(mapper=roleMenuMapper)


@auth_router.post("/auth:signInWithEmailAndPassword")
async def signin_email_and_password(
    req: OAuth2PasswordRequestForm = Depends(),
) -> UserCredential:
    """
    Authenticates a user with email and password.

    Args:

        req: Contains username (email) and password.

    Returns:

        Authentication user credential with metadata.

    Raises:
        HttpException(401 Unauthorized): Username or password error.
    """
    req = SignInWithEmailAndPasswordRequest(username=req.username, password=req.password)

    return await auth_service.signin_email_password(req=req)


@auth_router.get("/users:menus")
async def get_menus(current_user: CurrentUser = Depends(get_current_user())):
    if current_user.user_id == constant.ADMIN_ID:
        records, _ = await menu_service.retrieve_ordered_data_list(current=1, page_size=1000)
    else:
        user_role_records, _ = await user_role_service.list_user_roles(
            req=ListUserRolesRequest(user_id=current_user.user_id)
        )
        if not user_role_records:
            return []
        role_ids = [user_role.role_id for user_role in user_role_records]
        role_menu_records: list[RoleMenuModel] = await roleMenuMapper.get_by_role_ids(
            role_ids=role_ids
        )
        records = await menu_service.retrieve_by_ids(
            ids=[role_menu.menu_id for role_menu in role_menu_records]
        )
    records = [Menu(**record.model_dump()) for record in records]
    records = [record.model_dump() for record in records if record.visible == 1]
    records.sort(key=lambda x: x["sort"])
    result = list_to_tree(records)
    return result


@auth_router.get("/users:me")
async def get_me_info(
    current_user: CurrentUser = Depends(get_current_user()),
) -> HttpResponse[UserInfo]:
    """
    Retrieves the profile of the current user.

    Args:
        current_user: Currently authenticated user.

    Returns:
        BaseResponse with current user's profile information.
    """
    user_id = current_user.user_id
    user_record: UserModel = await user_service.retrieve_by_id(id=user_id)
    roles, role_models = await auth_service.get_roles(id=user_id)
    menus: list[Menu] = await auth_service.get_menus(id=user_id, role_models=role_models)
    if UserInfo.is_admin(user_id):
        permissions = ["*.*.*"]
    else:
        permission_list = [menu.permission for menu in menus]
        permissions = [permission for permission in permission_list if permission]
    user_info = UserInfo(
        **user_record.model_dump(),
        permissions=permissions,
        roles=roles,
        menus=menus,
    )
    return HttpResponse.success(user_info)
