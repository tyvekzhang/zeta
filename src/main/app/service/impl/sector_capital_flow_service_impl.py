# SPDX-License-Identifier: MIT
"""SectorCapitalFlow domain service impl"""

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
from src.main.app.mapper.sector_capital_flow_mapper import SectorCapitalFlowMapper
from src.main.app.model.sector_capital_flow_model import SectorCapitalFlowModel
from src.main.app.schema.sector_capital_flow_schema import (
    ListSectorCapitalFlowsRequest,
    SectorCapitalFlow,
    CreateSectorCapitalFlowRequest,
    UpdateSectorCapitalFlowRequest,
    BatchDeleteSectorCapitalFlowsRequest,
    ExportSectorCapitalFlowsRequest,
    BatchCreateSectorCapitalFlowsRequest,
    CreateSectorCapitalFlow,
    BatchUpdateSectorCapitalFlowsRequest,
    UpdateSectorCapitalFlow,
    ImportSectorCapitalFlowsRequest,
    ImportSectorCapitalFlow,
    ExportSectorCapitalFlow,
    BatchPatchSectorCapitalFlowsRequest,
    BatchUpdateSectorCapitalFlow,
)
from src.main.app.service.sector_capital_flow_service import SectorCapitalFlowService


class SectorCapitalFlowServiceImpl(BaseServiceImpl[SectorCapitalFlowMapper, SectorCapitalFlowModel], SectorCapitalFlowService):
    """
    Implementation of the SectorCapitalFlowService interface.
    """

    def __init__(self, mapper: SectorCapitalFlowMapper):
        """
        Initialize the SectorCapitalFlowServiceImpl instance.

        Args:
            mapper (SectorCapitalFlowMapper): The SectorCapitalFlowMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper, model=SectorCapitalFlowModel)
        self.mapper = mapper

    async def get_sector_capital_flow(
        self,
        *,
        id: int,
    ) -> SectorCapitalFlowModel:
        sector_capital_flow_record: SectorCapitalFlowModel = await self.mapper.select_by_id(id=id)
        if sector_capital_flow_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return sector_capital_flow_record

    async def list_sector_capital_flows(
        self, req: ListSectorCapitalFlowsRequest
    ) -> tuple[list[SectorCapitalFlowModel], int]:
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
        if req.trade_date is not None and req.trade_date != "":
            filters[FilterOperators.EQ]["trade_date"] = req.trade_date
        if req.sector_code is not None and req.sector_code != "":
            filters[FilterOperators.EQ]["sector_code"] = req.sector_code
        if req.sector_name is not None and req.sector_name != "":
            filters[FilterOperators.LIKE]["sector_name"] = req.sector_name
        if req.sector_type is not None and req.sector_type != "":
            filters[FilterOperators.EQ]["sector_type"] = req.sector_type
        if req.main_inflow is not None and req.main_inflow != "":
            filters[FilterOperators.EQ]["main_inflow"] = req.main_inflow
        if req.main_outflow is not None and req.main_outflow != "":
            filters[FilterOperators.EQ]["main_outflow"] = req.main_outflow
        if req.main_net is not None and req.main_net != "":
            filters[FilterOperators.EQ]["main_net"] = req.main_net
        if req.total_inflow is not None and req.total_inflow != "":
            filters[FilterOperators.EQ]["total_inflow"] = req.total_inflow
        if req.total_outflow is not None and req.total_outflow != "":
            filters[FilterOperators.EQ]["total_outflow"] = req.total_outflow
        if req.total_net is not None and req.total_net != "":
            filters[FilterOperators.EQ]["total_net"] = req.total_net
        if req.stock_count is not None and req.stock_count != "":
            filters[FilterOperators.EQ]["stock_count"] = req.stock_count
        if req.rise_count is not None and req.rise_count != "":
            filters[FilterOperators.EQ]["rise_count"] = req.rise_count
        if req.fall_count is not None and req.fall_count != "":
            filters[FilterOperators.EQ]["fall_count"] = req.fall_count
        if req.flat_count is not None and req.flat_count != "":
            filters[FilterOperators.EQ]["flat_count"] = req.flat_count
        if req.sector_index is not None and req.sector_index != "":
            filters[FilterOperators.EQ]["sector_index"] = req.sector_index
        if req.change_percent is not None and req.change_percent != "":
            filters[FilterOperators.EQ]["change_percent"] = req.change_percent
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

    

    async def create_sector_capital_flow(self, req: CreateSectorCapitalFlowRequest) -> SectorCapitalFlowModel:
        sector_capital_flow: SectorCapitalFlowModel = SectorCapitalFlowModel(**req.sector_capital_flow.model_dump())
        return await self.save(data=sector_capital_flow)

    async def update_sector_capital_flow(self, req: UpdateSectorCapitalFlowRequest) -> SectorCapitalFlowModel:
        sector_capital_flow_record: SectorCapitalFlowModel = await self.retrieve_by_id(id=req.sector_capital_flow.id)
        if sector_capital_flow_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        sector_capital_flow_model = SectorCapitalFlowModel(**req.sector_capital_flow.model_dump(exclude_unset=True))
        await self.modify_by_id(data=sector_capital_flow_model)
        merged_data = {**sector_capital_flow_record.model_dump(), **sector_capital_flow_model.model_dump()}
        return SectorCapitalFlowModel(**merged_data)

    async def delete_sector_capital_flow(self, id: int) -> None:
        sector_capital_flow_record: SectorCapitalFlowModel = await self.retrieve_by_id(id=id)
        if sector_capital_flow_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_sector_capital_flows(self, ids: list[int]) -> list[SectorCapitalFlowModel]:
        sector_capital_flow_records = list[SectorCapitalFlowModel] = await self.retrieve_by_ids(ids=ids)
        if sector_capital_flow_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(sector_capital_flow_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in sector_capital_flow_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(sector_capital_flow_records)} != {str(not_exits_ids)}",
            )
        return sector_capital_flow_records

    async def batch_create_sector_capital_flows(
        self,
        *,
        req: BatchCreateSectorCapitalFlowsRequest,
    ) -> list[SectorCapitalFlowModel]:
        sector_capital_flow_list: list[CreateSectorCapitalFlow] = req.sector_capital_flows
        if not sector_capital_flow_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [SectorCapitalFlowModel(**sector_capital_flow.model_dump()) for sector_capital_flow in sector_capital_flow_list]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_sector_capital_flows(
        self, req: BatchUpdateSectorCapitalFlowsRequest
    ) -> list[SectorCapitalFlowModel]:
        sector_capital_flow: BatchUpdateSectorCapitalFlow = req.sector_capital_flow
        ids: list[int] = req.ids
        if not sector_capital_flow or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(
            ids=ids, data=sector_capital_flow.model_dump(exclude_none=True)
        )
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_sector_capital_flows(
        self, req: BatchPatchSectorCapitalFlowsRequest
    ) -> list[SectorCapitalFlowModel]:
        sector_capital_flows: list[UpdateSectorCapitalFlow] = req.sector_capital_flows
        if not sector_capital_flows:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            sector_capital_flow.model_dump(exclude_unset=True) for sector_capital_flow in sector_capital_flows
        ]
        await self.mapper.batch_update(items=update_data)
        sector_capital_flow_ids: list[int] = [sector_capital_flow.id for sector_capital_flow in sector_capital_flows]
        return await self.mapper.select_by_ids(ids=sector_capital_flow_ids)

    async def batch_delete_sector_capital_flows(self, req: BatchDeleteSectorCapitalFlowsRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_sector_capital_flows_template(self) -> StreamingResponse:
        file_name = "sector_capital_flow_import_tpl"
        return await excel_util.export_excel(
            schema=CreateSectorCapitalFlow, file_name=file_name
        )

    async def export_sector_capital_flows(self, req: ExportSectorCapitalFlowsRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        sector_capital_flow_list: list[SectorCapitalFlowModel] = await self.mapper.select_by_ids(ids=ids)
        if sector_capital_flow_list is None or len(sector_capital_flow_list) == 0:
            logger.error(f"No sector_capital_flows found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        sector_capital_flow_page_list = [ExportSectorCapitalFlow(**sector_capital_flow.model_dump()) for sector_capital_flow in sector_capital_flow_list]
        file_name = "sector_capital_flow_data_export"
        return await excel_util.export_excel(
            schema=ExportSectorCapitalFlow, file_name=file_name, data_list=sector_capital_flow_page_list
        )

    async def import_sector_capital_flows(self, req: ImportSectorCapitalFlowsRequest) -> list[ImportSectorCapitalFlow]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        sector_capital_flow_records = import_df.to_dict(orient="records")
        if sector_capital_flow_records is None or len(sector_capital_flow_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in sector_capital_flow_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        sector_capital_flow_import_list = []
        for sector_capital_flow_record in sector_capital_flow_records:
            try:
                sector_capital_flow_create = ImportSectorCapitalFlow(**sector_capital_flow_record)
                sector_capital_flow_import_list.append(sector_capital_flow_create)
            except ValidationError as e:
                valid_data = {
                    k: v
                    for k, v in sector_capital_flow_record.items()
                    if k in ImportSectorCapitalFlow.model_fields
                }
                sector_capital_flow_create = ImportSectorCapitalFlow.model_construct(**valid_data)
                sector_capital_flow_create.err_msg = ValidateService.get_validate_err_msg(e)
                sector_capital_flow_import_list.append(sector_capital_flow_create)
                return sector_capital_flow_import_list

        return sector_capital_flow_import_list