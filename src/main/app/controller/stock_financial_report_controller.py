# SPDX-License-Identifier: MIT
"""StockFinancialReport REST Controller"""
from __future__ import annotations
from typing import Annotated

from fastlib.response import ListResponse
from fastapi import APIRouter, Query, Form
from starlette.responses import StreamingResponse

from src.main.app.mapper.stock_financial_report_mapper import stockFinancialReportMapper
from src.main.app.model.stock_financial_report_model import StockFinancialReportModel
from src.main.app.schema.stock_financial_report_schema import (
    ListStockFinancialReportsRequest,
    StockFinancialReport,
    CreateStockFinancialReportRequest,
    StockFinancialReportDetail,
    UpdateStockFinancialReportRequest,
    BatchDeleteStockFinancialReportsRequest,
    BatchUpdateStockFinancialReportsRequest,
    BatchUpdateStockFinancialReportsResponse,
    BatchCreateStockFinancialReportsRequest,
    BatchCreateStockFinancialReportsResponse,
    ExportStockFinancialReportsRequest,
    ImportStockFinancialReportsResponse,
    BatchGetStockFinancialReportsResponse,
    ImportStockFinancialReportsRequest,
    ImportStockFinancialReport, BatchPatchStockFinancialReportsRequest,
)
from src.main.app.service.impl.stock_financial_report_service_impl import StockFinancialReportServiceImpl
from src.main.app.service.stock_financial_report_service import StockFinancialReportService

stock_financial_report_router = APIRouter()
stock_financial_report_service: StockFinancialReportService = StockFinancialReportServiceImpl(mapper=stockFinancialReportMapper)


@stock_financial_report_router.get("/stockFinancialReports/{id}")
async def get_stock_financial_report(id: int) -> StockFinancialReportDetail:
    """
    Retrieve stock_financial_report details.

    Args:

        id: Unique ID of the stock_financial_report resource.

    Returns:

        StockFinancialReportDetail: The stock_financial_report object containing all its details.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have permission.
        HTTPException(404 Not Found): If the requested stock_financial_report does not exist.
    """
    stock_financial_report_record: StockFinancialReportModel = await stock_financial_report_service.get_stock_financial_report(id=id)
    return StockFinancialReportDetail(**stock_financial_report_record.model_dump())


