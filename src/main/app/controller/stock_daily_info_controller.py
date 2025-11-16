# SPDX-License-Identifier: MIT
"""StockDailyInfo REST Controller"""
from __future__ import annotations
from typing import Annotated

from fastlib.response import ListResponse
from fastapi import APIRouter, Query, Form
from starlette.responses import StreamingResponse

from src.main.app.mapper.stock_daily_info_mapper import stockDailyInfoMapper
from src.main.app.model.stock_daily_info_model import StockDailyInfoModel
from src.main.app.schema.stock_daily_info_schema import (
    ListStockDailyInfosRequest,
    StockDailyInfo,
    CreateStockDailyInfoRequest,
    StockDailyInfoDetail,
    UpdateStockDailyInfoRequest,
    BatchDeleteStockDailyInfosRequest,
    BatchUpdateStockDailyInfosRequest,
    BatchUpdateStockDailyInfosResponse,
    BatchCreateStockDailyInfosRequest,
    BatchCreateStockDailyInfosResponse,
    ExportStockDailyInfosRequest,
    ImportStockDailyInfosResponse,
    BatchGetStockDailyInfosResponse,
    ImportStockDailyInfosRequest,
    ImportStockDailyInfo, BatchPatchStockDailyInfosRequest,
)
from src.main.app.service.impl.stock_daily_info_service_impl import StockDailyInfoServiceImpl
from src.main.app.service.stock_daily_info_service import StockDailyInfoService

stock_daily_info_router = APIRouter()
stock_daily_info_service: StockDailyInfoService = StockDailyInfoServiceImpl(mapper=stockDailyInfoMapper)


@stock_daily_info_router.get("/stockDailyInfos/{id}")
async def get_stock_daily_info(id: int) -> StockDailyInfoDetail:
    """
    Retrieve stock_daily_info details.

    Args:

        id: Unique ID of the stock_daily_info resource.

    Returns:

        StockDailyInfoDetail: The stock_daily_info object containing all its details.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have permission.
        HTTPException(404 Not Found): If the requested stock_daily_info does not exist.
    """
    stock_daily_info_record: StockDailyInfoModel = await stock_daily_info_service.get_stock_daily_info(id=id)
    return StockDailyInfoDetail(**stock_daily_info_record.model_dump())


