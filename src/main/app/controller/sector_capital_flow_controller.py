# # SPDX-License-Identifier: MIT
# """SectorCapitalFlow REST Controller"""
# from __future__ import annotations
# from typing import Annotated

# from fastlib.response import ListResponse
# from fastapi import APIRouter, Query, Form
# from starlette.responses import StreamingResponse

# from src.main.app.mapper.sector_capital_flow_mapper import sectorCapitalFlowMapper
# from src.main.app.model.sector_capital_flow_model import SectorCapitalFlowModel
# from src.main.app.schema.sector_capital_flow_schema import (
#     ListSectorCapitalFlowsRequest,
#     SectorCapitalFlow,
#     CreateSectorCapitalFlowRequest,
#     SectorCapitalFlowDetail,
#     UpdateSectorCapitalFlowRequest,
#     BatchDeleteSectorCapitalFlowsRequest,
#     BatchUpdateSectorCapitalFlowsRequest,
#     BatchUpdateSectorCapitalFlowsResponse,
#     BatchCreateSectorCapitalFlowsRequest,
#     BatchCreateSectorCapitalFlowsResponse,
#     ExportSectorCapitalFlowsRequest,
#     ImportSectorCapitalFlowsResponse,
#     BatchGetSectorCapitalFlowsResponse,
#     ImportSectorCapitalFlowsRequest,
#     ImportSectorCapitalFlow, BatchPatchSectorCapitalFlowsRequest,
# )
# from src.main.app.service.impl.sector_capital_flow_service_impl import SectorCapitalFlowServiceImpl
# from src.main.app.service.sector_capital_flow_service import SectorCapitalFlowService

# sector_capital_flow_router = APIRouter()
# sector_capital_flow_service: SectorCapitalFlowService = SectorCapitalFlowServiceImpl(mapper=sectorCapitalFlowMapper)


# @sector_capital_flow_router.get("/sectorCapitalFlows/{id}")
# async def get_sector_capital_flow(id: int) -> SectorCapitalFlowDetail:
#     """
#     Retrieve sector_capital_flow details.

#     Args:

#         id: Unique ID of the sector_capital_flow resource.

#     Returns:

#         SectorCapitalFlowDetail: The sector_capital_flow object containing all its details.

#     Raises:

#         HTTPException(403 Forbidden): If the current user does not have permission.
#         HTTPException(404 Not Found): If the requested sector_capital_flow does not exist.
#     """
#     sector_capital_flow_record: SectorCapitalFlowModel = await sector_capital_flow_service.get_sector_capital_flow(id=id)
#     return SectorCapitalFlowDetail(**sector_capital_flow_record.model_dump())


# @sector_capital_flow_router.get("/sectorCapitalFlows")
# async def list_sector_capital_flows(
#     req: Annotated[ListSectorCapitalFlowsRequest, Query()],
# ) -> ListResponse[SectorCapitalFlow]:
#     """
#     List sector_capital_flows with pagination.

#     Args:

#         req: Request object containing pagination, filter and sort parameters.

#     Returns:

#         ListResponse: Paginated list of sector_capital_flows and total count.

#     Raises:

#         HTTPException(403 Forbidden): If user don't have access rights.
#     """
#     sector_capital_flow_records, total = await sector_capital_flow_service.list_sector_capital_flows(req=req)
#     return ListResponse(records=sector_capital_flow_records, total=total)


# @sector_capital_flow_router.post("/sectorCapitalFlows")
# async def creat_sector_capital_flow(
#     req: CreateSectorCapitalFlowRequest,
# ) -> SectorCapitalFlow:
#     """
#     Create a new sector_capital_flow.

#     Args:

#         req: Request object containing sector_capital_flow creation data.

#     Returns:

#          SectorCapitalFlow: The sector_capital_flow object.

#     Raises:

#         HTTPException(403 Forbidden): If the current user don't have access rights.
#         HTTPException(409 Conflict): If the creation data already exists.
#     """
#     sector_capital_flow: SectorCapitalFlowModel = await sector_capital_flow_service.create_sector_capital_flow(req=req)
#     return SectorCapitalFlow(**sector_capital_flow.model_dump())


# @sector_capital_flow_router.put("/sectorCapitalFlows")
# async def update_sector_capital_flow(
#     req: UpdateSectorCapitalFlowRequest,
# ) -> SectorCapitalFlow:
#     """
#     Update an existing sector_capital_flow.

