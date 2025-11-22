# SPDX-License-Identifier: MIT
"""StockCapitalFlow domain service impl"""

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
from src.main.app.mapper.stock_capital_flow_mapper import StockCapitalFlowMapper
from src.main.app.model.stock_capital_flow_model import StockCapitalFlowModel
from src.main.app.schema.stock_capital_flow_schema import (
    ListStockCapitalFlowsRequest,
    StockCapitalFlow,
    CreateStockCapitalFlowRequest,
    UpdateStockCapitalFlowRequest,
    BatchDeleteStockCapitalFlowsRequest,
    ExportStockCapitalFlowsRequest,
    BatchCreateStockCapitalFlowsRequest,
    CreateStockCapitalFlow,
    BatchUpdateStockCapitalFlowsRequest,
    UpdateStockCapitalFlow,
    ImportStockCapitalFlowsRequest,
    ImportStockCapitalFlow,
    ExportStockCapitalFlow,
    BatchPatchStockCapitalFlowsRequest,
    BatchUpdateStockCapitalFlow,
)
from src.main.app.service.stock_capital_flow_service import StockCapitalFlowService


class StockCapitalFlowServiceImpl(BaseServiceImpl[StockCapitalFlowMapper, StockCapitalFlowModel], StockCapitalFlowService):
    """
    Implementation of the StockCapitalFlowService interface.
    """

    def __init__(self, mapper: StockCapitalFlowMapper):
        """
        Initialize the StockCapitalFlowServiceImpl instance.

        Args:
            mapper (StockCapitalFlowMapper): The StockCapitalFlowMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper, model=StockCapitalFlowModel)
        self.mapper = mapper

    async def get_stock_capital_flow(
        self,
        *,
        id: int,
    ) -> StockCapitalFlowModel:
        stock_capital_flow_record: StockCapitalFlowModel = await self.mapper.select_by_id(id=id)
        if stock_capital_flow_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return stock_capital_flow_record

    async def list_stock_capital_flows(
        self, req: ListStockCapitalFlowsRequest
    ) -> tuple[list[StockCapitalFlowModel], int]:
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
        if req.stock_symbol_full is not None and req.stock_symbol_full != "":
            filters[FilterOperators.EQ]["stock_symbol_full"] = req.stock_symbol_full
        if req.exchange is not None and req.exchange != "":
            filters[FilterOperators.EQ]["exchange"] = req.exchange
        if req.main_inflow is not None and req.main_inflow != "":
            filters[FilterOperators.EQ]["main_inflow"] = req.main_inflow
        if req.main_outflow is not None and req.main_outflow != "":
            filters[FilterOperators.EQ]["main_outflow"] = req.main_outflow
        if req.main_net is not None and req.main_net != "":
            filters[FilterOperators.EQ]["main_net"] = req.main_net
        if req.retail_inflow is not None and req.retail_inflow != "":
            filters[FilterOperators.EQ]["retail_inflow"] = req.retail_inflow
        if req.retail_outflow is not None and req.retail_outflow != "":
            filters[FilterOperators.EQ]["retail_outflow"] = req.retail_outflow
        if req.retail_net is not None and req.retail_net != "":
            filters[FilterOperators.EQ]["retail_net"] = req.retail_net
        if req.total_inflow is not None and req.total_inflow != "":
            filters[FilterOperators.EQ]["total_inflow"] = req.total_inflow
        if req.total_outflow is not None and req.total_outflow != "":
            filters[FilterOperators.EQ]["total_outflow"] = req.total_outflow
        if req.total_net is not None and req.total_net != "":
            filters[FilterOperators.EQ]["total_net"] = req.total_net
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

    

    async def create_stock_capital_flow(self, req: CreateStockCapitalFlowRequest) -> StockCapitalFlowModel:
        stock_capital_flow: StockCapitalFlowModel = StockCapitalFlowModel(**req.stock_capital_flow.model_dump())
        return await self.save(data=stock_capital_flow)

    async def update_stock_capital_flow(self, req: UpdateStockCapitalFlowRequest) -> StockCapitalFlowModel:
        stock_capital_flow_record: StockCapitalFlowModel = await self.retrieve_by_id(id=req.stock_capital_flow.id)
        if stock_capital_flow_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        stock_capital_flow_model = StockCapitalFlowModel(**req.stock_capital_flow.model_dump(exclude_unset=True))
        await self.modify_by_id(data=stock_capital_flow_model)
        merged_data = {**stock_capital_flow_record.model_dump(), **stock_capital_flow_model.model_dump()}
        return StockCapitalFlowModel(**merged_data)

    async def delete_stock_capital_flow(self, id: int) -> None:
        stock_capital_flow_record: StockCapitalFlowModel = await self.retrieve_by_id(id=id)
        if stock_capital_flow_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_stock_capital_flows(self, ids: list[int]) -> list[StockCapitalFlowModel]:
        stock_capital_flow_records = list[StockCapitalFlowModel] = await self.retrieve_by_ids(ids=ids)
        if stock_capital_flow_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(stock_capital_flow_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in stock_capital_flow_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(stock_capital_flow_records)} != {str(not_exits_ids)}",
            )
        return stock_capital_flow_records

    async def batch_create_stock_capital_flows(
        self,
        *,
        req: BatchCreateStockCapitalFlowsRequest,
    ) -> list[StockCapitalFlowModel]:
        stock_capital_flow_list: list[CreateStockCapitalFlow] = req.stock_capital_flows
        if not stock_capital_flow_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [StockCapitalFlowModel(**stock_capital_flow.model_dump()) for stock_capital_flow in stock_capital_flow_list]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_stock_capital_flows(
        self, req: BatchUpdateStockCapitalFlowsRequest
    ) -> list[StockCapitalFlowModel]:
        stock_capital_flow: BatchUpdateStockCapitalFlow = req.stock_capital_flow
        ids: list[int] = req.ids
        if not stock_capital_flow or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(
            ids=ids, data=stock_capital_flow.model_dump(exclude_none=True)
        )
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_stock_capital_flows(
        self, req: BatchPatchStockCapitalFlowsRequest
    ) -> list[StockCapitalFlowModel]:
        stock_capital_flows: list[UpdateStockCapitalFlow] = req.stock_capital_flows
        if not stock_capital_flows:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            stock_capital_flow.model_dump(exclude_unset=True) for stock_capital_flow in stock_capital_flows
        ]
        await self.mapper.batch_update(items=update_data)
        stock_capital_flow_ids: list[int] = [stock_capital_flow.id for stock_capital_flow in stock_capital_flows]
        return await self.mapper.select_by_ids(ids=stock_capital_flow_ids)

    async def batch_delete_stock_capital_flows(self, req: BatchDeleteStockCapitalFlowsRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_stock_capital_flows_template(self) -> StreamingResponse:
        file_name = "stock_capital_flow_import_tpl"
        return await excel_util.export_excel(
            schema=CreateStockCapitalFlow, file_name=file_name
        )

    async def export_stock_capital_flows(self, req: ExportStockCapitalFlowsRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        stock_capital_flow_list: list[StockCapitalFlowModel] = await self.mapper.select_by_ids(ids=ids)
        if stock_capital_flow_list is None or len(stock_capital_flow_list) == 0:
            logger.error(f"No stock_capital_flows found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        stock_capital_flow_page_list = [ExportStockCapitalFlow(**stock_capital_flow.model_dump()) for stock_capital_flow in stock_capital_flow_list]
        file_name = "stock_capital_flow_data_export"
        return await excel_util.export_excel(
            schema=ExportStockCapitalFlow, file_name=file_name, data_list=stock_capital_flow_page_list
        )

    async def import_stock_capital_flows(self, req: ImportStockCapitalFlowsRequest) -> list[ImportStockCapitalFlow]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        stock_capital_flow_records = import_df.to_dict(orient="records")
        if stock_capital_flow_records is None or len(stock_capital_flow_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in stock_capital_flow_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        stock_capital_flow_import_list = []
        for stock_capital_flow_record in stock_capital_flow_records:
            try:
                stock_capital_flow_create = ImportStockCapitalFlow(**stock_capital_flow_record)
                stock_capital_flow_import_list.append(stock_capital_flow_create)
            except ValidationError as e:
                valid_data = {
                    k: v
                    for k, v in stock_capital_flow_record.items()
                    if k in ImportStockCapitalFlow.model_fields
                }
                stock_capital_flow_create = ImportStockCapitalFlow.model_construct(**valid_data)
                stock_capital_flow_create.err_msg = ValidateService.get_validate_err_msg(e)
                stock_capital_flow_import_list.append(stock_capital_flow_create)
                return stock_capital_flow_import_list

        return stock_capital_flow_import_list