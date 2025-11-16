# SPDX-License-Identifier: MIT
"""StockDailyInfo domain service impl"""

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
from src.main.app.mapper.stock_daily_info_mapper import StockDailyInfoMapper
from src.main.app.model.stock_daily_info_model import StockDailyInfoModel
from src.main.app.schema.stock_daily_info_schema import (
    ListStockDailyInfosRequest,
    StockDailyInfo,
    CreateStockDailyInfoRequest,
    UpdateStockDailyInfoRequest,
    BatchDeleteStockDailyInfosRequest,
    ExportStockDailyInfosRequest,
    BatchCreateStockDailyInfosRequest,
    CreateStockDailyInfo,
    BatchUpdateStockDailyInfosRequest,
    UpdateStockDailyInfo,
    ImportStockDailyInfosRequest,
    ImportStockDailyInfo,
    ExportStockDailyInfo,
    BatchPatchStockDailyInfosRequest,
    BatchUpdateStockDailyInfo,
)
from src.main.app.service.stock_daily_info_service import StockDailyInfoService


class StockDailyInfoServiceImpl(BaseServiceImpl[StockDailyInfoMapper, StockDailyInfoModel], StockDailyInfoService):
    """
    Implementation of the StockDailyInfoService interface.
    """

    def __init__(self, mapper: StockDailyInfoMapper):
        """
        Initialize the StockDailyInfoServiceImpl instance.

        Args:
            mapper (StockDailyInfoMapper): The StockDailyInfoMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper, model=StockDailyInfoModel)
        self.mapper = mapper

    async def get_stock_daily_info(
        self,
        *,
        id: int,
    ) -> StockDailyInfoModel:
        stock_daily_info_record: StockDailyInfoModel = await self.mapper.select_by_id(id=id)
        if stock_daily_info_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return stock_daily_info_record

    async def list_stock_daily_infos(
        self, req: ListStockDailyInfosRequest
    ) -> tuple[list[StockDailyInfoModel], int]:
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
        if req.trade_date is not None and req.trade_date != "":
            filters[FilterOperators.EQ]["trade_date"] = req.trade_date
        if req.open_price is not None and req.open_price != "":
            filters[FilterOperators.EQ]["open_price"] = req.open_price
        if req.close_price is not None and req.close_price != "":
            filters[FilterOperators.EQ]["close_price"] = req.close_price
        if req.high_price is not None and req.high_price != "":
            filters[FilterOperators.EQ]["high_price"] = req.high_price
        if req.low_price is not None and req.low_price != "":
            filters[FilterOperators.EQ]["low_price"] = req.low_price
        if req.volume is not None and req.volume != "":
            filters[FilterOperators.EQ]["volume"] = req.volume
        if req.turnover is not None and req.turnover != "":
            filters[FilterOperators.EQ]["turnover"] = req.turnover
        if req.change_amount is not None and req.change_amount != "":
            filters[FilterOperators.EQ]["change_amount"] = req.change_amount
        if req.change_rate is not None and req.change_rate != "":
            filters[FilterOperators.EQ]["change_rate"] = req.change_rate
        if req.pe_ratio is not None and req.pe_ratio != "":
            filters[FilterOperators.EQ]["pe_ratio"] = req.pe_ratio
        if req.pb_ratio is not None and req.pb_ratio != "":
            filters[FilterOperators.EQ]["pb_ratio"] = req.pb_ratio
        if req.market_cap is not None and req.market_cap != "":
            filters[FilterOperators.EQ]["market_cap"] = req.market_cap
        if req.circulating_market_cap is not None and req.circulating_market_cap != "":
            filters[FilterOperators.EQ]["circulating_market_cap"] = req.circulating_market_cap
        if req.turnover_rate is not None and req.turnover_rate != "":
            filters[FilterOperators.EQ]["turnover_rate"] = req.turnover_rate
        if req.bid_price1 is not None and req.bid_price1 != "":
            filters[FilterOperators.EQ]["bid_price1"] = req.bid_price1
        if req.bid_price2 is not None and req.bid_price2 != "":
            filters[FilterOperators.EQ]["bid_price2"] = req.bid_price2
        if req.bid_price3 is not None and req.bid_price3 != "":
            filters[FilterOperators.EQ]["bid_price3"] = req.bid_price3
        if req.bid_price4 is not None and req.bid_price4 != "":
            filters[FilterOperators.EQ]["bid_price4"] = req.bid_price4
        if req.bid_price5 is not None and req.bid_price5 != "":
            filters[FilterOperators.EQ]["bid_price5"] = req.bid_price5
        if req.bid_volume1 is not None and req.bid_volume1 != "":
            filters[FilterOperators.EQ]["bid_volume1"] = req.bid_volume1
        if req.bid_volume2 is not None and req.bid_volume2 != "":
            filters[FilterOperators.EQ]["bid_volume2"] = req.bid_volume2
        if req.bid_volume3 is not None and req.bid_volume3 != "":
            filters[FilterOperators.EQ]["bid_volume3"] = req.bid_volume3
        if req.bid_volume4 is not None and req.bid_volume4 != "":
            filters[FilterOperators.EQ]["bid_volume4"] = req.bid_volume4
        if req.bid_volume5 is not None and req.bid_volume5 != "":
            filters[FilterOperators.EQ]["bid_volume5"] = req.bid_volume5
        if req.ask_price1 is not None and req.ask_price1 != "":
            filters[FilterOperators.EQ]["ask_price1"] = req.ask_price1
        if req.ask_price2 is not None and req.ask_price2 != "":
            filters[FilterOperators.EQ]["ask_price2"] = req.ask_price2
        if req.ask_price3 is not None and req.ask_price3 != "":
            filters[FilterOperators.EQ]["ask_price3"] = req.ask_price3
        if req.ask_price4 is not None and req.ask_price4 != "":
            filters[FilterOperators.EQ]["ask_price4"] = req.ask_price4
        if req.ask_price5 is not None and req.ask_price5 != "":
            filters[FilterOperators.EQ]["ask_price5"] = req.ask_price5
        if req.ask_volume1 is not None and req.ask_volume1 != "":
            filters[FilterOperators.EQ]["ask_volume1"] = req.ask_volume1
        if req.ask_volume2 is not None and req.ask_volume2 != "":
            filters[FilterOperators.EQ]["ask_volume2"] = req.ask_volume2
        if req.ask_volume3 is not None and req.ask_volume3 != "":
            filters[FilterOperators.EQ]["ask_volume3"] = req.ask_volume3
        if req.ask_volume4 is not None and req.ask_volume4 != "":
            filters[FilterOperators.EQ]["ask_volume4"] = req.ask_volume4
        if req.ask_volume5 is not None and req.ask_volume5 != "":
            filters[FilterOperators.EQ]["ask_volume5"] = req.ask_volume5
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

    

    async def create_stock_daily_info(self, req: CreateStockDailyInfoRequest) -> StockDailyInfoModel:
        stock_daily_info: StockDailyInfoModel = StockDailyInfoModel(**req.stock_daily_info.model_dump())
        return await self.save(data=stock_daily_info)

    async def update_stock_daily_info(self, req: UpdateStockDailyInfoRequest) -> StockDailyInfoModel:
        stock_daily_info_record: StockDailyInfoModel = await self.retrieve_by_id(id=req.stock_daily_info.id)
        if stock_daily_info_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        stock_daily_info_model = StockDailyInfoModel(**req.stock_daily_info.model_dump(exclude_unset=True))
        await self.modify_by_id(data=stock_daily_info_model)
        merged_data = {**stock_daily_info_record.model_dump(), **stock_daily_info_model.model_dump()}
        return StockDailyInfoModel(**merged_data)

    async def delete_stock_daily_info(self, id: int) -> None:
        stock_daily_info_record: StockDailyInfoModel = await self.retrieve_by_id(id=id)
        if stock_daily_info_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_stock_daily_infos(self, ids: list[int]) -> list[StockDailyInfoModel]:
        stock_daily_info_records = list[StockDailyInfoModel] = await self.retrieve_by_ids(ids=ids)
        if stock_daily_info_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(stock_daily_info_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in stock_daily_info_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(stock_daily_info_records)} != {str(not_exits_ids)}",
            )
        return stock_daily_info_records

    async def batch_create_stock_daily_infos(
        self,
        *,
        req: BatchCreateStockDailyInfosRequest,
    ) -> list[StockDailyInfoModel]:
        stock_daily_info_list: list[CreateStockDailyInfo] = req.stock_daily_infos
        if not stock_daily_info_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [StockDailyInfoModel(**stock_daily_info.model_dump()) for stock_daily_info in stock_daily_info_list]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_stock_daily_infos(
        self, req: BatchUpdateStockDailyInfosRequest
    ) -> list[StockDailyInfoModel]:
        stock_daily_info: BatchUpdateStockDailyInfo = req.stock_daily_info
        ids: list[int] = req.ids
        if not stock_daily_info or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(
            ids=ids, data=stock_daily_info.model_dump(exclude_none=True)
        )
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_stock_daily_infos(
        self, req: BatchPatchStockDailyInfosRequest
    ) -> list[StockDailyInfoModel]:
        stock_daily_infos: list[UpdateStockDailyInfo] = req.stock_daily_infos
        if not stock_daily_infos:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            stock_daily_info.model_dump(exclude_unset=True) for stock_daily_info in stock_daily_infos
        ]
        await self.mapper.batch_update(items=update_data)
        stock_daily_info_ids: list[int] = [stock_daily_info.id for stock_daily_info in stock_daily_infos]
        return await self.mapper.select_by_ids(ids=stock_daily_info_ids)

    async def batch_delete_stock_daily_infos(self, req: BatchDeleteStockDailyInfosRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_stock_daily_infos_template(self) -> StreamingResponse:
        file_name = "stock_daily_info_import_tpl"
        return await excel_util.export_excel(
            schema=CreateStockDailyInfo, file_name=file_name
        )

    async def export_stock_daily_infos(self, req: ExportStockDailyInfosRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        stock_daily_info_list: list[StockDailyInfoModel] = await self.mapper.select_by_ids(ids=ids)
        if stock_daily_info_list is None or len(stock_daily_info_list) == 0:
            logger.error(f"No stock_daily_infos found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        stock_daily_info_page_list = [ExportStockDailyInfo(**stock_daily_info.model_dump()) for stock_daily_info in stock_daily_info_list]
        file_name = "stock_daily_info_data_export"
        return await excel_util.export_excel(
            schema=ExportStockDailyInfo, file_name=file_name, data_list=stock_daily_info_page_list
        )

    async def import_stock_daily_infos(self, req: ImportStockDailyInfosRequest) -> list[ImportStockDailyInfo]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        stock_daily_info_records = import_df.to_dict(orient="records")
        if stock_daily_info_records is None or len(stock_daily_info_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in stock_daily_info_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        stock_daily_info_import_list = []
        for stock_daily_info_record in stock_daily_info_records:
            try:
                stock_daily_info_create = ImportStockDailyInfo(**stock_daily_info_record)
                stock_daily_info_import_list.append(stock_daily_info_create)
            except ValidationError as e:
                valid_data = {
                    k: v
                    for k, v in stock_daily_info_record.items()
                    if k in ImportStockDailyInfo.model_fields
                }
                stock_daily_info_create = ImportStockDailyInfo.model_construct(**valid_data)
                stock_daily_info_create.err_msg = ValidateService.get_validate_err_msg(e)
                stock_daily_info_import_list.append(stock_daily_info_create)
                return stock_daily_info_import_list

        return stock_daily_info_import_list