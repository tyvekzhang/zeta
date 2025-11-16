# SPDX-License-Identifier: MIT
"""IntelligenceInformation domain service impl"""

from __future__ import annotations

import io
import json
from typing import Type, Any

import pandas as pd
from loguru import logger
from pydantic import ValidationError
from starlette.responses import StreamingResponse

from fastlib.constants import FilterOperators
from fastlib.service.impl.base_service_impl import BaseServiceImpl
from fastlib.utils import excel_util
from fastlib.utils.validate_util import ValidateService
from src.main.app.exception.biz_exception import BusinessErrorCode
from src.main.app.exception.biz_exception import BusinessException
from src.main.app.mapper.intelligence_information_mapper import IntelligenceInformationMapper
from src.main.app.model.intelligence_information_model import IntelligenceInformationModel
from src.main.app.schema.intelligence_information_schema import (
    ListIntelligenceInformationRequest,
    IntelligenceInformation,
    CreateIntelligenceInformationRequest,
    UpdateIntelligenceInformationRequest,
    BatchDeleteIntelligenceInformationRequest,
    ExportIntelligenceInformationRequest,
    BatchCreateIntelligenceInformationRequest,
    CreateIntelligenceInformation,
    BatchUpdateIntelligenceInformationRequest,
    UpdateIntelligenceInformation,
    ImportIntelligenceInformationRequest,
    ImportIntelligenceInformation,
    ExportIntelligenceInformation,
    BatchPatchIntelligenceInformationRequest,
    BatchUpdateIntelligenceInformation,
)
from src.main.app.service.intelligence_information_service import IntelligenceInformationService


