# # SPDX-License-Identifier: MIT
# """StockCapitalFlow REST Controller"""
# from __future__ import annotations
# from typing import Annotated

# from fastlib.response import ListResponse
# from fastapi import APIRouter, Query, Form
# from starlette.responses import StreamingResponse

# from src.main.app.mapper.stock_capital_flow_mapper import stockCapitalFlowMapper
# from src.main.app.model.stock_capital_flow_model import StockCapitalFlowModel
# from src.main.app.schema.stock_capital_flow_schema import (
#     ListStockCapitalFlowsRequest,
#     StockCapitalFlow,
#     CreateStockCapitalFlowRequest,
#     StockCapitalFlowDetail,
#     UpdateStockCapitalFlowRequest,
#     BatchDeleteStockCapitalFlowsRequest,
#     BatchUpdateStockCapitalFlowsRequest,
#     BatchUpdateStockCapitalFlowsResponse,
#     BatchCreateStockCapitalFlowsRequest,
#     BatchCreateStockCapitalFlowsResponse,
#     ExportStockCapitalFlowsRequest,
#     ImportStockCapitalFlowsResponse,
#     BatchGetStockCapitalFlowsResponse,
#     ImportStockCapitalFlowsRequest,
#     ImportStockCapitalFlow, BatchPatchStockCapitalFlowsRequest,
# )
# from src.main.app.service.impl.stock_capital_flow_service_impl import StockCapitalFlowServiceImpl
# from src.main.app.service.stock_capital_flow_service import StockCapitalFlowService

# stock_capital_flow_router = APIRouter()
# stock_capital_flow_service: StockCapitalFlowService = StockCapitalFlowServiceImpl(mapper=stockCapitalFlowMapper)


# @stock_capital_flow_router.get("/stockCapitalFlows/{id}")
# async def get_stock_capital_flow(id: int) -> StockCapitalFlowDetail:
#     """
#     Retrieve stock_capital_flow details.

#     Args:

#         id: Unique ID of the stock_capital_flow resource.

#     Returns:

#         StockCapitalFlowDetail: The stock_capital_flow object containing all its details.

#     Raises:

#         HTTPException(403 Forbidden): If the current user does not have permission.
#         HTTPException(404 Not Found): If the requested stock_capital_flow does not exist.
#     """
#     stock_capital_flow_record: StockCapitalFlowModel = await stock_capital_flow_service.get_stock_capital_flow(id=id)
#     return StockCapitalFlowDetail(**stock_capital_flow_record.model_dump())


# @stock_capital_flow_router.get("/stockCapitalFlows")
# async def list_stock_capital_flows(
#     req: Annotated[ListStockCapitalFlowsRequest, Query()],
# ) -> ListResponse[StockCapitalFlow]:
#     """
#     List stock_capital_flows with pagination.

#     Args:

#         req: Request object containing pagination, filter and sort parameters.

#     Returns:

#         ListResponse: Paginated list of stock_capital_flows and total count.

#     Raises:

#         HTTPException(403 Forbidden): If user don't have access rights.
#     """
#     stock_capital_flow_records, total = await stock_capital_flow_service.list_stock_capital_flows(req=req)
#     return ListResponse(records=stock_capital_flow_records, total=total)


# @stock_capital_flow_router.post("/stockCapitalFlows")
# async def creat_stock_capital_flow(
#     req: CreateStockCapitalFlowRequest,
# ) -> StockCapitalFlow:
#     """
#     Create a new stock_capital_flow.

#     Args:

#         req: Request object containing stock_capital_flow creation data.

#     Returns:

#          StockCapitalFlow: The stock_capital_flow object.

#     Raises:

#         HTTPException(403 Forbidden): If the current user don't have access rights.
#         HTTPException(409 Conflict): If the creation data already exists.
#     """
#     stock_capital_flow: StockCapitalFlowModel = await stock_capital_flow_service.create_stock_capital_flow(req=req)
#     return StockCapitalFlow(**stock_capital_flow.model_dump())


# @stock_capital_flow_router.put("/stockCapitalFlows")
# async def update_stock_capital_flow(
#     req: UpdateStockCapitalFlowRequest,
# ) -> StockCapitalFlow:
#     """
#     Update an existing stock_capital_flow.

#     Args:

#         req: Request object containing stock_capital_flow update data.

