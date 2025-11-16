# SPDX-License-Identifier: MIT
"""StockBasicInfo REST Controller"""
from __future__ import annotations
from typing import Annotated

from fastlib.response import ListResponse
from fastapi import APIRouter, Query, Form
from starlette.responses import StreamingResponse

from src.main.app.mapper.stock_basic_info_mapper import stockBasicInfoMapper
from src.main.app.model.stock_basic_info_model import StockBasicInfoModel
from src.main.app.schema.stock_basic_info_schema import (
    ListStockBasicInfosRequest,
    StockBasicInfo,
    CreateStockBasicInfoRequest,
    StockBasicInfoDetail,
    UpdateStockBasicInfoRequest,
    BatchDeleteStockBasicInfosRequest,
    BatchUpdateStockBasicInfosRequest,
    BatchUpdateStockBasicInfosResponse,
    BatchCreateStockBasicInfosRequest,
    BatchCreateStockBasicInfosResponse,
    ExportStockBasicInfosRequest,
    ImportStockBasicInfosResponse,
    BatchGetStockBasicInfosResponse,
    ImportStockBasicInfosRequest,
    ImportStockBasicInfo, BatchPatchStockBasicInfosRequest,
)
from src.main.app.service.impl.stock_basic_info_service_impl import StockBasicInfoServiceImpl
from src.main.app.service.stock_basic_info_service import StockBasicInfoService

stock_basic_info_router = APIRouter()
stock_basic_info_service: StockBasicInfoService = StockBasicInfoServiceImpl(mapper=stockBasicInfoMapper)


@stock_basic_info_router.get("/stockBasicInfos/{id}")
async def get_stock_basic_info(id: int) -> StockBasicInfoDetail:
    """
    Retrieve stock_basic_info details.

    Args:

        id: Unique ID of the stock_basic_info resource.

    Returns:

        StockBasicInfoDetail: The stock_basic_info object containing all its details.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have permission.
        HTTPException(404 Not Found): If the requested stock_basic_info does not exist.
    """
    stock_basic_info_record: StockBasicInfoModel = await stock_basic_info_service.get_stock_basic_info(id=id)
    return StockBasicInfoDetail(**stock_basic_info_record.model_dump())


