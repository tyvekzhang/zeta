# SPDX-License-Identifier: MIT
"""StockHolderInfo REST Controller"""
from __future__ import annotations
from typing import Annotated

from fastlib.response import ListResponse
from fastapi import APIRouter, Query, Form
from starlette.responses import StreamingResponse

from src.main.app.mapper.stock_holder_info_mapper import stockHolderInfoMapper
from src.main.app.model.stock_holder_info_model import StockHolderInfoModel
from src.main.app.schema.stock_holder_info_schema import (
    ListStockHolderInfosRequest,
    StockHolderInfo,
    CreateStockHolderInfoRequest,
    StockHolderInfoDetail,
    UpdateStockHolderInfoRequest,
    BatchDeleteStockHolderInfosRequest,
    BatchUpdateStockHolderInfosRequest,
    BatchUpdateStockHolderInfosResponse,
    BatchCreateStockHolderInfosRequest,
    BatchCreateStockHolderInfosResponse,
    ExportStockHolderInfosRequest,
    ImportStockHolderInfosResponse,
    BatchGetStockHolderInfosResponse,
    ImportStockHolderInfosRequest,
    ImportStockHolderInfo, BatchPatchStockHolderInfosRequest,
)
from src.main.app.service.impl.stock_holder_info_service_impl import StockHolderInfoServiceImpl
from src.main.app.service.stock_holder_info_service import StockHolderInfoService

stock_holder_info_router = APIRouter()
stock_holder_info_service: StockHolderInfoService = StockHolderInfoServiceImpl(mapper=stockHolderInfoMapper)


@stock_holder_info_router.get("/stockHolderInfos/{id}")
async def get_stock_holder_info(id: int) -> StockHolderInfoDetail:
    """
    Retrieve stock_holder_info details.

    Args:

        id: Unique ID of the stock_holder_info resource.

    Returns:

        StockHolderInfoDetail: The stock_holder_info object containing all its details.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have permission.
        HTTPException(404 Not Found): If the requested stock_holder_info does not exist.
    """
    stock_holder_info_record: StockHolderInfoModel = await stock_holder_info_service.get_stock_holder_info(id=id)
    return StockHolderInfoDetail(**stock_holder_info_record.model_dump())