#     Args:

#         req: Request object containing sector_capital_flow update data.

#     Returns:

#         SectorCapitalFlow: The updated sector_capital_flow object.

#     Raises:

#         HTTPException(403 Forbidden): If the current user doesn't have update permissions.
#         HTTPException(404 Not Found): If the sector_capital_flow to update doesn't exist.
#     """
#     sector_capital_flow: SectorCapitalFlowModel = await sector_capital_flow_service.update_sector_capital_flow(req=req)
#     return SectorCapitalFlow(**sector_capital_flow.model_dump())


# @sector_capital_flow_router.delete("/sectorCapitalFlows/{id}")
# async def delete_sector_capital_flow(
#     id: int,
# ) -> None:
#     """
#     Delete sector_capital_flow by ID.

#     Args:

#         id: The ID of the sector_capital_flow to delete.

#     Raises:

#         HTTPException(403 Forbidden): If the current user doesn't have access permissions.
#         HTTPException(404 Not Found): If the sector_capital_flow with given ID doesn't exist.
#     """
#     await sector_capital_flow_service.delete_sector_capital_flow(id=id)


# @sector_capital_flow_router.get("/sectorCapitalFlows:batchGet")
# async def batch_get_sector_capital_flows(
#     ids: list[int] = Query(..., description="List of sector_capital_flow IDs to retrieve"),
# ) -> BatchGetSectorCapitalFlowsResponse:
#     """
#     Retrieves multiple sector_capital_flows by their IDs.

#     Args:

#         ids (list[int]): A list of sector_capital_flow resource IDs.

#     Returns:

#         list[SectorCapitalFlowDetail]: A list of sector_capital_flow objects matching the provided IDs.

#     Raises:

#         HTTPException(403 Forbidden): If the current user does not have access rights.
#         HTTPException(404 Not Found): If one of the requested sector_capital_flows does not exist.
#     """
#     sector_capital_flow_records: list[SectorCapitalFlowModel] = await sector_capital_flow_service.batch_get_sector_capital_flows(ids)
#     sector_capital_flow_detail_list: list[SectorCapitalFlowDetail] = [
#         SectorCapitalFlowDetail(**sector_capital_flow_record.model_dump()) for sector_capital_flow_record in sector_capital_flow_records
#     ]
#     return BatchGetSectorCapitalFlowsResponse(sector_capital_flows=sector_capital_flow_detail_list)


# @sector_capital_flow_router.post("/sectorCapitalFlows:batchCreate")
# async def batch_create_sector_capital_flows(
#     req: BatchCreateSectorCapitalFlowsRequest,
# ) -> BatchCreateSectorCapitalFlowsResponse:
#     """
#     Batch create sector_capital_flows.

#     Args:

#         req (BatchCreateSectorCapitalFlowsRequest): Request body containing a list of sector_capital_flow creation items.

#     Returns:

#         BatchCreateSectorCapitalFlowsResponse: Response containing the list of created sector_capital_flows.

#     Raises:

#         HTTPException(403 Forbidden): If the current user lacks access rights.
#         HTTPException(409 Conflict): If any sector_capital_flow creation data already exists.
#     """

#     sector_capital_flow_records = await sector_capital_flow_service.batch_create_sector_capital_flows(req=req)
#     sector_capital_flow_list: list[SectorCapitalFlow] = [
#         SectorCapitalFlow(**sector_capital_flow_record.model_dump()) for sector_capital_flow_record in sector_capital_flow_records
#     ]
#     return BatchCreateSectorCapitalFlowsResponse(sector_capital_flows=sector_capital_flow_list)


# @sector_capital_flow_router.post("/sectorCapitalFlows:batchUpdate")
# async def batch_update_sector_capital_flows(
#     req: BatchUpdateSectorCapitalFlowsRequest,
# ) -> BatchUpdateSectorCapitalFlowsResponse:
#     """
#     Batch update multiple sector_capital_flows with the same changes.

#     Args:

#         req (BatchUpdateSectorCapitalFlowsRequest): The batch update request data with ids.

#     Returns:

#         BatchUpdateBooksResponse: Contains the list of updated sector_capital_flows.

#     Raises:

#         HTTPException 403 (Forbidden): If user lacks permission to modify sector_capital_flows
#         HTTPException 404 (Not Found): If any specified sector_capital_flow ID doesn't exist
#     """
#     sector_capital_flow_records: list[SectorCapitalFlowModel] = await sector_capital_flow_service.batch_update_sector_capital_flows(req=req)
#     sector_capital_flow_list: list[SectorCapitalFlow] = [SectorCapitalFlow(**sector_capital_flow.model_dump()) for sector_capital_flow in sector_capital_flow_records]
#     return BatchUpdateSectorCapitalFlowsResponse(sector_capital_flows=sector_capital_flow_list)


# @sector_capital_flow_router.post("/sectorCapitalFlows:batchPatch")
# async def batch_patch_sector_capital_flows(
#     req: BatchPatchSectorCapitalFlowsRequest,
# ) -> BatchUpdateSectorCapitalFlowsResponse:
#     """
#     Batch update multiple sector_capital_flows with individual changes.

#     Args:

#         req (BatchPatchSectorCapitalFlowsRequest): The batch patch request data.

#     Returns:

#         BatchUpdateBooksResponse: Contains the list of updated sector_capital_flows.

#     Raises:

#         HTTPException 403 (Forbidden): If user lacks permission to modify sector_capital_flows
#         HTTPException 404 (Not Found): If any specified sector_capital_flow ID doesn't exist
#     """
#     sector_capital_flow_records: list[SectorCapitalFlowModel] = await sector_capital_flow_service.batch_patch_sector_capital_flows(req=req)
#     sector_capital_flow_list: list[SectorCapitalFlow] = [SectorCapitalFlow(**sector_capital_flow.model_dump()) for sector_capital_flow in sector_capital_flow_records]
#     return BatchUpdateSectorCapitalFlowsResponse(sector_capital_flows=sector_capital_flow_list)


# @sector_capital_flow_router.post("/sectorCapitalFlows:batchDelete")
# async def batch_delete_sector_capital_flows(
#     req: BatchDeleteSectorCapitalFlowsRequest,
# ) -> None:
#     """
#     Batch delete sector_capital_flows.

#     Args:
#         req (BatchDeleteSectorCapitalFlowsRequest): Request object containing delete info.

#     Raises:
#         HTTPException(404 Not Found): If any of the sector_capital_flows do not exist.
#         HTTPException(403 Forbidden): If user don't have access rights.
#     """
#     await sector_capital_flow_service.batch_delete_sector_capital_flows(req=req)


# @sector_capital_flow_router.get("/sectorCapitalFlows:exportTemplate")
# async def export_sector_capital_flows_template() -> StreamingResponse:
#     """
#     Export the Excel template for sector_capital_flow import.

#     Returns:
#         StreamingResponse: An Excel file stream containing the import template.

#     Raises:
#         HTTPException(403 Forbidden): If user don't have access rights.
#     """

#     return await sector_capital_flow_service.export_sector_capital_flows_template()


# @sector_capital_flow_router.get("/sectorCapitalFlows:export")
# async def export_sector_capital_flows(
#     req: ExportSectorCapitalFlowsRequest = Query(...),
# ) -> StreamingResponse:
#     """
#     Export sector_capital_flow data based on the provided sector_capital_flow IDs.

#     Args:
#         req (ExportSectorCapitalFlowsRequest): Query parameters specifying the sector_capital_flows to export.

#     Returns:
#         StreamingResponse: A streaming response containing the generated Excel file.

#     Raises:
#         HTTPException(403 Forbidden): If the current user lacks access rights.
#         HTTPException(404 Not Found ): If no matching sector_capital_flows are found.
#     """
#     return await sector_capital_flow_service.export_sector_capital_flows(
#         req=req,
#     )

# @sector_capital_flow_router.post("/sectorCapitalFlows:import")
# async def import_sector_capital_flows(
#     req: ImportSectorCapitalFlowsRequest = Form(...),
# ) -> ImportSectorCapitalFlowsResponse:
#     """
#     Import sector_capital_flows from an uploaded Excel file.

#     Args:
#         req (UploadFile): The Excel file containing sector_capital_flow data to import.

#     Returns:
#         ImportSectorCapitalFlowsResponse: List of successfully parsed sector_capital_flow data.

#     Raises:
#         HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
#         HTTPException(403 Forbidden): If the current user lacks access rights.
#     """

#     import_sector_capital_flows_resp: list[ImportSectorCapitalFlow] = await sector_capital_flow_service.import_sector_capital_flows(
#         req=req
#     )
#     return ImportSectorCapitalFlowsResponse(sector_capital_flows=import_sector_capital_flows_resp)