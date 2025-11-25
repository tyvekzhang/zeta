# SPDX-License-Identifier: MIT
"""Stock REST Controller"""
from __future__ import annotations
from typing import Annotated

from fastlib.response import ListResponse, HttpResponse
from fastapi import APIRouter, Query, Form
from starlette.responses import StreamingResponse

from src.main.app.mapper.stock_mapper import stockMapper
from src.main.app.model.stock_model import StockModel
from src.main.app.schema.stock_schema import (
    ListStocksRequest,
    Stock,
    CreateStockRequest,
    StockDetail,
    UpdateStockRequest,
    BatchDeleteStocksRequest,
    BatchUpdateStocksRequest,
    BatchUpdateStocksResponse,
    BatchCreateStocksRequest,
    BatchCreateStocksResponse,
    ExportStocksRequest,
    ImportStocksResponse,
    BatchGetStocksResponse,
    ImportStocksRequest,
    ImportStock, BatchPatchStocksRequest,
)
from src.main.app.service.impl.stock_service_impl import StockServiceImpl
from src.main.app.service.stock_service import StockService

stock_router = APIRouter()
stock_service: StockService = StockServiceImpl(mapper=stockMapper)

@stock_router.post("/stocks:syncManually")
async def sync_stocks_manual():
    """
    手动同步 akshare 的股票基础数据。
    """
    await stock_service.sync_manually()
    return HttpResponse.success()

@stock_router.get("/stocks/{id}")
async def get_stock(id: int) -> StockDetail:
    """
    Retrieve stock details.

    Args:

        id: Unique ID of the stock resource.

    Returns:

        StockDetail: The stock object containing all its details.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have permission.
        HTTPException(404 Not Found): If the requested stock does not exist.
    """
    stock_record: StockModel = await stock_service.get_stock(id=id)
    return StockDetail(**stock_record.model_dump())


