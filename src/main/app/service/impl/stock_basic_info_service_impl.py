# SPDX-License-Identifier: MIT
"""StockBasicInfo domain service impl"""

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
from src.main.app.mapper.stock_basic_info_mapper import StockBasicInfoMapper
from src.main.app.model.stock_basic_info_model import StockBasicInfoModel
from src.main.app.schema.stock_basic_info_schema import (
    ListStockBasicInfosRequest,
    StockBasicInfo,
    CreateStockBasicInfoRequest,
    UpdateStockBasicInfoRequest,
    BatchDeleteStockBasicInfosRequest,
    ExportStockBasicInfosRequest,
    BatchCreateStockBasicInfosRequest,
    CreateStockBasicInfo,
    BatchUpdateStockBasicInfosRequest,
    UpdateStockBasicInfo,
    ImportStockBasicInfosRequest,
    ImportStockBasicInfo,
    ExportStockBasicInfo,
    BatchPatchStockBasicInfosRequest,
    BatchUpdateStockBasicInfo,
)
from src.main.app.service.stock_basic_info_service import StockBasicInfoService


class StockBasicInfoServiceImpl(BaseServiceImpl[StockBasicInfoMapper, StockBasicInfoModel], StockBasicInfoService):
    """
    Implementation of the StockBasicInfoService interface.
    """

    def __init__(self, mapper: StockBasicInfoMapper):
        """
        Initialize the StockBasicInfoServiceImpl instance.

        Args:
            mapper (StockBasicInfoMapper): The StockBasicInfoMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper, model=StockBasicInfoModel)
        self.mapper = mapper

    async def get_stock_basic_info(
        self,
        *,
        id: int,
    ) -> StockBasicInfoModel:
        stock_basic_info_record: StockBasicInfoModel = await self.mapper.select_by_id(id=id)
        if stock_basic_info_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return stock_basic_info_record

    async def list_stock_basic_infos(
        self, req: ListStockBasicInfosRequest
    ) -> tuple[list[StockBasicInfoModel], int]:
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
        if req.symbol is not None and req.symbol != "":
            filters[FilterOperators.EQ]["symbol"] = req.symbol
        if req.symbol_full is not None and req.symbol_full != "":
            filters[FilterOperators.EQ]["symbol_full"] = req.symbol_full
        if req.name is not None and req.name != "":
            filters[FilterOperators.LIKE]["name"] = req.name
        if req.exchange is not None and req.exchange != "":
            filters[FilterOperators.EQ]["exchange"] = req.exchange
        if req.listing_date is not None and req.listing_date != "":
            filters[FilterOperators.EQ]["listing_date"] = req.listing_date
        if req.industry is not None and req.industry != "":
            filters[FilterOperators.EQ]["industry"] = req.industry
        if req.industry_gy is not None and req.industry_gy != "":
            filters[FilterOperators.EQ]["industry_gy"] = req.industry_gy
        if req.province is not None and req.province != "":
            filters[FilterOperators.EQ]["province"] = req.province
        if req.city is not None and req.city != "":
            filters[FilterOperators.EQ]["city"] = req.city
        if req.website is not None and req.website != "":
            filters[FilterOperators.EQ]["website"] = req.website
        if req.price_tick is not None and req.price_tick != "":
            filters[FilterOperators.EQ]["price_tick"] = req.price_tick
        if req.data_source is not None and req.data_source != "":
            filters[FilterOperators.EQ]["data_source"] = req.data_source
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

    

    async def create_stock_basic_info(self, req: CreateStockBasicInfoRequest) -> StockBasicInfoModel:
        stock_basic_info: StockBasicInfoModel = StockBasicInfoModel(**req.stock_basic_info.model_dump())
        return await self.save(data=stock_basic_info)

    async def update_stock_basic_info(self, req: UpdateStockBasicInfoRequest) -> StockBasicInfoModel:
        stock_basic_info_record: StockBasicInfoModel = await self.retrieve_by_id(id=req.stock_basic_info.id)
        if stock_basic_info_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        stock_basic_info_model = StockBasicInfoModel(**req.stock_basic_info.model_dump(exclude_unset=True))
        await self.modify_by_id(data=stock_basic_info_model)
        merged_data = {**stock_basic_info_record.model_dump(), **stock_basic_info_model.model_dump()}
        return StockBasicInfoModel(**merged_data)

    async def delete_stock_basic_info(self, id: int) -> None:
        stock_basic_info_record: StockBasicInfoModel = await self.retrieve_by_id(id=id)
        if stock_basic_info_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_stock_basic_infos(self, ids: list[int]) -> list[StockBasicInfoModel]:
        stock_basic_info_records = list[StockBasicInfoModel] = await self.retrieve_by_ids(ids=ids)
        if stock_basic_info_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(stock_basic_info_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in stock_basic_info_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(stock_basic_info_records)} != {str(not_exits_ids)}",
            )
        return stock_basic_info_records

    async def batch_create_stock_basic_infos(
        self,
        *,
        req: BatchCreateStockBasicInfosRequest,
    ) -> list[StockBasicInfoModel]:
        stock_basic_info_list: list[CreateStockBasicInfo] = req.stock_basic_infos
        if not stock_basic_info_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [StockBasicInfoModel(**stock_basic_info.model_dump()) for stock_basic_info in stock_basic_info_list]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_stock_basic_infos(
        self, req: BatchUpdateStockBasicInfosRequest
    ) -> list[StockBasicInfoModel]:
        stock_basic_info: BatchUpdateStockBasicInfo = req.stock_basic_info
        ids: list[int] = req.ids
        if not stock_basic_info or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(
            ids=ids, data=stock_basic_info.model_dump(exclude_none=True)
        )
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_stock_basic_infos(
        self, req: BatchPatchStockBasicInfosRequest
    ) -> list[StockBasicInfoModel]:
        stock_basic_infos: list[UpdateStockBasicInfo] = req.stock_basic_infos
        if not stock_basic_infos:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            stock_basic_info.model_dump(exclude_unset=True) for stock_basic_info in stock_basic_infos
        ]
        await self.mapper.batch_update(items=update_data)
        stock_basic_info_ids: list[int] = [stock_basic_info.id for stock_basic_info in stock_basic_infos]
        return await self.mapper.select_by_ids(ids=stock_basic_info_ids)

    async def batch_delete_stock_basic_infos(self, req: BatchDeleteStockBasicInfosRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_stock_basic_infos_template(self) -> StreamingResponse:
        file_name = "stock_basic_info_import_tpl"
        return await excel_util.export_excel(
            schema=CreateStockBasicInfo, file_name=file_name
        )

    async def export_stock_basic_infos(self, req: ExportStockBasicInfosRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        stock_basic_info_list: list[StockBasicInfoModel] = await self.mapper.select_by_ids(ids=ids)
        if stock_basic_info_list is None or len(stock_basic_info_list) == 0:
            logger.error(f"No stock_basic_infos found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        stock_basic_info_page_list = [ExportStockBasicInfo(**stock_basic_info.model_dump()) for stock_basic_info in stock_basic_info_list]
        file_name = "stock_basic_info_data_export"
        return await excel_util.export_excel(
            schema=ExportStockBasicInfo, file_name=file_name, data_list=stock_basic_info_page_list
        )

    async def import_stock_basic_infos(self, req: ImportStockBasicInfosRequest) -> list[ImportStockBasicInfo]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        stock_basic_info_records = import_df.to_dict(orient="records")
        if stock_basic_info_records is None or len(stock_basic_info_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in stock_basic_info_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        stock_basic_info_import_list = []
        for stock_basic_info_record in stock_basic_info_records:
            try:
                stock_basic_info_create = ImportStockBasicInfo(**stock_basic_info_record)
                stock_basic_info_import_list.append(stock_basic_info_create)
            except ValidationError as e:
                valid_data = {
                    k: v
                    for k, v in stock_basic_info_record.items()
                    if k in ImportStockBasicInfo.model_fields
                }
                stock_basic_info_create = ImportStockBasicInfo.model_construct(**valid_data)
                stock_basic_info_create.err_msg = ValidateService.get_validate_err_msg(e)
                stock_basic_info_import_list.append(stock_basic_info_create)
                return stock_basic_info_import_list

        return stock_basic_info_import_list