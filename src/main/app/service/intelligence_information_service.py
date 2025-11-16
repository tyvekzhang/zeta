# SPDX-License-Identifier: MIT
"""IntelligenceInformation Service"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Type

from starlette.responses import StreamingResponse

from fastlib.service.base_service import BaseService
from src.main.app.model.intelligence_information_model import IntelligenceInformationModel
from src.main.app.schema.intelligence_information_schema import (
    ListIntelligenceInformationRequest,
    CreateIntelligenceInformationRequest,
    IntelligenceInformation,
    UpdateIntelligenceInformationRequest,
    BatchDeleteIntelligenceInformationRequest,
    ExportIntelligenceInformationRequest,
    BatchCreateIntelligenceInformationRequest,
    BatchUpdateIntelligenceInformationRequest,
    ImportIntelligenceInformationRequest,
    ImportIntelligenceInformation,
    BatchPatchIntelligenceInformationRequest,
)


class IntelligenceInformationService(BaseService[IntelligenceInformationModel], ABC):
    @abstractmethod
    async def get_intelligence_information(
        self,
        *,
        id: int,
    ) -> IntelligenceInformationModel: ...

    @abstractmethod
    async def list_intelligence_information(
        self, *, req: ListIntelligenceInformationRequest
    ) -> tuple[list[IntelligenceInformationModel], int]: ...

    

    @abstractmethod
    async def create_intelligence_information(self, *, req: CreateIntelligenceInformationRequest) -> IntelligenceInformationModel: ...

    @abstractmethod
    async def update_intelligence_information(self, req: UpdateIntelligenceInformationRequest) -> IntelligenceInformationModel: ...

    @abstractmethod
    async def delete_intelligence_information(self, id: int) -> None: ...

    @abstractmethod
    async def batch_get_intelligence_information(self, ids: list[int]) -> list[IntelligenceInformationModel]: ...

    @abstractmethod
    async def batch_create_intelligence_information(
        self,
        *,
        req: BatchCreateIntelligenceInformationRequest,
    ) -> list[IntelligenceInformationModel]: ...

    @abstractmethod
    async def batch_update_intelligence_information(
        self, req: BatchUpdateIntelligenceInformationRequest
    ) -> list[IntelligenceInformationModel]: ...

    @abstractmethod
    async def batch_patch_intelligence_information(
        self, req: BatchPatchIntelligenceInformationRequest
    ) -> list[IntelligenceInformationModel]: ...

    @abstractmethod
    async def batch_delete_intelligence_information(self, req: BatchDeleteIntelligenceInformationRequest): ...

    @abstractmethod
    async def export_intelligence_information_template(self) -> StreamingResponse: ...

    @abstractmethod
    async def export_intelligence_information(
        self, req: ExportIntelligenceInformationRequest
    ) -> StreamingResponse: ...

    @abstractmethod
    async def import_intelligence_information(
        self, req: ImportIntelligenceInformationRequest
    ) -> list[ImportIntelligenceInformation]: ...