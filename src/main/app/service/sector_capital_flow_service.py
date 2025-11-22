# SPDX-License-Identifier: MIT
"""SectorCapitalFlow Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type

from starlette.responses import StreamingResponse

from fastlib.service.base_service import BaseService
from src.main.app.model.sector_capital_flow_model import SectorCapitalFlowModel
from src.main.app.schema.sector_capital_flow_schema import (
    ListSectorCapitalFlowsRequest,
    CreateSectorCapitalFlowRequest,
    SectorCapitalFlow,
    UpdateSectorCapitalFlowRequest,
    BatchDeleteSectorCapitalFlowsRequest,
    ExportSectorCapitalFlowsRequest,
    BatchCreateSectorCapitalFlowsRequest,
    BatchUpdateSectorCapitalFlowsRequest,
    ImportSectorCapitalFlowsRequest,
    ImportSectorCapitalFlow,
    BatchPatchSectorCapitalFlowsRequest,
)


class SectorCapitalFlowService(BaseService[SectorCapitalFlowModel], ABC):
    @abstractmethod
    async def get_sector_capital_flow(
        self,
        *,
        id: int,
    ) -> SectorCapitalFlowModel: ...

    @abstractmethod
    async def list_sector_capital_flows(
        self, *, req: ListSectorCapitalFlowsRequest
    ) -> tuple[list[SectorCapitalFlowModel], int]: ...

    

    @abstractmethod
    async def create_sector_capital_flow(self, *, req: CreateSectorCapitalFlowRequest) -> SectorCapitalFlowModel: ...

    @abstractmethod
    async def update_sector_capital_flow(self, req: UpdateSectorCapitalFlowRequest) -> SectorCapitalFlowModel: ...

    @abstractmethod
    async def delete_sector_capital_flow(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_sector_capital_flows(self, ids: list[int]) -> list[SectorCapitalFlowModel]: ...

    @abstractmethod
    async def batch_create_sector_capital_flows(
        self,
        *,
        req: BatchCreateSectorCapitalFlowsRequest,
    ) -> list[SectorCapitalFlowModel]: ...

    @abstractmethod
    async def batch_update_sector_capital_flows(
        self, req: BatchUpdateSectorCapitalFlowsRequest
    ) -> list[SectorCapitalFlowModel]: ...

    @abstractmethod
    async def batch_patch_sector_capital_flows(
        self, req: BatchPatchSectorCapitalFlowsRequest
    ) -> list[SectorCapitalFlowModel]: ...

    @abstractmethod
    async def batch_delete_sector_capital_flows(self, req: BatchDeleteSectorCapitalFlowsRequest): ...

    @abstractmethod
    async def export_sector_capital_flows_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_sector_capital_flows(
        self, req: ExportSectorCapitalFlowsRequest
    ) -> StreamingResponse: ...

    @abstractmethod
    async def import_sector_capital_flows(
        self, req: ImportSectorCapitalFlowsRequest
    ) -> list[ImportSectorCapitalFlow]: ...