#     Returns:

#         StockCapitalFlow: The updated stock_capital_flow object.

#     Raises:

#         HTTPException(403 Forbidden): If the current user doesn't have update permissions.
#         HTTPException(404 Not Found): If the stock_capital_flow to update doesn't exist.
#     """
#     stock_capital_flow: StockCapitalFlowModel = await stock_capital_flow_service.update_stock_capital_flow(req=req)
#     return StockCapitalFlow(**stock_capital_flow.model_dump())


# @stock_capital_flow_router.delete("/stockCapitalFlows/{id}")
# async def delete_stock_capital_flow(
#     id: int,
# ) -> None:
#     """
#     Delete stock_capital_flow by ID.

#     Args:

#         id: The ID of the stock_capital_flow to delete.

#     Raises:

#         HTTPException(403 Forbidden): If the current user doesn't have access permissions.
#         HTTPException(404 Not Found): If the stock_capital_flow with given ID doesn't exist.
#     """
#     await stock_capital_flow_service.delete_stock_capital_flow(id=id)


# @stock_capital_flow_router.get("/stockCapitalFlows:batchGet")
# async def batch_get_stock_capital_flows(
#     ids: list[int] = Query(..., description="List of stock_capital_flow IDs to retrieve"),
# ) -> BatchGetStockCapitalFlowsResponse:
#     """
#     Retrieves multiple stock_capital_flows by their IDs.

#     Args:

#         ids (list[int]): A list of stock_capital_flow resource IDs.

#     Returns:

#         list[StockCapitalFlowDetail]: A list of stock_capital_flow objects matching the provided IDs.

#     Raises:

#         HTTPException(403 Forbidden): If the current user does not have access rights.
#         HTTPException(404 Not Found): If one of the requested stock_capital_flows does not exist.
#     """
#     stock_capital_flow_records: list[StockCapitalFlowModel] = await stock_capital_flow_service.batch_get_stock_capital_flows(ids)
#     stock_capital_flow_detail_list: list[StockCapitalFlowDetail] = [
#         StockCapitalFlowDetail(**stock_capital_flow_record.model_dump()) for stock_capital_flow_record in stock_capital_flow_records
#     ]
#     return BatchGetStockCapitalFlowsResponse(stock_capital_flows=stock_capital_flow_detail_list)


# @stock_capital_flow_router.post("/stockCapitalFlows:batchCreate")
# async def batch_create_stock_capital_flows(
#     req: BatchCreateStockCapitalFlowsRequest,
# ) -> BatchCreateStockCapitalFlowsResponse:
#     """
#     Batch create stock_capital_flows.

#     Args:

#         req (BatchCreateStockCapitalFlowsRequest): Request body containing a list of stock_capital_flow creation items.

#     Returns:

#         BatchCreateStockCapitalFlowsResponse: Response containing the list of created stock_capital_flows.

#     Raises:

#         HTTPException(403 Forbidden): If the current user lacks access rights.
#         HTTPException(409 Conflict): If any stock_capital_flow creation data already exists.
#     """

#     stock_capital_flow_records = await stock_capital_flow_service.batch_create_stock_capital_flows(req=req)
#     stock_capital_flow_list: list[StockCapitalFlow] = [
#         StockCapitalFlow(**stock_capital_flow_record.model_dump()) for stock_capital_flow_record in stock_capital_flow_records
#     ]
#     return BatchCreateStockCapitalFlowsResponse(stock_capital_flows=stock_capital_flow_list)


# @stock_capital_flow_router.post("/stockCapitalFlows:batchUpdate")
# async def batch_update_stock_capital_flows(
#     req: BatchUpdateStockCapitalFlowsRequest,
# ) -> BatchUpdateStockCapitalFlowsResponse:
#     """
#     Batch update multiple stock_capital_flows with the same changes.

#     Args:

#         req (BatchUpdateStockCapitalFlowsRequest): The batch update request data with ids.

#     Returns:

#         BatchUpdateBooksResponse: Contains the list of updated stock_capital_flows.

#     Raises:

