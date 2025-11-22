# # SPDX-License-Identifier: MIT
# """StockDailyRecommendation REST Controller"""
# from __future__ import annotations
# from typing import Annotated

# from fastlib.response import ListResponse
# from fastapi import APIRouter, Query, Form
# from starlette.responses import StreamingResponse

# from src.main.app.mapper.stock_daily_recommendation_mapper import stockDailyRecommendationMapper
# from src.main.app.model.stock_daily_recommendation_model import StockDailyRecommendationModel
# from src.main.app.schema.stock_daily_recommendation_schema import (
#     ListStockDailyRecommendationsRequest,
#     StockDailyRecommendation,
#     CreateStockDailyRecommendationRequest,
#     StockDailyRecommendationDetail,
#     UpdateStockDailyRecommendationRequest,
#     BatchDeleteStockDailyRecommendationsRequest,
#     BatchUpdateStockDailyRecommendationsRequest,
#     BatchUpdateStockDailyRecommendationsResponse,
#     BatchCreateStockDailyRecommendationsRequest,
#     BatchCreateStockDailyRecommendationsResponse,
#     ExportStockDailyRecommendationsRequest,
#     ImportStockDailyRecommendationsResponse,
#     BatchGetStockDailyRecommendationsResponse,
#     ImportStockDailyRecommendationsRequest,
#     ImportStockDailyRecommendation, BatchPatchStockDailyRecommendationsRequest,
# )
# from src.main.app.service.impl.stock_daily_recommendation_service_impl import StockDailyRecommendationServiceImpl
# from src.main.app.service.stock_daily_recommendation_service import StockDailyRecommendationService

# stock_daily_recommendation_router = APIRouter()
# stock_daily_recommendation_service: StockDailyRecommendationService = StockDailyRecommendationServiceImpl(mapper=stockDailyRecommendationMapper)


# @stock_daily_recommendation_router.get("/stockDailyRecommendations/{id}")
# async def get_stock_daily_recommendation(id: int) -> StockDailyRecommendationDetail:
#     """
#     Retrieve stock_daily_recommendation details.

#     Args:

#         id: Unique ID of the stock_daily_recommendation resource.

#     Returns:

#         StockDailyRecommendationDetail: The stock_daily_recommendation object containing all its details.

#     Raises:

#         HTTPException(403 Forbidden): If the current user does not have permission.
#         HTTPException(404 Not Found): If the requested stock_daily_recommendation does not exist.
#     """
#     stock_daily_recommendation_record: StockDailyRecommendationModel = await stock_daily_recommendation_service.get_stock_daily_recommendation(id=id)
#     return StockDailyRecommendationDetail(**stock_daily_recommendation_record.model_dump())


# @stock_daily_recommendation_router.get("/stockDailyRecommendations")
# async def list_stock_daily_recommendations(
#     req: Annotated[ListStockDailyRecommendationsRequest, Query()],
# ) -> ListResponse[StockDailyRecommendation]:
#     """
#     List stock_daily_recommendations with pagination.

#     Args:

#         req: Request object containing pagination, filter and sort parameters.

#     Returns:

#         ListResponse: Paginated list of stock_daily_recommendations and total count.

#     Raises:

#         HTTPException(403 Forbidden): If user don't have access rights.
#     """
#     stock_daily_recommendation_records, total = await stock_daily_recommendation_service.list_stock_daily_recommendations(req=req)
#     return ListResponse(records=stock_daily_recommendation_records, total=total)


# @stock_daily_recommendation_router.post("/stockDailyRecommendations")
# async def creat_stock_daily_recommendation(
#     req: CreateStockDailyRecommendationRequest,
# ) -> StockDailyRecommendation:
#     """
#     Create a new stock_daily_recommendation.

#     Args:

#         req: Request object containing stock_daily_recommendation creation data.

#     Returns:

#          StockDailyRecommendation: The stock_daily_recommendation object.

#     Raises:

#         HTTPException(403 Forbidden): If the current user don't have access rights.
#         HTTPException(409 Conflict): If the creation data already exists.
#     """
#     stock_daily_recommendation: StockDailyRecommendationModel = await stock_daily_recommendation_service.create_stock_daily_recommendation(req=req)
#     return StockDailyRecommendation(**stock_daily_recommendation.model_dump())


# @stock_daily_recommendation_router.put("/stockDailyRecommendations")
# async def update_stock_daily_recommendation(
#     req: UpdateStockDailyRecommendationRequest,
# ) -> StockDailyRecommendation:
#     """
#     Update an existing stock_daily_recommendation.

#     Args:

#         req: Request object containing stock_daily_recommendation update data.