@stock_daily_info_router.get("/stockDailyInfos")
async def list_stock_daily_infos(
    req: Annotated[ListStockDailyInfosRequest, Query()],
) -> ListResponse[StockDailyInfo]:
    """
    List stock_daily_infos with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        ListResponse: Paginated list of stock_daily_infos and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    stock_daily_info_records, total = await stock_daily_info_service.list_stock_daily_infos(req=req)
    return ListResponse(records=stock_daily_info_records, total=total)


@stock_daily_info_router.post("/stockDailyInfos")
async def creat_stock_daily_info(
    req: CreateStockDailyInfoRequest,
) -> StockDailyInfo:
    """
    Create a new stock_daily_info.

    Args:

        req: Request object containing stock_daily_info creation data.

    Returns:

         StockDailyInfo: The stock_daily_info object.

    Raises:

        HTTPException(403 Forbidden): If the current user don't have access rights.
        HTTPException(409 Conflict): If the creation data already exists.
    """
    stock_daily_info: StockDailyInfoModel = await stock_daily_info_service.create_stock_daily_info(req=req)
    return StockDailyInfo(**stock_daily_info.model_dump())


@stock_daily_info_router.put("/stockDailyInfos")
async def update_stock_daily_info(
    req: UpdateStockDailyInfoRequest,
) -> StockDailyInfo:
    """
    Update an existing stock_daily_info.

    Args:

        req: Request object containing stock_daily_info update data.

    Returns:

        StockDailyInfo: The updated stock_daily_info object.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have update permissions.
        HTTPException(404 Not Found): If the stock_daily_info to update doesn't exist.
    """
    stock_daily_info: StockDailyInfoModel = await stock_daily_info_service.update_stock_daily_info(req=req)
    return StockDailyInfo(**stock_daily_info.model_dump())


@stock_daily_info_router.delete("/stockDailyInfos/{id}")
async def delete_stock_daily_info(
    id: int,
) -> None:
    """
    Delete stock_daily_info by ID.

    Args:

        id: The ID of the stock_daily_info to delete.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have access permissions.
        HTTPException(404 Not Found): If the stock_daily_info with given ID doesn't exist.
    """
    await stock_daily_info_service.delete_stock_daily_info(id=id)


@stock_daily_info_router.get("/stockDailyInfos:batchGet")
async def batch_get_stock_daily_infos(
    ids: list[int] = Query(..., description="List of stock_daily_info IDs to retrieve"),
) -> BatchGetStockDailyInfosResponse:
    """
    Retrieves multiple stock_daily_infos by their IDs.

    Args:

        ids (list[int]): A list of stock_daily_info resource IDs.

    Returns:

        list[StockDailyInfoDetail]: A list of stock_daily_info objects matching the provided IDs.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have access rights.
        HTTPException(404 Not Found): If one of the requested stock_daily_infos does not exist.
    """
    stock_daily_info_records: list[StockDailyInfoModel] = await stock_daily_info_service.batch_get_stock_daily_infos(ids)
    stock_daily_info_detail_list: list[StockDailyInfoDetail] = [
        StockDailyInfoDetail(**stock_daily_info_record.model_dump()) for stock_daily_info_record in stock_daily_info_records
    ]
    return BatchGetStockDailyInfosResponse(stock_daily_infos=stock_daily_info_detail_list)


@stock_daily_info_router.post("/stockDailyInfos:batchCreate")
async def batch_create_stock_daily_infos(
    req: BatchCreateStockDailyInfosRequest,
) -> BatchCreateStockDailyInfosResponse:
    """
    Batch create stock_daily_infos.

    Args:

        req (BatchCreateStockDailyInfosRequest): Request body containing a list of stock_daily_info creation items.

    Returns:

        BatchCreateStockDailyInfosResponse: Response containing the list of created stock_daily_infos.

    Raises:

        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(409 Conflict): If any stock_daily_info creation data already exists.
    """

    stock_daily_info_records = await stock_daily_info_service.batch_create_stock_daily_infos(req=req)
    stock_daily_info_list: list[StockDailyInfo] = [
        StockDailyInfo(**stock_daily_info_record.model_dump()) for stock_daily_info_record in stock_daily_info_records
    ]
    return BatchCreateStockDailyInfosResponse(stock_daily_infos=stock_daily_info_list)


@stock_daily_info_router.post("/stockDailyInfos:batchUpdate")
async def batch_update_stock_daily_infos(
    req: BatchUpdateStockDailyInfosRequest,
) -> BatchUpdateStockDailyInfosResponse:
    """
    Batch update multiple stock_daily_infos with the same changes.

    Args:

        req (BatchUpdateStockDailyInfosRequest): The batch update request data with ids.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated stock_daily_infos.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify stock_daily_infos
        HTTPException 404 (Not Found): If any specified stock_daily_info ID doesn't exist
    """
    stock_daily_info_records: list[StockDailyInfoModel] = await stock_daily_info_service.batch_update_stock_daily_infos(req=req)
    stock_daily_info_list: list[StockDailyInfo] = [StockDailyInfo(**stock_daily_info.model_dump()) for stock_daily_info in stock_daily_info_records]
    return BatchUpdateStockDailyInfosResponse(stock_daily_infos=stock_daily_info_list)


@stock_daily_info_router.post("/stockDailyInfos:batchPatch")
async def batch_patch_stock_daily_infos(
    req: BatchPatchStockDailyInfosRequest,
) -> BatchUpdateStockDailyInfosResponse:
    """
    Batch update multiple stock_daily_infos with individual changes.

    Args:

        req (BatchPatchStockDailyInfosRequest): The batch patch request data.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated stock_daily_infos.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify stock_daily_infos
        HTTPException 404 (Not Found): If any specified stock_daily_info ID doesn't exist
    """
    stock_daily_info_records: list[StockDailyInfoModel] = await stock_daily_info_service.batch_patch_stock_daily_infos(req=req)
    stock_daily_info_list: list[StockDailyInfo] = [StockDailyInfo(**stock_daily_info.model_dump()) for stock_daily_info in stock_daily_info_records]
    return BatchUpdateStockDailyInfosResponse(stock_daily_infos=stock_daily_info_list)


@stock_daily_info_router.post("/stockDailyInfos:batchDelete")
async def batch_delete_stock_daily_infos(
    req: BatchDeleteStockDailyInfosRequest,
) -> None:
    """
    Batch delete stock_daily_infos.

    Args:
        req (BatchDeleteStockDailyInfosRequest): Request object containing delete info.

    Raises:
        HTTPException(404 Not Found): If any of the stock_daily_infos do not exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    await stock_daily_info_service.batch_delete_stock_daily_infos(req=req)


@stock_daily_info_router.get("/stockDailyInfos:exportTemplate")
async def export_stock_daily_infos_template() -> StreamingResponse:
    """
    Export the Excel template for stock_daily_info import.

    Returns:
        StreamingResponse: An Excel file stream containing the import template.

    Raises:
        HTTPException(403 Forbidden): If user don't have access rights.
    """

    return await stock_daily_info_service.export_stock_daily_infos_template()


@stock_daily_info_router.get("/stockDailyInfos:export")
async def export_stock_daily_infos(
    req: ExportStockDailyInfosRequest = Query(...),
) -> StreamingResponse:
    """
    Export stock_daily_info data based on the provided stock_daily_info IDs.

    Args:
        req (ExportStockDailyInfosRequest): Query parameters specifying the stock_daily_infos to export.

    Returns:
        StreamingResponse: A streaming response containing the generated Excel file.

    Raises:
        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(404 Not Found ): If no matching stock_daily_infos are found.
    """
    return await stock_daily_info_service.export_stock_daily_infos(
        req=req,
    )

@stock_daily_info_router.post("/stockDailyInfos:import")
async def import_stock_daily_infos(
    req: ImportStockDailyInfosRequest = Form(...),
) -> ImportStockDailyInfosResponse:
    """
    Import stock_daily_infos from an uploaded Excel file.

    Args:
        req (UploadFile): The Excel file containing stock_daily_info data to import.

    Returns:
        ImportStockDailyInfosResponse: List of successfully parsed stock_daily_info data.

    Raises:
        HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
        HTTPException(403 Forbidden): If the current user lacks access rights.
    """

    import_stock_daily_infos_resp: list[ImportStockDailyInfo] = await stock_daily_info_service.import_stock_daily_infos(
        req=req
    )
    return ImportStockDailyInfosResponse(stock_daily_infos=import_stock_daily_infos_resp)