@stock_router.get("/stocks")
async def list_stocks(
    req: Annotated[ListStocksRequest, Query()],
) -> ListResponse[Stock]:
    """
    List stocks with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        ListResponse: Paginated list of stocks and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    stock_records, total = await stock_service.list_stocks(req=req)
    return ListResponse(records=stock_records, total=total)


@stock_router.post("/stocks")
async def creat_stock(
    req: CreateStockRequest,
) -> Stock:
    """
    Create a new stock.

    Args:

        req: Request object containing stock creation data.

    Returns:

         Stock: The stock object.

    Raises:

        HTTPException(403 Forbidden): If the current user don't have access rights.
        HTTPException(409 Conflict): If the creation data already exists.
    """
    stock: StockModel = await stock_service.create_stock(req=req)
    return Stock(**stock.model_dump())


@stock_router.put("/stocks")
async def update_stock(
    req: UpdateStockRequest,
) -> Stock:
    """
    Update an existing stock.

    Args:

        req: Request object containing stock update data.

    Returns:

        Stock: The updated stock object.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have update permissions.
        HTTPException(404 Not Found): If the stock to update doesn't exist.
    """
    stock: StockModel = await stock_service.update_stock(req=req)
    return Stock(**stock.model_dump())


@stock_router.delete("/stocks/{id}")
async def delete_stock(
    id: int,
) -> None:
    """
    Delete stock by ID.

    Args:

        id: The ID of the stock to delete.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have access permissions.
        HTTPException(404 Not Found): If the stock with given ID doesn't exist.
    """
    await stock_service.delete_stock(id=id)


@stock_router.get("/stocks:batchGet")
async def batch_get_stocks(
    ids: list[int] = Query(..., description="List of stock IDs to retrieve"),
) -> BatchGetStocksResponse:
    """
    Retrieves multiple stocks by their IDs.

    Args:

        ids (list[int]): A list of stock resource IDs.

    Returns:

        list[StockDetail]: A list of stock objects matching the provided IDs.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have access rights.
        HTTPException(404 Not Found): If one of the requested stocks does not exist.
    """
    stock_records: list[StockModel] = await stock_service.batch_get_stocks(ids)
    stock_detail_list: list[StockDetail] = [
        StockDetail(**stock_record.model_dump()) for stock_record in stock_records
    ]
    return BatchGetStocksResponse(stocks=stock_detail_list)


@stock_router.post("/stocks:batchCreate")
async def batch_create_stocks(
    req: BatchCreateStocksRequest,
) -> BatchCreateStocksResponse:
    """
    Batch create stocks.

    Args:

        req (BatchCreateStocksRequest): Request body containing a list of stock creation items.

    Returns:

        BatchCreateStocksResponse: Response containing the list of created stocks.

    Raises:

        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(409 Conflict): If any stock creation data already exists.
    """

    stock_records = await stock_service.batch_create_stocks(req=req)
    stock_list: list[Stock] = [
        Stock(**stock_record.model_dump()) for stock_record in stock_records
    ]
    return BatchCreateStocksResponse(stocks=stock_list)


@stock_router.post("/stocks:batchUpdate")
async def batch_update_stocks(
    req: BatchUpdateStocksRequest,
) -> BatchUpdateStocksResponse:
    """
    Batch update multiple stocks with the same changes.

    Args:

        req (BatchUpdateStocksRequest): The batch update request data with ids.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated stocks.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify stocks
        HTTPException 404 (Not Found): If any specified stock ID doesn't exist
    """
    stock_records: list[StockModel] = await stock_service.batch_update_stocks(req=req)
    stock_list: list[Stock] = [Stock(**stock.model_dump()) for stock in stock_records]
    return BatchUpdateStocksResponse(stocks=stock_list)


@stock_router.post("/stocks:batchPatch")
async def batch_patch_stocks(
    req: BatchPatchStocksRequest,
) -> BatchUpdateStocksResponse:
    """
    Batch update multiple stocks with individual changes.

    Args:

        req (BatchPatchStocksRequest): The batch patch request data.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated stocks.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify stocks
        HTTPException 404 (Not Found): If any specified stock ID doesn't exist
    """
    stock_records: list[StockModel] = await stock_service.batch_patch_stocks(req=req)
    stock_list: list[Stock] = [Stock(**stock.model_dump()) for stock in stock_records]
    return BatchUpdateStocksResponse(stocks=stock_list)


@stock_router.post("/stocks:batchDelete")
async def batch_delete_stocks(
    req: BatchDeleteStocksRequest,
) -> None:
    """
    Batch delete stocks.

    Args:
        req (BatchDeleteStocksRequest): Request object containing delete info.

    Raises:
        HTTPException(404 Not Found): If any of the stocks do not exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    await stock_service.batch_delete_stocks(req=req)


@stock_router.get("/stocks:exportTemplate")
async def export_stocks_template() -> StreamingResponse:
    """
    Export the Excel template for stock import.

    Returns:
        StreamingResponse: An Excel file stream containing the import template.

    Raises:
        HTTPException(403 Forbidden): If user don't have access rights.
    """

    return await stock_service.export_stocks_template()


@stock_router.get("/stocks:export")
async def export_stocks(
    req: ExportStocksRequest = Query(...),
) -> StreamingResponse:
    """
    Export stock data based on the provided stock IDs.

    Args:
        req (ExportStocksRequest): Query parameters specifying the stocks to export.

    Returns:
        StreamingResponse: A streaming response containing the generated Excel file.

    Raises:
        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(404 Not Found ): If no matching stocks are found.
    """
    return await stock_service.export_stocks(
        req=req,
    )

@stock_router.post("/stocks:import")
async def import_stocks(
    req: ImportStocksRequest = Form(...),
) -> ImportStocksResponse:
    """
    Import stocks from an uploaded Excel file.

    Args:
        req (UploadFile): The Excel file containing stock data to import.

    Returns:
        ImportStocksResponse: List of successfully parsed stock data.

    Raises:
        HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
        HTTPException(403 Forbidden): If the current user lacks access rights.
    """

    import_stocks_resp: list[ImportStock] = await stock_service.import_stocks(
        req=req
    )
    return ImportStocksResponse(stocks=import_stocks_resp)