# SPDX-License-Identifier: MIT
"""BankCapitalInfo Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type

from starlette.responses import StreamingResponse

from fastlib.service.base_service import BaseService
from src.main.app.model.bank_capital_info_model import BankCapitalInfoModel
from src.main.app.schema.bank_capital_info_schema import (
    ListBankCapitalInfosRequest,
    CreateBankCapitalInfoRequest,
    BankCapitalInfo,
    UpdateBankCapitalInfoRequest,
    BatchDeleteBankCapitalInfosRequest,
    ExportBankCapitalInfosRequest,
    BatchCreateBankCapitalInfosRequest,
    BatchUpdateBankCapitalInfosRequest,
    ImportBankCapitalInfosRequest,
    ImportBankCapitalInfo,
    BatchPatchBankCapitalInfosRequest,
)


class BankCapitalInfoService(BaseService[BankCapitalInfoModel], ABC):
    @abstractmethod
    async def get_bank_capital_info(
        self,
        *,
        id: int,
    ) -> BankCapitalInfoModel: ...

    @abstractmethod
    async def list_bank_capital_infos(
        self, *, req: ListBankCapitalInfosRequest
    ) -> tuple[list[BankCapitalInfoModel], int]: ...

    

    @abstractmethod
    async def create_bank_capital_info(self, *, req: CreateBankCapitalInfoRequest) -> BankCapitalInfoModel: ...

    @abstractmethod
    async def update_bank_capital_info(self, req: UpdateBankCapitalInfoRequest) -> BankCapitalInfoModel: ...

    @abstractmethod
    async def delete_bank_capital_info(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_bank_capital_infos(self, ids: list[int]) -> list[BankCapitalInfoModel]: ...

    @abstractmethod
    async def batch_create_bank_capital_infos(
        self,
        *,
        req: BatchCreateBankCapitalInfosRequest,
    ) -> list[BankCapitalInfoModel]: ...

    @abstractmethod
    async def batch_update_bank_capital_infos(
        self, req: BatchUpdateBankCapitalInfosRequest
    ) -> list[BankCapitalInfoModel]: ...

    @abstractmethod
    async def batch_patch_bank_capital_infos(
        self, req: BatchPatchBankCapitalInfosRequest
    ) -> list[BankCapitalInfoModel]: ...

    @abstractmethod
    async def batch_delete_bank_capital_infos(self, req: BatchDeleteBankCapitalInfosRequest): ...

    @abstractmethod
    async def export_bank_capital_infos_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_bank_capital_infos(
        self, req: ExportBankCapitalInfosRequest
    ) -> StreamingResponse: ...

    @abstractmethod
    async def import_bank_capital_infos(
        self, req: ImportBankCapitalInfosRequest
    ) -> list[ImportBankCapitalInfo]: ...