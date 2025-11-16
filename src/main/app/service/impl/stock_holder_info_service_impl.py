# SPDX-License-Identifier: MIT
"""StockHolderInfo domain service impl"""

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
from src.main.app.mapper.stock_holder_info_mapper import StockHolderInfoMapper
from src.main.app.model.stock_holder_info_model import StockHolderInfoModel
from src.main.app.schema.stock_holder_info_schema import (
    ListStockHolderInfosRequest,
    StockHolderInfo,
    CreateStockHolderInfoRequest,
    UpdateStockHolderInfoRequest,
    BatchDeleteStockHolderInfosRequest,
    ExportStockHolderInfosRequest,
    BatchCreateStockHolderInfosRequest,
    CreateStockHolderInfo,
    BatchUpdateStockHolderInfosRequest,
    UpdateStockHolderInfo,
    ImportStockHolderInfosRequest,
    ImportStockHolderInfo,
    ExportStockHolderInfo,
    BatchPatchStockHolderInfosRequest,
    BatchUpdateStockHolderInfo,
)
from src.main.app.service.stock_holder_info_service import StockHolderInfoService


class StockHolderInfoServiceImpl(BaseServiceImpl[StockHolderInfoMapper, StockHolderInfoModel], StockHolderInfoService):
    """
    Implementation of the StockHolderInfoService interface.
    """

    def __init__(self, mapper: StockHolderInfoMapper):
        """
        Initialize the StockHolderInfoServiceImpl instance.

        Args:
            mapper (StockHolderInfoMapper): The StockHolderInfoMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper, model=StockHolderInfoModel)
        self.mapper = mapper

    async def get_stock_holder_info(
        self,
        *,
        id: int,
    ) -> StockHolderInfoModel:
        stock_holder_info_record: StockHolderInfoModel = await self.mapper.select_by_id(id=id)
        if stock_holder_info_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return stock_holder_info_record

    async def list_stock_holder_infos(
        self, req: ListStockHolderInfosRequest
    ) -> tuple[list[StockHolderInfoModel], int]:
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
        if req.holder_name is not None and req.holder_name != "":
            filters[FilterOperators.LIKE]["holder_name"] = req.holder_name
        if req.holder_info is not None and req.holder_info != "":
            filters[FilterOperators.EQ]["holder_info"] = req.holder_info
        if req.holder_type is not None and req.holder_type != "":
            filters[FilterOperators.EQ]["holder_type"] = req.holder_type
        if req.share_amount is not None and req.share_amount != "":
            filters[FilterOperators.EQ]["share_amount"] = req.share_amount
        if req.share_ratio is not None and req.share_ratio != "":
            filters[FilterOperators.EQ]["share_ratio"] = req.share_ratio
        if req.change_amount is not None and req.change_amount != "":
            filters[FilterOperators.EQ]["change_amount"] = req.change_amount
        if req.change_type is not None and req.change_type != "":
            filters[FilterOperators.EQ]["change_type"] = req.change_type
        if req.report_date is not None and req.report_date != "":
            filters[FilterOperators.EQ]["report_date"] = req.report_date
        if req.is_top_ten is not None and req.is_top_ten != "":
            filters[FilterOperators.EQ]["is_top_ten"] = req.is_top_ten
        if req.ranking is not None and req.ranking != "":
            filters[FilterOperators.EQ]["ranking"] = req.ranking
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

    

    async def create_stock_holder_info(self, req: CreateStockHolderInfoRequest) -> StockHolderInfoModel:
        stock_holder_info: StockHolderInfoModel = StockHolderInfoModel(**req.stock_holder_info.model_dump())
        return await self.save(data=stock_holder_info)

    async def update_stock_holder_info(self, req: UpdateStockHolderInfoRequest) -> StockHolderInfoModel:
        stock_holder_info_record: StockHolderInfoModel = await self.retrieve_by_id(id=req.stock_holder_info.id)
        if stock_holder_info_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        stock_holder_info_model = StockHolderInfoModel(**req.stock_holder_info.model_dump(exclude_unset=True))
        await self.modify_by_id(data=stock_holder_info_model)
        merged_data = {**stock_holder_info_record.model_dump(), **stock_holder_info_model.model_dump()}
        return StockHolderInfoModel(**merged_data)

    async def delete_stock_holder_info(self, id: int) -> None:
        stock_holder_info_record: StockHolderInfoModel = await self.retrieve_by_id(id=id)
        if stock_holder_info_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_stock_holder_infos(self, ids: list[int]) -> list[StockHolderInfoModel]:
        stock_holder_info_records = list[StockHolderInfoModel] = await self.retrieve_by_ids(ids=ids)
        if stock_holder_info_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(stock_holder_info_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in stock_holder_info_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(stock_holder_info_records)} != {str(not_exits_ids)}",
            )
        return stock_holder_info_records

    async def batch_create_stock_holder_infos(
        self,
        *,
        req: BatchCreateStockHolderInfosRequest,
    ) -> list[StockHolderInfoModel]:
        stock_holder_info_list: list[CreateStockHolderInfo] = req.stock_holder_infos
        if not stock_holder_info_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [StockHolderInfoModel(**stock_holder_info.model_dump()) for stock_holder_info in stock_holder_info_list]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_stock_holder_infos(
        self, req: BatchUpdateStockHolderInfosRequest
    ) -> list[StockHolderInfoModel]:
        stock_holder_info: BatchUpdateStockHolderInfo = req.stock_holder_info
        ids: list[int] = req.ids
        if not stock_holder_info or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(
            ids=ids, data=stock_holder_info.model_dump(exclude_none=True)
        )
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_stock_holder_infos(
        self, req: BatchPatchStockHolderInfosRequest
    ) -> list[StockHolderInfoModel]:
        stock_holder_infos: list[UpdateStockHolderInfo] = req.stock_holder_infos
        if not stock_holder_infos:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            stock_holder_info.model_dump(exclude_unset=True) for stock_holder_info in stock_holder_infos
        ]
        await self.mapper.batch_update(items=update_data)
        stock_holder_info_ids: list[int] = [stock_holder_info.id for stock_holder_info in stock_holder_infos]
        return await self.mapper.select_by_ids(ids=stock_holder_info_ids)

    async def batch_delete_stock_holder_infos(self, req: BatchDeleteStockHolderInfosRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_stock_holder_infos_template(self) -> StreamingResponse:
        file_name = "stock_holder_info_import_tpl"
        return await excel_util.export_excel(
            schema=CreateStockHolderInfo, file_name=file_name
        )

    async def export_stock_holder_infos(self, req: ExportStockHolderInfosRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        stock_holder_info_list: list[StockHolderInfoModel] = await self.mapper.select_by_ids(ids=ids)
        if stock_holder_info_list is None or len(stock_holder_info_list) == 0:
            logger.error(f"No stock_holder_infos found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        stock_holder_info_page_list = [ExportStockHolderInfo(**stock_holder_info.model_dump()) for stock_holder_info in stock_holder_info_list]
        file_name = "stock_holder_info_data_export"
        return await excel_util.export_excel(
            schema=ExportStockHolderInfo, file_name=file_name, data_list=stock_holder_info_page_list
        )

    async def import_stock_holder_infos(self, req: ImportStockHolderInfosRequest) -> list[ImportStockHolderInfo]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        stock_holder_info_records = import_df.to_dict(orient="records")
        if stock_holder_info_records is None or len(stock_holder_info_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in stock_holder_info_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        stock_holder_info_import_list = []
        for stock_holder_info_record in stock_holder_info_records:
            try:
                stock_holder_info_create = ImportStockHolderInfo(**stock_holder_info_record)
                stock_holder_info_import_list.append(stock_holder_info_create)
            except ValidationError as e:
                valid_data = {
                    k: v
                    for k, v in stock_holder_info_record.items()
                    if k in ImportStockHolderInfo.model_fields
                }
                stock_holder_info_create = ImportStockHolderInfo.model_construct(**valid_data)
                stock_holder_info_create.err_msg = ValidateService.get_validate_err_msg(e)
                stock_holder_info_import_list.append(stock_holder_info_create)
                return stock_holder_info_import_list

        return stock_holder_info_import_list