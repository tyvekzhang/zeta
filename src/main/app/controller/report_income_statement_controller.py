# SPDX-License-Identifier: MIT
"""ReportIncomeStatement REST Controller"""
from __future__ import annotations
from typing import Annotated

from fastlib.response import ListResponse, HttpResponse
from fastapi import APIRouter, Query, Form
from starlette.responses import StreamingResponse

from src.main.app.mapper.report_income_statement_mapper import reportIncomeStatementMapper
from src.main.app.model.report_income_statement_model import ReportIncomeStatementModel
from src.main.app.schema.report_income_statement_schema import (
    ListReportIncomeStatementsRequest,
    ReportIncomeStatement,
    CreateReportIncomeStatementRequest,
    ReportIncomeStatementDetail,
    UpdateReportIncomeStatementRequest,
    BatchDeleteReportIncomeStatementsRequest,
    BatchUpdateReportIncomeStatementsRequest,
    BatchUpdateReportIncomeStatementsResponse,
    BatchCreateReportIncomeStatementsRequest,
    BatchCreateReportIncomeStatementsResponse,
    ExportReportIncomeStatementsRequest,
    ImportReportIncomeStatementsResponse,
    BatchGetReportIncomeStatementsResponse,
    ImportReportIncomeStatementsRequest,
    ImportReportIncomeStatement, BatchPatchReportIncomeStatementsRequest,
)
from src.main.app.service.impl.report_income_statement_service_impl import ReportIncomeStatementServiceImpl
from src.main.app.service.report_income_statement_service import ReportIncomeStatementService

report_income_statement_router = APIRouter()
report_income_statement_service: ReportIncomeStatementService = ReportIncomeStatementServiceImpl(mapper=reportIncomeStatementMapper)

@report_income_statement_router.post("/reportIncomeStatements:syncManually")
async def sync_stocks_manual(year: int, quarter: int):
    """
    手动同步 akshare 的股票利润表信息。
    """
    await report_income_statement_service.sync_manually(year, quarter)
    return HttpResponse.success()

@report_income_statement_router.get("/reportIncomeStatements/{id}")
async def get_report_income_statement(id: int) -> ReportIncomeStatementDetail:
    """
    Retrieve report_income_statement details.

    Args:

        id: Unique ID of the report_income_statement resource.

    Returns:

        ReportIncomeStatementDetail: The report_income_statement object containing all its details.

    Raises:

        HTTPException(403 Forbidden): If the current user does not have permission.
        HTTPException(404 Not Found): If the requested report_income_statement does not exist.
    """
    report_income_statement_record: ReportIncomeStatementModel = await report_income_statement_service.get_report_income_statement(id=id)
    return ReportIncomeStatementDetail(**report_income_statement_record.model_dump())


@report_income_statement_router.get("/reportIncomeStatements")
async def list_report_income_statements(
    req: Annotated[ListReportIncomeStatementsRequest, Query()],
) -> ListResponse[ReportIncomeStatement]:
    """
    List report_income_statements with pagination.

    Args:

        req: Request object containing pagination, filter and sort parameters.

    Returns:

        ListResponse: Paginated list of report_income_statements and total count.

    Raises:

        HTTPException(403 Forbidden): If user don't have access rights.
    """
    report_income_statement_records, total = await report_income_statement_service.list_report_income_statements(req=req)
    return ListResponse(records=report_income_statement_records, total=total)


@report_income_statement_router.post("/reportIncomeStatements")
async def creat_report_income_statement(
    req: CreateReportIncomeStatementRequest,
) -> ReportIncomeStatement:
    """
    Create a new report_income_statement.

    Args:

        req: Request object containing report_income_statement creation data.

    Returns:

         ReportIncomeStatement: The report_income_statement object.

    Raises:

        HTTPException(403 Forbidden): If the current user don't have access rights.
        HTTPException(409 Conflict): If the creation data already exists.
    """
    report_income_statement: ReportIncomeStatementModel = await report_income_statement_service.create_report_income_statement(req=req)
    return ReportIncomeStatement(**report_income_statement.model_dump())