@stock_basic_info_router.get("/stockBasicInfos")
async def list_stock_basic_infos(
    req: Annotated[ListStockBasicInfosRequest, Query()],
) -> ListResponse[StockBasicInfo]:
    """
    List stock_basic_infos with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        ListResponse: Paginated list of stock_basic_infos and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    stock_basic_info_records, total = await stock_basic_info_service.list_stock_basic_infos(req=req)
    return ListResponse(records=stock_basic_info_records, total=total)


@stock_basic_info_router.post("/stockBasicInfos")
async def creat_stock_basic_info(
    req: CreateStockBasicInfoRequest,
) -> StockBasicInfo:
    """
    Create a new stock_basic_info.

    Args:

        req: Request object containing stock_basic_info creation data.

    Returns:

         StockBasicInfo: The stock_basic_info object.

    Raises:

        HTTPException(403 Forbidden): If the current user don't have access rights.
        HTTPException(409 Conflict): If the creation data already exists.
    """
    stock_basic_info: StockBasicInfoModel = await stock_basic_info_service.create_stock_basic_info(req=req)
    return StockBasicInfo(**stock_basic_info.model_dump())


@stock_basic_info_router.put("/stockBasicInfos")
async def update_stock_basic_info(
    req: UpdateStockBasicInfoRequest,
) -> StockBasicInfo:
    """
    Update an existing stock_basic_info.

    Args:

        req: Request object containing stock_basic_info update data.

    Returns:

        StockBasicInfo: The updated stock_basic_info object.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have update permissions.
        HTTPException(404 Not Found): If the stock_basic_info to update doesn't exist.
    """
    stock_basic_info: StockBasicInfoModel = await stock_basic_info_service.update_stock_basic_info(req=req)
    return StockBasicInfo(**stock_basic_info.model_dump())


@stock_basic_info_router.delete("/stockBasicInfos/{id}")
async def delete_stock_basic_info(
    id: int,
) -> None:
    """
    Delete stock_basic_info by ID.

    Args:

        id: The ID of the stock_basic_info to delete.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have access permissions.
        HTTPException(404 Not Found): If the stock_basic_info with given ID doesn't exist.
    """
    await stock_basic_info_service.delete_stock_basic_info(id=id)


@stock_basic_info_router.get("/stockBasicInfos:batchGet")
async def batch_get_stock_basic_infos(
    ids: list[int] = Query(..., description="List of stock_basic_info IDs to retrieve"),
) -> BatchGetStockBasicInfosResponse:
    """
    Retrieves multiple stock_basic_infos by their IDs.

    Args:

        ids (list[int]): A list of stock_basic_info resource IDs.

    Returns:

        list[StockBasicInfoDetail]: A list of stock_basic_info objects matching the provided IDs.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have access rights.
        HTTPException(404 Not Found): If one of the requested stock_basic_infos does not exist.
    """
    stock_basic_info_records: list[StockBasicInfoModel] = await stock_basic_info_service.batch_get_stock_basic_infos(ids)
    stock_basic_info_detail_list: list[StockBasicInfoDetail] = [
        StockBasicInfoDetail(**stock_basic_info_record.model_dump()) for stock_basic_info_record in stock_basic_info_records
    ]
    return BatchGetStockBasicInfosResponse(stock_basic_infos=stock_basic_info_detail_list)


@stock_basic_info_router.post("/stockBasicInfos:batchCreate")
async def batch_create_stock_basic_infos(
    req: BatchCreateStockBasicInfosRequest,
) -> BatchCreateStockBasicInfosResponse:
    """
    Batch create stock_basic_infos.

    Args:

        req (BatchCreateStockBasicInfosRequest): Request body containing a list of stock_basic_info creation items.

    Returns:

        BatchCreateStockBasicInfosResponse: Response containing the list of created stock_basic_infos.

    Raises:

        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(409 Conflict): If any stock_basic_info creation data already exists.
    """

    stock_basic_info_records = await stock_basic_info_service.batch_create_stock_basic_infos(req=req)
    stock_basic_info_list: list[StockBasicInfo] = [
        StockBasicInfo(**stock_basic_info_record.model_dump()) for stock_basic_info_record in stock_basic_info_records
    ]
    return BatchCreateStockBasicInfosResponse(stock_basic_infos=stock_basic_info_list)


@stock_basic_info_router.post("/stockBasicInfos:batchUpdate")
async def batch_update_stock_basic_infos(
    req: BatchUpdateStockBasicInfosRequest,
) -> BatchUpdateStockBasicInfosResponse:
    """
    Batch update multiple stock_basic_infos with the same changes.

    Args:

        req (BatchUpdateStockBasicInfosRequest): The batch update request data with ids.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated stock_basic_infos.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify stock_basic_infos
        HTTPException 404 (Not Found): If any specified stock_basic_info ID doesn't exist
    """
    stock_basic_info_records: list[StockBasicInfoModel] = await stock_basic_info_service.batch_update_stock_basic_infos(req=req)
    stock_basic_info_list: list[StockBasicInfo] = [StockBasicInfo(**stock_basic_info.model_dump()) for stock_basic_info in stock_basic_info_records]
    return BatchUpdateStockBasicInfosResponse(stock_basic_infos=stock_basic_info_list)


@stock_basic_info_router.post("/stockBasicInfos:batchPatch")
async def batch_patch_stock_basic_infos(
    req: BatchPatchStockBasicInfosRequest,
) -> BatchUpdateStockBasicInfosResponse:
    """
    Batch update multiple stock_basic_infos with individual changes.

    Args:

        req (BatchPatchStockBasicInfosRequest): The batch patch request data.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated stock_basic_infos.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify stock_basic_infos
        HTTPException 404 (Not Found): If any specified stock_basic_info ID doesn't exist
    """
    stock_basic_info_records: list[StockBasicInfoModel] = await stock_basic_info_service.batch_patch_stock_basic_infos(req=req)
    stock_basic_info_list: list[StockBasicInfo] = [StockBasicInfo(**stock_basic_info.model_dump()) for stock_basic_info in stock_basic_info_records]
    return BatchUpdateStockBasicInfosResponse(stock_basic_infos=stock_basic_info_list)


@stock_basic_info_router.post("/stockBasicInfos:batchDelete")
async def batch_delete_stock_basic_infos(
    req: BatchDeleteStockBasicInfosRequest,
) -> None:
    """
    Batch delete stock_basic_infos.

    Args:
        req (BatchDeleteStockBasicInfosRequest): Request object containing delete info.

    Raises:
        HTTPException(404 Not Found): If any of the stock_basic_infos do not exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    await stock_basic_info_service.batch_delete_stock_basic_infos(req=req)


@stock_basic_info_router.get("/stockBasicInfos:exportTemplate")
async def export_stock_basic_infos_template() -> StreamingResponse:
    """
    Export the Excel template for stock_basic_info import.

    Returns:
        StreamingResponse: An Excel file stream containing the import template.

    Raises:
        HTTPException(403 Forbidden): If user don't have access rights.
    """

    return await stock_basic_info_service.export_stock_basic_infos_template()


@stock_basic_info_router.get("/stockBasicInfos:export")
async def export_stock_basic_infos(
    req: ExportStockBasicInfosRequest = Query(...),
) -> StreamingResponse:
    """
    Export stock_basic_info data based on the provided stock_basic_info IDs.

    Args:
        req (ExportStockBasicInfosRequest): Query parameters specifying the stock_basic_infos to export.

    Returns:
        StreamingResponse: A streaming response containing the generated Excel file.

    Raises:
        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(404 Not Found ): If no matching stock_basic_infos are found.
    """
    return await stock_basic_info_service.export_stock_basic_infos(
        req=req,
    )

@stock_basic_info_router.post("/stockBasicInfos:import")
async def import_stock_basic_infos(
    req: ImportStockBasicInfosRequest = Form(...),
) -> ImportStockBasicInfosResponse:
    """
    Import stock_basic_infos from an uploaded Excel file.

    Args:
        req (UploadFile): The Excel file containing stock_basic_info data to import.

    Returns:
        ImportStockBasicInfosResponse: List of successfully parsed stock_basic_info data.

    Raises:
        HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
        HTTPException(403 Forbidden): If the current user lacks access rights.
    """

    import_stock_basic_infos_resp: list[ImportStockBasicInfo] = await stock_basic_info_service.import_stock_basic_infos(
        req=req
    )
    return ImportStockBasicInfosResponse(stock_basic_infos=import_stock_basic_infos_resp)