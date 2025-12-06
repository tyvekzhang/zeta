# SPDX-License-Identifier: MIT
"""BankCapitalInfo mapper"""

from __future__ import annotations

from sqlmodel import select
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession

from fastlib.mapper.impl.base_mapper_impl import SqlModelMapper
from src.main.app.model.bank_capital_info_model import BankCapitalInfoModel


class BankCapitalInfoMapper(SqlModelMapper[BankCapitalInfoModel]):

    async def select_by_bank_code(
        self, *, bank_code: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[BankCapitalInfoModel]:
        """
        Retrieve a record by bank_code.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.bank_code == bank_code)
        )
        return result.one_or_none()

    async def select_by_bank_code_list(
        self, *, bank_code_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[BankCapitalInfoModel]:
        """
        Retrieve records by list of bank_code.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.bank_code.in_(bank_code_list))
        )
        return result.all()


    async def select_by_bank_type(
        self, *, bank_type: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[BankCapitalInfoModel]:
        """
        Retrieve a record by bank_type.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.bank_type == bank_type)
        )
        return result.one_or_none()

    async def select_by_bank_type_list(
        self, *, bank_type_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[BankCapitalInfoModel]:
        """
        Retrieve records by list of bank_type.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.bank_type.in_(bank_type_list))
        )
        return result.all()


    async def select_by_trade_date(
        self, *, trade_date: str, db_session: Optional[AsyncSession] = None
    ) -> Optional[BankCapitalInfoModel]:
        """
        Retrieve a record by trade_date.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.trade_date == trade_date)
        )
        return result.one_or_none()

    async def select_by_trade_date_list(
        self, *, trade_date_list: list[str], db_session: Optional[AsyncSession] = None
    ) -> list[BankCapitalInfoModel]:
        """
        Retrieve records by list of trade_date.
        """
        db_session = db_session or self.db.session
        result = await db_session.exec(
            select(self.model).where(self.model.trade_date.in_(trade_date_list))
        )
        return result.all()



bankCapitalInfoMapper = BankCapitalInfoMapper(BankCapitalInfoModel)