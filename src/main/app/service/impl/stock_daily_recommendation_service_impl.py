# SPDX-License-Identifier: MIT
"""StockDailyRecommendation domain service impl"""

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
from src.main.app.mapper.stock_daily_recommendation_mapper import StockDailyRecommendationMapper
from src.main.app.model.stock_daily_recommendation_model import StockDailyRecommendationModel
from src.main.app.schema.stock_daily_recommendation_schema import (
    ListStockDailyRecommendationsRequest,
    StockDailyRecommendation,
    CreateStockDailyRecommendationRequest,
    UpdateStockDailyRecommendationRequest,
    BatchDeleteStockDailyRecommendationsRequest,
    ExportStockDailyRecommendationsRequest,
    BatchCreateStockDailyRecommendationsRequest,
    CreateStockDailyRecommendation,
    BatchUpdateStockDailyRecommendationsRequest,
    UpdateStockDailyRecommendation,
    ImportStockDailyRecommendationsRequest,
    ImportStockDailyRecommendation,
    ExportStockDailyRecommendation,
    BatchPatchStockDailyRecommendationsRequest,
    BatchUpdateStockDailyRecommendation,
)
from src.main.app.service.stock_daily_recommendation_service import StockDailyRecommendationService


class StockDailyRecommendationServiceImpl(BaseServiceImpl[StockDailyRecommendationMapper, StockDailyRecommendationModel], StockDailyRecommendationService):
    """
    Implementation of the StockDailyRecommendationService interface.
    """

    def __init__(self, mapper: StockDailyRecommendationMapper):
        """
        Initialize the StockDailyRecommendationServiceImpl instance.

        Args:
            mapper (StockDailyRecommendationMapper): The StockDailyRecommendationMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper, model=StockDailyRecommendationModel)
        self.mapper = mapper

    async def get_stock_daily_recommendation(
        self,
        *,
        id: int,
    ) -> StockDailyRecommendationModel:
        stock_daily_recommendation_record: StockDailyRecommendationModel = await self.mapper.select_by_id(id=id)
        if stock_daily_recommendation_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return stock_daily_recommendation_record

    async def list_stock_daily_recommendations(
        self, req: ListStockDailyRecommendationsRequest
    ) -> tuple[list[StockDailyRecommendationModel], int]:
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
        if req.recommend_date is not None and req.recommend_date != "":
            filters[FilterOperators.EQ]["recommend_date"] = req.recommend_date
        if req.recommend_level is not None and req.recommend_level != "":
            filters[FilterOperators.EQ]["recommend_level"] = req.recommend_level
        if req.price is not None and req.price != "":
            filters[FilterOperators.EQ]["price"] = req.price
        if req.target_price is not None and req.target_price != "":
            filters[FilterOperators.EQ]["target_price"] = req.target_price
        if req.recommend_reason is not None and req.recommend_reason != "":
            filters[FilterOperators.EQ]["recommend_reason"] = req.recommend_reason
        if req.analyst is not None and req.analyst != "":
            filters[FilterOperators.EQ]["analyst"] = req.analyst
        if req.institution is not None and req.institution != "":
            filters[FilterOperators.EQ]["institution"] = req.institution
        if req.risk_level is not None and req.risk_level != "":
            filters[FilterOperators.EQ]["risk_level"] = req.risk_level
        if req.validity_period is not None and req.validity_period != "":
            filters[FilterOperators.EQ]["validity_period"] = req.validity_period
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

    

    async def create_stock_daily_recommendation(self, req: CreateStockDailyRecommendationRequest) -> StockDailyRecommendationModel:
        stock_daily_recommendation: StockDailyRecommendationModel = StockDailyRecommendationModel(**req.stock_daily_recommendation.model_dump())
        return await self.save(data=stock_daily_recommendation)

    async def update_stock_daily_recommendation(self, req: UpdateStockDailyRecommendationRequest) -> StockDailyRecommendationModel:
        stock_daily_recommendation_record: StockDailyRecommendationModel = await self.retrieve_by_id(id=req.stock_daily_recommendation.id)
        if stock_daily_recommendation_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        stock_daily_recommendation_model = StockDailyRecommendationModel(**req.stock_daily_recommendation.model_dump(exclude_unset=True))
        await self.modify_by_id(data=stock_daily_recommendation_model)
        merged_data = {**stock_daily_recommendation_record.model_dump(), **stock_daily_recommendation_model.model_dump()}
        return StockDailyRecommendationModel(**merged_data)

    async def delete_stock_daily_recommendation(self, id: int) -> None:
        stock_daily_recommendation_record: StockDailyRecommendationModel = await self.retrieve_by_id(id=id)
        if stock_daily_recommendation_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_stock_daily_recommendations(self, ids: list[int]) -> list[StockDailyRecommendationModel]:
        stock_daily_recommendation_records = list[StockDailyRecommendationModel] = await self.retrieve_by_ids(ids=ids)
        if stock_daily_recommendation_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(stock_daily_recommendation_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in stock_daily_recommendation_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(stock_daily_recommendation_records)} != {str(not_exits_ids)}",
            )
        return stock_daily_recommendation_records

    async def batch_create_stock_daily_recommendations(
        self,
        *,
        req: BatchCreateStockDailyRecommendationsRequest,
    ) -> list[StockDailyRecommendationModel]:
        stock_daily_recommendation_list: list[CreateStockDailyRecommendation] = req.stock_daily_recommendations
        if not stock_daily_recommendation_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [StockDailyRecommendationModel(**stock_daily_recommendation.model_dump()) for stock_daily_recommendation in stock_daily_recommendation_list]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_stock_daily_recommendations(
        self, req: BatchUpdateStockDailyRecommendationsRequest
    ) -> list[StockDailyRecommendationModel]:
        stock_daily_recommendation: BatchUpdateStockDailyRecommendation = req.stock_daily_recommendation
        ids: list[int] = req.ids
        if not stock_daily_recommendation or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(
            ids=ids, data=stock_daily_recommendation.model_dump(exclude_none=True)
        )
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_stock_daily_recommendations(
        self, req: BatchPatchStockDailyRecommendationsRequest
    ) -> list[StockDailyRecommendationModel]:
        stock_daily_recommendations: list[UpdateStockDailyRecommendation] = req.stock_daily_recommendations
        if not stock_daily_recommendations:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            stock_daily_recommendation.model_dump(exclude_unset=True) for stock_daily_recommendation in stock_daily_recommendations
        ]
        await self.mapper.batch_update(items=update_data)
        stock_daily_recommendation_ids: list[int] = [stock_daily_recommendation.id for stock_daily_recommendation in stock_daily_recommendations]
        return await self.mapper.select_by_ids(ids=stock_daily_recommendation_ids)

    async def batch_delete_stock_daily_recommendations(self, req: BatchDeleteStockDailyRecommendationsRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_stock_daily_recommendations_template(self) -> StreamingResponse:
        file_name = "stock_daily_recommendation_import_tpl"
        return await excel_util.export_excel(
            schema=CreateStockDailyRecommendation, file_name=file_name
        )

    async def export_stock_daily_recommendations(self, req: ExportStockDailyRecommendationsRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        stock_daily_recommendation_list: list[StockDailyRecommendationModel] = await self.mapper.select_by_ids(ids=ids)
        if stock_daily_recommendation_list is None or len(stock_daily_recommendation_list) == 0:
            logger.error(f"No stock_daily_recommendations found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        stock_daily_recommendation_page_list = [ExportStockDailyRecommendation(**stock_daily_recommendation.model_dump()) for stock_daily_recommendation in stock_daily_recommendation_list]
        file_name = "stock_daily_recommendation_data_export"
        return await excel_util.export_excel(
            schema=ExportStockDailyRecommendation, file_name=file_name, data_list=stock_daily_recommendation_page_list
        )

    async def import_stock_daily_recommendations(self, req: ImportStockDailyRecommendationsRequest) -> list[ImportStockDailyRecommendation]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        stock_daily_recommendation_records = import_df.to_dict(orient="records")
        if stock_daily_recommendation_records is None or len(stock_daily_recommendation_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in stock_daily_recommendation_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        stock_daily_recommendation_import_list = []
        for stock_daily_recommendation_record in stock_daily_recommendation_records:
            try:
                stock_daily_recommendation_create = ImportStockDailyRecommendation(**stock_daily_recommendation_record)
                stock_daily_recommendation_import_list.append(stock_daily_recommendation_create)
            except ValidationError as e:
                valid_data = {
                    k: v
                    for k, v in stock_daily_recommendation_record.items()
                    if k in ImportStockDailyRecommendation.model_fields
                }
                stock_daily_recommendation_create = ImportStockDailyRecommendation.model_construct(**valid_data)
                stock_daily_recommendation_create.err_msg = ValidateService.get_validate_err_msg(e)
                stock_daily_recommendation_import_list.append(stock_daily_recommendation_create)
                return stock_daily_recommendation_import_list

        return stock_daily_recommendation_import_list