#         HTTPException 403 (Forbidden): If user lacks permission to modify stock_capital_flows
#         HTTPException 404 (Not Found): If any specified stock_capital_flow ID doesn't exist
#     """
#     stock_capital_flow_records: list[StockCapitalFlowModel] = await stock_capital_flow_service.batch_update_stock_capital_flows(req=req)
#     stock_capital_flow_list: list[StockCapitalFlow] = [StockCapitalFlow(**stock_capital_flow.model_dump()) for stock_capital_flow in stock_capital_flow_records]
#     return BatchUpdateStockCapitalFlowsResponse(stock_capital_flows=stock_capital_flow_list)


# @stock_capital_flow_router.post("/stockCapitalFlows:batchPatch")
# async def batch_patch_stock_capital_flows(
#     req: BatchPatchStockCapitalFlowsRequest,
# ) -> BatchUpdateStockCapitalFlowsResponse:
#     """
#     Batch update multiple stock_capital_flows with individual changes.

#     Args:

#         req (BatchPatchStockCapitalFlowsRequest): The batch patch request data.

#     Returns:

#         BatchUpdateBooksResponse: Contains the list of updated stock_capital_flows.

#     Raises:

#         HTTPException 403 (Forbidden): If user lacks permission to modify stock_capital_flows
#         HTTPException 404 (Not Found): If any specified stock_capital_flow ID doesn't exist
#     """
#     stock_capital_flow_records: list[StockCapitalFlowModel] = await stock_capital_flow_service.batch_patch_stock_capital_flows(req=req)
#     stock_capital_flow_list: list[StockCapitalFlow] = [StockCapitalFlow(**stock_capital_flow.model_dump()) for stock_capital_flow in stock_capital_flow_records]
#     return BatchUpdateStockCapitalFlowsResponse(stock_capital_flows=stock_capital_flow_list)


# @stock_capital_flow_router.post("/stockCapitalFlows:batchDelete")
# async def batch_delete_stock_capital_flows(
#     req: BatchDeleteStockCapitalFlowsRequest,
# ) -> None:
#     """
#     Batch delete stock_capital_flows.

#     Args:
#         req (BatchDeleteStockCapitalFlowsRequest): Request object containing delete info.

#     Raises:
#         HTTPException(404 Not Found): If any of the stock_capital_flows do not exist.
#         HTTPException(403 Forbidden): If user don't have access rights.
#     """
#     await stock_capital_flow_service.batch_delete_stock_capital_flows(req=req)


# @stock_capital_flow_router.get("/stockCapitalFlows:exportTemplate")
# async def export_stock_capital_flows_template() -> StreamingResponse:
#     """
#     Export the Excel template for stock_capital_flow import.

#     Returns:
#         StreamingResponse: An Excel file stream containing the import template.

#     Raises:
#         HTTPException(403 Forbidden): If user don't have access rights.
#     """

#     return await stock_capital_flow_service.export_stock_capital_flows_template()


# @stock_capital_flow_router.get("/stockCapitalFlows:export")
# async def export_stock_capital_flows(
#     req: ExportStockCapitalFlowsRequest = Query(...),
# ) -> StreamingResponse:
#     """
#     Export stock_capital_flow data based on the provided stock_capital_flow IDs.

#     Args:
#         req (ExportStockCapitalFlowsRequest): Query parameters specifying the stock_capital_flows to export.

#     Returns:
#         StreamingResponse: A streaming response containing the generated Excel file.

#     Raises:
#         HTTPException(403 Forbidden): If the current user lacks access rights.
#         HTTPException(404 Not Found ): If no matching stock_capital_flows are found.
#     """
#     return await stock_capital_flow_service.export_stock_capital_flows(
#         req=req,
#     )

# @stock_capital_flow_router.post("/stockCapitalFlows:import")
# async def import_stock_capital_flows(
#     req: ImportStockCapitalFlowsRequest = Form(...),
# ) -> ImportStockCapitalFlowsResponse:
#     """
#     Import stock_capital_flows from an uploaded Excel file.

#     Args:
#         req (UploadFile): The Excel file containing stock_capital_flow data to import.

#     Returns:
#         ImportStockCapitalFlowsResponse: List of successfully parsed stock_capital_flow data.

#     Raises:
#         HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
#         HTTPException(403 Forbidden): If the current user lacks access rights.
#     """

#     import_stock_capital_flows_resp: list[ImportStockCapitalFlow] = await stock_capital_flow_service.import_stock_capital_flows(
#         req=req
#     )
#     return ImportStockCapitalFlowsResponse(stock_capital_flows=import_stock_capital_flows_resp)