class IntelligenceInformationServiceImpl(BaseServiceImpl[IntelligenceInformationMapper, IntelligenceInformationModel], IntelligenceInformationService):
    """
    Implementation of the IntelligenceInformationService interface.
    """

    def __init__(self, mapper: IntelligenceInformationMapper):
        """
        Initialize the IntelligenceInformationServiceImpl instance.

        Args:
            mapper (IntelligenceInformationMapper): The IntelligenceInformationMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper, model=IntelligenceInformationModel)
        self.mapper = mapper

    async def get_intelligence_information(
        self,
        *,
        id: int,
    ) -> IntelligenceInformationModel:
        intelligence_information_record: IntelligenceInformationModel = await self.mapper.select_by_id(id=id)
        if intelligence_information_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return intelligence_information_record

    async def list_intelligence_information(
        self, req: ListIntelligenceInformationRequest
    ) -> tuple[list[IntelligenceInformationModel], int]:
        filters = {
            FilterOperators.EQ: {},
            FilterOperators.NE: {},
            FilterOperators.GT: {},
            FilterOperators.GE: {},
            FilterOperators.LT: {},
            FilterOperators.LE: {},
            FilterOperators.BETWEEN: {},
            FilterOperators.LIKE: {},
        }
        if req.id is not None and req.id != "":
            filters[FilterOperators.EQ]["id"] = req.id
        if req.stock_symbol_full is not None and req.stock_symbol_full != "":
            filters[FilterOperators.EQ]["stock_symbol_full"] = req.stock_symbol_full
        if req.news_title is not None and req.news_title != "":
            filters[FilterOperators.EQ]["news_title"] = req.news_title
        if req.news_content is not None and req.news_content != "":
            filters[FilterOperators.EQ]["news_content"] = req.news_content
        if req.news_source is not None and req.news_source != "":
            filters[FilterOperators.EQ]["news_source"] = req.news_source
        if req.publish_time is not None and req.publish_time != "":
            filters[FilterOperators.EQ]["publish_time"] = req.publish_time
        if req.news_url is not None and req.news_url != "":
            filters[FilterOperators.EQ]["news_url"] = req.news_url
        if req.impact_direction is not None and req.impact_direction != "":
            filters[FilterOperators.EQ]["impact_direction"] = req.impact_direction
        if req.impact_level is not None and req.impact_level != "":
            filters[FilterOperators.EQ]["impact_level"] = req.impact_level
        if req.created_at is not None and req.created_at != "":
            filters[FilterOperators.EQ]["created_at"] = req.created_at
        if req.updated_at is not None and req.updated_at != "":
            filters[FilterOperators.EQ]["updated_at"] = req.updated_at
        sort_list = None
        sort_str = req.sort_str
        if sort_str is not None:
            sort_list = json.loads(sort_str)
        return await self.mapper.select_by_ordered_page(
            current=req.current,
            page_size=req.page_size,
            count=req.count,
            **filters,
            sort_list=sort_list,
        )

    

    async def create_intelligence_information(self, req: CreateIntelligenceInformationRequest) -> IntelligenceInformationModel:
        intelligence_information: IntelligenceInformationModel = IntelligenceInformationModel(**req.intelligence_information.model_dump())
        return await self.save(data=intelligence_information)

    async def update_intelligence_information(self, req: UpdateIntelligenceInformationRequest) -> IntelligenceInformationModel:
        intelligence_information_record: IntelligenceInformationModel = await self.retrieve_by_id(id=req.intelligence_information.id)
        if intelligence_information_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        intelligence_information_model = IntelligenceInformationModel(**req.intelligence_information.model_dump(exclude_unset=True))
        await self.modify_by_id(data=intelligence_information_model)
        merged_data = {**intelligence_information_record.model_dump(), **intelligence_information_model.model_dump()}
        return IntelligenceInformationModel(**merged_data)

    async def delete_intelligence_information(self, id: int) -> None:
        intelligence_information_record: IntelligenceInformationModel = await self.retrieve_by_id(id=id)
        if intelligence_information_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_intelligence_information(self, ids: list[int]) -> list[IntelligenceInformationModel]:
        intelligence_information_records = list[IntelligenceInformationModel] = await self.retrieve_by_ids(ids=ids)
        if intelligence_information_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(intelligence_information_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in intelligence_information_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(intelligence_information_records)} != {str(not_exits_ids)}",
            )
        return intelligence_information_records

    async def batch_create_intelligence_information(
        self,
        *,
        req: BatchCreateIntelligenceInformationRequest,
    ) -> list[IntelligenceInformationModel]:
        intelligence_information_list: list[CreateIntelligenceInformation] = req.intelligence_information
        if not intelligence_information_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [IntelligenceInformationModel(**intelligence_information.model_dump()) for intelligence_information in intelligence_information_list]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_intelligence_information(
        self, req: BatchUpdateIntelligenceInformationRequest
    ) -> list[IntelligenceInformationModel]:
        intelligence_information: BatchUpdateIntelligenceInformation = req.intelligence_information
        ids: list[int] = req.ids
        if not intelligence_information or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(
            ids=ids, data=intelligence_information.model_dump(exclude_none=True)
        )
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_intelligence_information(
        self, req: BatchPatchIntelligenceInformationRequest
    ) -> list[IntelligenceInformationModel]:
        intelligence_information: list[UpdateIntelligenceInformation] = req.intelligence_information
        if not intelligence_information:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            intelligence_information.model_dump(exclude_unset=True) for intelligence_information in intelligence_information
        ]
        await self.mapper.batch_update(items=update_data)
        intelligence_information_ids: list[int] = [intelligence_information.id for intelligence_information in intelligence_information]
        return await self.mapper.select_by_ids(ids=intelligence_information_ids)

    async def batch_delete_intelligence_information(self, req: BatchDeleteIntelligenceInformationRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_intelligence_information_template(self) -> StreamingResponse:
        file_name = "intelligence_information_import_tpl"
        return await excel_util.export_excel(
            schema=CreateIntelligenceInformation, file_name=file_name
        )

    async def export_intelligence_information(self, req: ExportIntelligenceInformationRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        intelligence_information_list: list[IntelligenceInformationModel] = await self.mapper.select_by_ids(ids=ids)
        if intelligence_information_list is None or len(intelligence_information_list) == 0:
            logger.error(f"No intelligence_information found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        intelligence_information_page_list = [ExportIntelligenceInformation(**intelligence_information.model_dump()) for intelligence_information in intelligence_information_list]
        file_name = "intelligence_information_data_export"
        return await excel_util.export_excel(
            schema=ExportIntelligenceInformation, file_name=file_name, data_list=intelligence_information_page_list
        )

    async def import_intelligence_information(self, req: ImportIntelligenceInformationRequest) -> list[ImportIntelligenceInformation]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        intelligence_information_records = import_df.to_dict(orient="records")
        if intelligence_information_records is None or len(intelligence_information_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in intelligence_information_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        intelligence_information_import_list = []
        for intelligence_information_record in intelligence_information_records:
            try:
                intelligence_information_create = ImportIntelligenceInformation(**intelligence_information_record)
                intelligence_information_import_list.append(intelligence_information_create)
            except ValidationError as e:
                valid_data = {
                    k: v
                    for k, v in intelligence_information_record.items()
                    if k in ImportIntelligenceInformation.model_fields
                }
                intelligence_information_create = ImportIntelligenceInformation.model_construct(**valid_data)
                intelligence_information_create.err_msg = ValidateService.get_validate_err_msg(e)
                intelligence_information_import_list.append(intelligence_information_create)
                return intelligence_information_import_list

        return intelligence_information_import_list