#     Returns:

#         StockDailyRecommendation: The updated stock_daily_recommendation object.

#     Raises:

#         HTTPException(403 Forbidden): If the current user doesn't have update permissions.
#         HTTPException(404 Not Found): If the stock_daily_recommendation to update doesn't exist.
#     """
#     stock_daily_recommendation: StockDailyRecommendationModel = await stock_daily_recommendation_service.update_stock_daily_recommendation(req=req)
#     return StockDailyRecommendation(**stock_daily_recommendation.model_dump())


# @stock_daily_recommendation_router.delete("/stockDailyRecommendations/{id}")
# async def delete_stock_daily_recommendation(
#     id: int,
# ) -> None:
#     """
#     Delete stock_daily_recommendation by ID.

#     Args:

#         id: The ID of the stock_daily_recommendation to delete.

#     Raises:

#         HTTPException(403 Forbidden): If the current user doesn't have access permissions.
#         HTTPException(404 Not Found): If the stock_daily_recommendation with given ID doesn't exist.
#     """
#     await stock_daily_recommendation_service.delete_stock_daily_recommendation(id=id)


# @stock_daily_recommendation_router.get("/stockDailyRecommendations:batchGet")
# async def batch_get_stock_daily_recommendations(
#     ids: list[int] = Query(..., description="List of stock_daily_recommendation IDs to retrieve"),
# ) -> BatchGetStockDailyRecommendationsResponse:
#     """
#     Retrieves multiple stock_daily_recommendations by their IDs.

#     Args:

#         ids (list[int]): A list of stock_daily_recommendation resource IDs.

#     Returns:

#         list[StockDailyRecommendationDetail]: A list of stock_daily_recommendation objects matching the provided IDs.

#     Raises:

#         HTTPException(403 Forbidden): If the current user does not have access rights.
#         HTTPException(404 Not Found): If one of the requested stock_daily_recommendations does not exist.
#     """
#     stock_daily_recommendation_records: list[StockDailyRecommendationModel] = await stock_daily_recommendation_service.batch_get_stock_daily_recommendations(ids)
#     stock_daily_recommendation_detail_list: list[StockDailyRecommendationDetail] = [
#         StockDailyRecommendationDetail(**stock_daily_recommendation_record.model_dump()) for stock_daily_recommendation_record in stock_daily_recommendation_records
#     ]
#     return BatchGetStockDailyRecommendationsResponse(stock_daily_recommendations=stock_daily_recommendation_detail_list)


# @stock_daily_recommendation_router.post("/stockDailyRecommendations:batchCreate")
# async def batch_create_stock_daily_recommendations(
#     req: BatchCreateStockDailyRecommendationsRequest,
# ) -> BatchCreateStockDailyRecommendationsResponse:
#     """
#     Batch create stock_daily_recommendations.

#     Args:

#         req (BatchCreateStockDailyRecommendationsRequest): Request body containing a list of stock_daily_recommendation creation items.

#     Returns:

#         BatchCreateStockDailyRecommendationsResponse: Response containing the list of created stock_daily_recommendations.

#     Raises:

#         HTTPException(403 Forbidden): If the current user lacks access rights.
#         HTTPException(409 Conflict): If any stock_daily_recommendation creation data already exists.
#     """

#     stock_daily_recommendation_records = await stock_daily_recommendation_service.batch_create_stock_daily_recommendations(req=req)
#     stock_daily_recommendation_list: list[StockDailyRecommendation] = [
#         StockDailyRecommendation(**stock_daily_recommendation_record.model_dump()) for stock_daily_recommendation_record in stock_daily_recommendation_records
#     ]
#     return BatchCreateStockDailyRecommendationsResponse(stock_daily_recommendations=stock_daily_recommendation_list)


# @stock_daily_recommendation_router.post("/stockDailyRecommendations:batchUpdate")
# async def batch_update_stock_daily_recommendations(
#     req: BatchUpdateStockDailyRecommendationsRequest,
# ) -> BatchUpdateStockDailyRecommendationsResponse:
#     """
#     Batch update multiple stock_daily_recommendations with the same changes.

#     Args:

#         req (BatchUpdateStockDailyRecommendationsRequest): The batch update request data with ids.

#     Returns:

#         BatchUpdateBooksResponse: Contains the list of updated stock_daily_recommendations.

#     Raises:

#         HTTPException 403 (Forbidden): If user lacks permission to modify stock_daily_recommendations
#         HTTPException 404 (Not Found): If any specified stock_daily_recommendation ID doesn't exist
#     """
#     stock_daily_recommendation_records: list[StockDailyRecommendationModel] = await stock_daily_recommendation_service.batch_update_stock_daily_recommendations(req=req)
#     stock_daily_recommendation_list: list[StockDailyRecommendation] = [StockDailyRecommendation(**stock_daily_recommendation.model_dump()) for stock_daily_recommendation in stock_daily_recommendation_records]
#     return BatchUpdateStockDailyRecommendationsResponse(stock_daily_recommendations=stock_daily_recommendation_list)


# @stock_daily_recommendation_router.post("/stockDailyRecommendations:batchPatch")
# async def batch_patch_stock_daily_recommendations(
#     req: BatchPatchStockDailyRecommendationsRequest,
# ) -> BatchUpdateStockDailyRecommendationsResponse:
#     """
#     Batch update multiple stock_daily_recommendations with individual changes.

#     Args:

#         req (BatchPatchStockDailyRecommendationsRequest): The batch patch request data.

#     Returns:

#         BatchUpdateBooksResponse: Contains the list of updated stock_daily_recommendations.

#     Raises:

#         HTTPException 403 (Forbidden): If user lacks permission to modify stock_daily_recommendations
#         HTTPException 404 (Not Found): If any specified stock_daily_recommendation ID doesn't exist
#     """
#     stock_daily_recommendation_records: list[StockDailyRecommendationModel] = await stock_daily_recommendation_service.batch_patch_stock_daily_recommendations(req=req)
#     stock_daily_recommendation_list: list[StockDailyRecommendation] = [StockDailyRecommendation(**stock_daily_recommendation.model_dump()) for stock_daily_recommendation in stock_daily_recommendation_records]
#     return BatchUpdateStockDailyRecommendationsResponse(stock_daily_recommendations=stock_daily_recommendation_list)


# @stock_daily_recommendation_router.post("/stockDailyRecommendations:batchDelete")
# async def batch_delete_stock_daily_recommendations(
#     req: BatchDeleteStockDailyRecommendationsRequest,
# ) -> None:
#     """
#     Batch delete stock_daily_recommendations.

#     Args:
#         req (BatchDeleteStockDailyRecommendationsRequest): Request object containing delete info.

#     Raises:
#         HTTPException(404 Not Found): If any of the stock_daily_recommendations do not exist.
#         HTTPException(403 Forbidden): If user don't have access rights.
#     """
#     await stock_daily_recommendation_service.batch_delete_stock_daily_recommendations(req=req)


# @stock_daily_recommendation_router.get("/stockDailyRecommendations:exportTemplate")
# async def export_stock_daily_recommendations_template() -> StreamingResponse:
#     """
#     Export the Excel template for stock_daily_recommendation import.

#     Returns:
#         StreamingResponse: An Excel file stream containing the import template.

#     Raises:
#         HTTPException(403 Forbidden): If user don't have access rights.
#     """

#     return await stock_daily_recommendation_service.export_stock_daily_recommendations_template()


# @stock_daily_recommendation_router.get("/stockDailyRecommendations:export")
# async def export_stock_daily_recommendations(
#     req: ExportStockDailyRecommendationsRequest = Query(...),
# ) -> StreamingResponse:
#     """
#     Export stock_daily_recommendation data based on the provided stock_daily_recommendation IDs.

#     Args:
#         req (ExportStockDailyRecommendationsRequest): Query parameters specifying the stock_daily_recommendations to export.

#     Returns:
#         StreamingResponse: A streaming response containing the generated Excel file.

#     Raises:
#         HTTPException(403 Forbidden): If the current user lacks access rights.
#         HTTPException(404 Not Found ): If no matching stock_daily_recommendations are found.
#     """
#     return await stock_daily_recommendation_service.export_stock_daily_recommendations(
#         req=req,
#     )

# @stock_daily_recommendation_router.post("/stockDailyRecommendations:import")
# async def import_stock_daily_recommendations(
#     req: ImportStockDailyRecommendationsRequest = Form(...),
# ) -> ImportStockDailyRecommendationsResponse:
#     """
#     Import stock_daily_recommendations from an uploaded Excel file.

#     Args:
#         req (UploadFile): The Excel file containing stock_daily_recommendation data to import.

#     Returns:
#         ImportStockDailyRecommendationsResponse: List of successfully parsed stock_daily_recommendation data.

#     Raises:
#         HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
#         HTTPException(403 Forbidden): If the current user lacks access rights.
#     """

#     import_stock_daily_recommendations_resp: list[ImportStockDailyRecommendation] = await stock_daily_recommendation_service.import_stock_daily_recommendations(
#         req=req
#     )
#     return ImportStockDailyRecommendationsResponse(stock_daily_recommendations=import_stock_daily_recommendations_resp)