@stock_financial_report_router.get("/stockFinancialReports")
async def list_stock_financial_reports(
    req: Annotated[ListStockFinancialReportsRequest, Query()],
) -> ListResponse[StockFinancialReport]:
    """
    List stock_financial_reports with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        ListResponse: Paginated list of stock_financial_reports and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    stock_financial_report_records, total = await stock_financial_report_service.list_stock_financial_reports(req=req)
    return ListResponse(records=stock_financial_report_records, total=total)


@stock_financial_report_router.post("/stockFinancialReports")
async def creat_stock_financial_report(
    req: CreateStockFinancialReportRequest,
) -> StockFinancialReport:
    """
    Create a new stock_financial_report.

    Args:

        req: Request object containing stock_financial_report creation data.

    Returns:

         StockFinancialReport: The stock_financial_report object.

    Raises:

        HTTPException(403 Forbidden): If the current user don't have access rights.
        HTTPException(409 Conflict): If the creation data already exists.
    """
    stock_financial_report: StockFinancialReportModel = await stock_financial_report_service.create_stock_financial_report(req=req)
    return StockFinancialReport(**stock_financial_report.model_dump())


@stock_financial_report_router.put("/stockFinancialReports")
async def update_stock_financial_report(
    req: UpdateStockFinancialReportRequest,
) -> StockFinancialReport:
    """
    Update an existing stock_financial_report.

    Args:

        req: Request object containing stock_financial_report update data.

    Returns:

        StockFinancialReport: The updated stock_financial_report object.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have update permissions.
        HTTPException(404 Not Found): If the stock_financial_report to update doesn't exist.
    """
    stock_financial_report: StockFinancialReportModel = await stock_financial_report_service.update_stock_financial_report(req=req)
    return StockFinancialReport(**stock_financial_report.model_dump())


@stock_financial_report_router.delete("/stockFinancialReports/{id}")
async def delete_stock_financial_report(
    id: int,
) -> None:
    """
    Delete stock_financial_report by ID.

    Args:

        id: The ID of the stock_financial_report to delete.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have access permissions.
        HTTPException(404 Not Found): If the stock_financial_report with given ID doesn't exist.
    """
    await stock_financial_report_service.delete_stock_financial_report(id=id)


@stock_financial_report_router.get("/stockFinancialReports:batchGet")
async def batch_get_stock_financial_reports(
    ids: list[int] = Query(..., description="List of stock_financial_report IDs to retrieve"),
) -> BatchGetStockFinancialReportsResponse:
    """
    Retrieves multiple stock_financial_reports by their IDs.

    Args:

        ids (list[int]): A list of stock_financial_report resource IDs.

    Returns:

        list[StockFinancialReportDetail]: A list of stock_financial_report objects matching the provided IDs.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have access rights.
        HTTPException(404 Not Found): If one of the requested stock_financial_reports does not exist.
    """
    stock_financial_report_records: list[StockFinancialReportModel] = await stock_financial_report_service.batch_get_stock_financial_reports(ids)
    stock_financial_report_detail_list: list[StockFinancialReportDetail] = [
        StockFinancialReportDetail(**stock_financial_report_record.model_dump()) for stock_financial_report_record in stock_financial_report_records
    ]
    return BatchGetStockFinancialReportsResponse(stock_financial_reports=stock_financial_report_detail_list)


@stock_financial_report_router.post("/stockFinancialReports:batchCreate")
async def batch_create_stock_financial_reports(
    req: BatchCreateStockFinancialReportsRequest,
) -> BatchCreateStockFinancialReportsResponse:
    """
    Batch create stock_financial_reports.

    Args:

        req (BatchCreateStockFinancialReportsRequest): Request body containing a list of stock_financial_report creation items.

    Returns:

        BatchCreateStockFinancialReportsResponse: Response containing the list of created stock_financial_reports.

    Raises:

        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(409 Conflict): If any stock_financial_report creation data already exists.
    """

    stock_financial_report_records = await stock_financial_report_service.batch_create_stock_financial_reports(req=req)
    stock_financial_report_list: list[StockFinancialReport] = [
        StockFinancialReport(**stock_financial_report_record.model_dump()) for stock_financial_report_record in stock_financial_report_records
    ]
    return BatchCreateStockFinancialReportsResponse(stock_financial_reports=stock_financial_report_list)


@stock_financial_report_router.post("/stockFinancialReports:batchUpdate")
async def batch_update_stock_financial_reports(
    req: BatchUpdateStockFinancialReportsRequest,
) -> BatchUpdateStockFinancialReportsResponse:
    """
    Batch update multiple stock_financial_reports with the same changes.

    Args:

        req (BatchUpdateStockFinancialReportsRequest): The batch update request data with ids.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated stock_financial_reports.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify stock_financial_reports
        HTTPException 404 (Not Found): If any specified stock_financial_report ID doesn't exist
    """
    stock_financial_report_records: list[StockFinancialReportModel] = await stock_financial_report_service.batch_update_stock_financial_reports(req=req)
    stock_financial_report_list: list[StockFinancialReport] = [StockFinancialReport(**stock_financial_report.model_dump()) for stock_financial_report in stock_financial_report_records]
    return BatchUpdateStockFinancialReportsResponse(stock_financial_reports=stock_financial_report_list)


@stock_financial_report_router.post("/stockFinancialReports:batchPatch")
async def batch_patch_stock_financial_reports(
    req: BatchPatchStockFinancialReportsRequest,
) -> BatchUpdateStockFinancialReportsResponse:
    """
    Batch update multiple stock_financial_reports with individual changes.

    Args:

        req (BatchPatchStockFinancialReportsRequest): The batch patch request data.

    Returns:

        BatchUpdateBooksResponse: Contains the list of updated stock_financial_reports.

    Raises:

        HTTPException 403 (Forbidden): If user lacks permission to modify stock_financial_reports
        HTTPException 404 (Not Found): If any specified stock_financial_report ID doesn't exist
    """
    stock_financial_report_records: list[StockFinancialReportModel] = await stock_financial_report_service.batch_patch_stock_financial_reports(req=req)
    stock_financial_report_list: list[StockFinancialReport] = [StockFinancialReport(**stock_financial_report.model_dump()) for stock_financial_report in stock_financial_report_records]
    return BatchUpdateStockFinancialReportsResponse(stock_financial_reports=stock_financial_report_list)


@stock_financial_report_router.post("/stockFinancialReports:batchDelete")
async def batch_delete_stock_financial_reports(
    req: BatchDeleteStockFinancialReportsRequest,
) -> None:
    """
    Batch delete stock_financial_reports.

    Args:
        req (BatchDeleteStockFinancialReportsRequest): Request object containing delete info.

    Raises:
        HTTPException(404 Not Found): If any of the stock_financial_reports do not exist.
        HTTPException(403 Forbidden): If user don't have access rights.
    """
    await stock_financial_report_service.batch_delete_stock_financial_reports(req=req)


@stock_financial_report_router.get("/stockFinancialReports:exportTemplate")
async def export_stock_financial_reports_template() -> StreamingResponse:
    """
    Export the Excel template for stock_financial_report import.

    Returns:
        StreamingResponse: An Excel file stream containing the import template.

    Raises:
        HTTPException(403 Forbidden): If user don't have access rights.
    """

    return await stock_financial_report_service.export_stock_financial_reports_template()


@stock_financial_report_router.get("/stockFinancialReports:export")
async def export_stock_financial_reports(
    req: ExportStockFinancialReportsRequest = Query(...),
) -> StreamingResponse:
    """
    Export stock_financial_report data based on the provided stock_financial_report IDs.

    Args:
        req (ExportStockFinancialReportsRequest): Query parameters specifying the stock_financial_reports to export.

    Returns:
        StreamingResponse: A streaming response containing the generated Excel file.

    Raises:
        HTTPException(403 Forbidden): If the current user lacks access rights.
        HTTPException(404 Not Found ): If no matching stock_financial_reports are found.
    """
    return await stock_financial_report_service.export_stock_financial_reports(
        req=req,
    )

@stock_financial_report_router.post("/stockFinancialReports:import")
async def import_stock_financial_reports(
    req: ImportStockFinancialReportsRequest = Form(...),
) -> ImportStockFinancialReportsResponse:
    """
    Import stock_financial_reports from an uploaded Excel file.

    Args:
        req (UploadFile): The Excel file containing stock_financial_report data to import.

    Returns:
        ImportStockFinancialReportsResponse: List of successfully parsed stock_financial_report data.

    Raises:
        HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
        HTTPException(403 Forbidden): If the current user lacks access rights.
    """

    import_stock_financial_reports_resp: list[ImportStockFinancialReport] = await stock_financial_report_service.import_stock_financial_reports(
        req=req
    )
    return ImportStockFinancialReportsResponse(stock_financial_reports=import_stock_financial_reports_resp)