@stock_holder_info_router.get("/stockHolderInfos")
async def list_stock_holder_infos(
    req: Annotated[ListStockHolderInfosRequest, Query()],
) -> ListResponse[StockHolderInfo]:
    """
    List stock_holder_infos with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        ListResponse: Paginated list of stock_holder_infos and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    stock_holder_info_records, total = await stock_holder_info_service.list_stock_holder_infos(req=req)
    return ListResponse(records=stock_holder_info_records, total=total)


@stock_holder_info_router.post("/stockHolderInfos")
async def creat_stock_holder_info(
    req: CreateStockHolderInfoRequest,
) -> StockHolderInfo:
    """
    Create a new stock_holder_info.

    Args:

        req: Request object containing stock_holder_info creation data.

    Returns:

         StockHolderInfo: The stock_holder_info object.

    Raises:

        HTTPException(403 Forbidden): If the current user don't have access rights.
        HTTPException(409 Conflict): If the creation data already exists.
    """
    stock_holder_info: StockHolderInfoModel = await stock_holder_info_service.create_stock_holder_info(req=req)
    return StockHolderInfo(**stock_holder_info.model_dump())


@stock_holder_info_router.put("/stockHolderInfos")
async def update_stock_holder_info(
    req: UpdateStockHolderInfoRequest,
) -> StockHolderInfo:
    """
    Update an existing stock_holder_info.

    Args:

        req: Request object containing stock_holder_info update data.

    Returns:

        StockHolderInfo: The updated stock_holder_info object.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have update permissions.
        HTTPException(404 Not Found): If the stock_holder_info to update doesn't exist.
    """
    stock_holder_info: StockHolderInfoModel = await stock_holder_info_service.update_stock_holder_info(req=req)
    return StockHolderInfo(**stock_holder_info.model_dump())


@stock_holder_info_router.delete("/stockHolderInfos/{id}")
async def delete_stock_holder_info(
    id: int,
) -> None:
    """
    Delete stock_holder_info by ID.

    Args:

        id: The ID of the stock_holder_info to delete.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have access permissions.
        HTTPException(404 Not Found): If the stock_holder_info with given ID doesn't exist.
    """
    await stock_holder_info_service.delete_stock_holder_info(id=id)


@stock_holder_info_router.get("/stockHolderInfos:batchGet")
async def batch_get_stock_holder_infos(
    ids: list[int] = Query(..., description="List of stock_holder_info IDs to retrieve"),
) -> BatchGetStockHolderInfosResponse:
    """
    Retrieves multiple stock_holder_infos by their IDs.

    Args:

        ids (list[int]): A list of stock_holder_info resource IDs.

    Returns:

        list[StockHolderInfoDetail]: A list of stock_holder_info objects matching the provided IDs.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have access rights.
        HTTPException(404 Not Found): If one of the requested stock_holder_infos does not exist.
    """
    stock_holder_info_records: list[StockHolderInfoModel] = await stock_holder_info_service.batch_get_stock_holder_infos(ids)
    stock_holder_info_detail_list: list[StockHolderInfoDetail] = [
        StockHolderInfoDetail(**stock_holder_info_record.model_dump()) for stock_holder_info_record in stock_holder_info_records
    ]
    return BatchGetStockHolderInfosResponse(stock_holder_infos=stock_holder_info_detail_list)


@stock_holder_info_router.post("/stockHolderInfos:batchCreate")
async def batch_create_stock_holder_infos(
    req: BatchCreateStockHolderInfosRequest,
) -> BatchCreateStockHolderInfosResponse:
    """
    Batch create stock_holder_infos.

    Args:

        req (BatchCreateStockHolderInfosRequest): Request body containing a list of stock_holder_info creation items.

    Returns:

        BatchCreateStockHolderInfosResponse: Response containing the list of created stock_holder_infos.

    Raises:

        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(409 Conflict): If any stock_holder_info creation data already exists.
    """

    stock_holder_info_records = await stock_holder_info_service.batch_create_stock_holder_infos(req=req)
    stock_holder_info_list: list[StockHolderInfo] = [
        StockHolderInfo(**stock_holder_info_record.model_dump()) for stock_holder_info_record in stock_holder_info_records
    ]
    return BatchCreateStockHolderInfosResponse(stock_holder_infos=stock_holder_info_list)


@stock_holder_info_router.post("/stockHolderInfos:batchUpdate")
async def batch_update_stock_holder_infos(
    req: BatchUpdateStockHolderInfosRequest,
) -> BatchUpdateStockHolderInfosResponse:
    """
    Batch update multiple stock_holder_infos with the same changes.

    Args:

        req (BatchUpdateStockHolderInfosRequest): The batch update request data with ids.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated stock_holder_infos.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify stock_holder_infos
        HTTPException 404 (Not Found): If any specified stock_holder_info ID doesn't exist
    """
    stock_holder_info_records: list[StockHolderInfoModel] = await stock_holder_info_service.batch_update_stock_holder_infos(req=req)
    stock_holder_info_list: list[StockHolderInfo] = [StockHolderInfo(**stock_holder_info.model_dump()) for stock_holder_info in stock_holder_info_records]
    return BatchUpdateStockHolderInfosResponse(stock_holder_infos=stock_holder_info_list)


@stock_holder_info_router.post("/stockHolderInfos:batchPatch")
async def batch_patch_stock_holder_infos(
    req: BatchPatchStockHolderInfosRequest,
) -> BatchUpdateStockHolderInfosResponse:
    """
    Batch update multiple stock_holder_infos with individual changes.

    Args:

        req (BatchPatchStockHolderInfosRequest): The batch patch request data.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated stock_holder_infos.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify stock_holder_infos
        HTTPException 404 (Not Found): If any specified stock_holder_info ID doesn't exist
    """
    stock_holder_info_records: list[StockHolderInfoModel] = await stock_holder_info_service.batch_patch_stock_holder_infos(req=req)
    stock_holder_info_list: list[StockHolderInfo] = [StockHolderInfo(**stock_holder_info.model_dump()) for stock_holder_info in stock_holder_info_records]
    return BatchUpdateStockHolderInfosResponse(stock_holder_infos=stock_holder_info_list)


@stock_holder_info_router.post("/stockHolderInfos:batchDelete")
async def batch_delete_stock_holder_infos(
    req: BatchDeleteStockHolderInfosRequest,
) -> None:
    """
    Batch delete stock_holder_infos.

    Args:
        req (BatchDeleteStockHolderInfosRequest): Request object containing delete info.

    Raises:
        HTTPException(404 Not Found): If any of the stock_holder_infos do not exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    await stock_holder_info_service.batch_delete_stock_holder_infos(req=req)


@stock_holder_info_router.get("/stockHolderInfos:exportTemplate")
async def export_stock_holder_infos_template() -> StreamingResponse:
    """
    Export the Excel template for stock_holder_info import.

    Returns:
        StreamingResponse: An Excel file stream containing the import template.

    Raises:
        HTTPException(403 Forbidden): If user don't have access rights.
    """

    return await stock_holder_info_service.export_stock_holder_infos_template()


@stock_holder_info_router.get("/stockHolderInfos:export")
async def export_stock_holder_infos(
    req: ExportStockHolderInfosRequest = Query(...),
) -> StreamingResponse:
    """
    Export stock_holder_info data based on the provided stock_holder_info IDs.

    Args:
        req (ExportStockHolderInfosRequest): Query parameters specifying the stock_holder_infos to export.

    Returns:
        StreamingResponse: A streaming response containing the generated Excel file.

    Raises:
        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(404 Not Found ): If no matching stock_holder_infos are found.
    """
    return await stock_holder_info_service.export_stock_holder_infos(
        req=req,
    )

@stock_holder_info_router.post("/stockHolderInfos:import")
async def import_stock_holder_infos(
    req: ImportStockHolderInfosRequest = Form(...),
) -> ImportStockHolderInfosResponse:
    """
    Import stock_holder_infos from an uploaded Excel file.

    Args:
        req (UploadFile): The Excel file containing stock_holder_info data to import.

    Returns:
        ImportStockHolderInfosResponse: List of successfully parsed stock_holder_info data.

    Raises:
        HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
        HTTPException(403 Forbidden): If the current user lacks access rights.
    """

    import_stock_holder_infos_resp: list[ImportStockHolderInfo] = await stock_holder_info_service.import_stock_holder_infos(
        req=req
    )
    return ImportStockHolderInfosResponse(stock_holder_infos=import_stock_holder_infos_resp)