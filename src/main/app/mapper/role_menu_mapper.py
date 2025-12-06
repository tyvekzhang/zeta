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
#
"""RoleMenu mapper"""

from typing import Optional

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from fastlib.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.role_menu_model import RoleMenuModel


class RoleMenuMapper(SqlModelMapper[RoleMenuModel]):
    async def get_by_role_ids(
        self, *, role_ids: list[int], db_session: Optional[AsyncSession] = None
    ) -> list[RoleMenuModel]:
        """
        Retrieve records by list of role id.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(select(self.model).where(self.model.role_id.in_(role_ids)))
        return result.all()


roleMenuMapper = RoleMenuMapper(RoleMenuModel)