@report_income_statement_router.put("/reportIncomeStatements")
async def update_report_income_statement(
    req: UpdateReportIncomeStatementRequest,
) -> ReportIncomeStatement:
    """
    Update an existing report_income_statement.

    Args:

        req: Request object containing report_income_statement update data.

    Returns:

        ReportIncomeStatement: The updated report_income_statement object.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have update permissions.
        HTTPException(404 Not Found): If the report_income_statement to update doesn't exist.
    """
    report_income_statement: ReportIncomeStatementModel = await report_income_statement_service.update_report_income_statement(req=req)
    return ReportIncomeStatement(**report_income_statement.model_dump())


@report_income_statement_router.delete("/reportIncomeStatements/{id}")
async def delete_report_income_statement(
    id: int,
) -> None:
    """
    Delete report_income_statement by ID.

    Args:

        id: The ID of the report_income_statement to delete.

    Raises:

        HTTPException(403 Forbidden): If the current user doesn't have access permissions.
        HTTPException(404 Not Found): If the report_income_statement with given ID doesn't exist.
    """
    await report_income_statement_service.delete_report_income_statement(id=id)


# @report_income_statement_router.get("/reportIncomeStatements:batchGet")
# async def batch_get_report_income_statements(
#     ids: list[int] = Query(..., description="List of report_income_statement IDs to retrieve"),
# ) -> BatchGetReportIncomeStatementsResponse:
#     """
#     Retrieves multiple report_income_statements by their IDs.
# 
#     Args:
# 
#         ids (list[int]): A list of report_income_statement resource IDs.
# 
#     Returns:
# 
#         list[ReportIncomeStatementDetail]: A list of report_income_statement objects matching the provided IDs.
# 
#     Raises:
# 
#         HTTPException(403 Forbidden): If the current user does not have access rights.
#         HTTPException(404 Not Found): If one of the requested report_income_statements does not exist.
#     """
#     report_income_statement_records: list[ReportIncomeStatementModel] = await report_income_statement_service.batch_get_report_income_statements(ids)
#     report_income_statement_detail_list: list[ReportIncomeStatementDetail] = [
#         ReportIncomeStatementDetail(**report_income_statement_record.model_dump()) for report_income_statement_record in report_income_statement_records
#     ]
#     return BatchGetReportIncomeStatementsResponse(report_income_statements=report_income_statement_detail_list)
# 
# 
# @report_income_statement_router.post("/reportIncomeStatements:batchCreate")
# async def batch_create_report_income_statements(
#     req: BatchCreateReportIncomeStatementsRequest,
# ) -> BatchCreateReportIncomeStatementsResponse:
#     """
#     Batch create report_income_statements.
# 
#     Args:
# 
#         req (BatchCreateReportIncomeStatementsRequest): Request body containing a list of report_income_statement creation items.
# 
#     Returns:
# 
#         BatchCreateReportIncomeStatementsResponse: Response containing the list of created report_income_statements.
# 
#     Raises:
# 
#         HTTPException(403 Forbidden): If the current user lacks access rights.
#         HTTPException(409 Conflict): If any report_income_statement creation data already exists.
#     """
# 
#     report_income_statement_records = await report_income_statement_service.batch_create_report_income_statements(req=req)
#     report_income_statement_list: list[ReportIncomeStatement] = [
#         ReportIncomeStatement(**report_income_statement_record.model_dump()) for report_income_statement_record in report_income_statement_records
#     ]
#     return BatchCreateReportIncomeStatementsResponse(report_income_statements=report_income_statement_list)
# 
# 
# @report_income_statement_router.post("/reportIncomeStatements:batchUpdate")
# async def batch_update_report_income_statements(
#     req: BatchUpdateReportIncomeStatementsRequest,
# ) -> BatchUpdateReportIncomeStatementsResponse:
#     """
#     Batch update multiple report_income_statements with the same changes.
# 
#     Args:
# 
#         req (BatchUpdateReportIncomeStatementsRequest): The batch update request data with ids.
# 
#     Returns:
# 
#         BatchUpdateBooksResponse: Contains the list of updated report_income_statements.
# 
#     Raises:
# 
#         HTTPException 403 (Forbidden): If user lacks permission to modify report_income_statements
#         HTTPException 404 (Not Found): If any specified report_income_statement ID doesn't exist
#     """
#     report_income_statement_records: list[ReportIncomeStatementModel] = await report_income_statement_service.batch_update_report_income_statements(req=req)
#     report_income_statement_list: list[ReportIncomeStatement] = [ReportIncomeStatement(**report_income_statement.model_dump()) for report_income_statement in report_income_statement_records]
#     return BatchUpdateReportIncomeStatementsResponse(report_income_statements=report_income_statement_list)
# 
# 
# @report_income_statement_router.post("/reportIncomeStatements:batchPatch")
# async def batch_patch_report_income_statements(
#     req: BatchPatchReportIncomeStatementsRequest,
# ) -> BatchUpdateReportIncomeStatementsResponse:
#     """
#     Batch update multiple report_income_statements with individual changes.
# 
#     Args:
# 
#         req (BatchPatchReportIncomeStatementsRequest): The batch patch request data.
# 
#     Returns:
# 
#         BatchUpdateBooksResponse: Contains the list of updated report_income_statements.
# 
#     Raises:
# 
#         HTTPException 403 (Forbidden): If user lacks permission to modify report_income_statements
#         HTTPException 404 (Not Found): If any specified report_income_statement ID doesn't exist
#     """
#     report_income_statement_records: list[ReportIncomeStatementModel] = await report_income_statement_service.batch_patch_report_income_statements(req=req)
#     report_income_statement_list: list[ReportIncomeStatement] = [ReportIncomeStatement(**report_income_statement.model_dump()) for report_income_statement in report_income_statement_records]
#     return BatchUpdateReportIncomeStatementsResponse(report_income_statements=report_income_statement_list)
# 
# 
# @report_income_statement_router.post("/reportIncomeStatements:batchDelete")
# async def batch_delete_report_income_statements(
#     req: BatchDeleteReportIncomeStatementsRequest,
# ) -> None:
#     """
#     Batch delete report_income_statements.
# 
#     Args:
#         req (BatchDeleteReportIncomeStatementsRequest): Request object containing delete info.
# 
#     Raises:
#         HTTPException(404 Not Found): If any of the report_income_statements do not exist.
#         HTTPException(403 Forbidden): If user don't have access rights.
#     """
#     await report_income_statement_service.batch_delete_report_income_statements(req=req)
# 
# 
# @report_income_statement_router.get("/reportIncomeStatements:exportTemplate")
# async def export_report_income_statements_template() -> StreamingResponse:
#     """
#     Export the Excel template for report_income_statement import.
# 
#     Returns:
#         StreamingResponse: An Excel file stream containing the import template.
# 
#     Raises:
#         HTTPException(403 Forbidden): If user don't have access rights.
#     """
# 
#     return await report_income_statement_service.export_report_income_statements_template()
# 
# 
# @report_income_statement_router.get("/reportIncomeStatements:export")
# async def export_report_income_statements(
#     req: ExportReportIncomeStatementsRequest = Query(...),
# ) -> StreamingResponse:
#     """
#     Export report_income_statement data based on the provided report_income_statement IDs.
# 
#     Args:
#         req (ExportReportIncomeStatementsRequest): Query parameters specifying the report_income_statements to export.
# 
#     Returns:
#         StreamingResponse: A streaming response containing the generated Excel file.
# 
#     Raises:
#         HTTPException(403 Forbidden): If the current user lacks access rights.
#         HTTPException(404 Not Found ): If no matching report_income_statements are found.
#     """
#     return await report_income_statement_service.export_report_income_statements(
#         req=req,
#     )
# 
# @report_income_statement_router.post("/reportIncomeStatements:import")
# async def import_report_income_statements(
#     req: ImportReportIncomeStatementsRequest = Form(...),
# ) -> ImportReportIncomeStatementsResponse:
#     """
#     Import report_income_statements from an uploaded Excel file.
# 
#     Args:
#         req (UploadFile): The Excel file containing report_income_statement data to import.
# 
#     Returns:
#         ImportReportIncomeStatementsResponse: List of successfully parsed report_income_statement data.
# 
#     Raises:
#         HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
#         HTTPException(403 Forbidden): If the current user lacks access rights.
#     """
# 
#     import_report_income_statements_resp: list[ImportReportIncomeStatement] = await report_income_statement_service.import_report_income_statements(
#         req=req
#     )
#     return ImportReportIncomeStatementsResponse(report_income_statements=import_report_income_statements_resp)
# 