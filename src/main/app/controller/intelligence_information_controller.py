# # SPDX-License-Identifier: MIT
# """IntelligenceInformation REST Controller"""
# from __future__ import annotations
# from typing import Annotated

# from fastlib.response import ListResponse
# from fastapi import APIRouter, Query, Form
# from starlette.responses import StreamingResponse

# from src.main.app.mapper.intelligence_information_mapper import intelligenceInformationMapper
# from src.main.app.model.intelligence_information_model import IntelligenceInformationModel
# from src.main.app.schema.intelligence_information_schema import (
#     ListIntelligenceInformationRequest,
#     IntelligenceInformation,
#     CreateIntelligenceInformationRequest,
#     IntelligenceInformationDetail,
#     UpdateIntelligenceInformationRequest,
#     BatchDeleteIntelligenceInformationRequest,
#     BatchUpdateIntelligenceInformationRequest,
#     BatchUpdateIntelligenceInformationResponse,
#     BatchCreateIntelligenceInformationRequest,
#     BatchCreateIntelligenceInformationResponse,
#     ExportIntelligenceInformationRequest,
#     ImportIntelligenceInformationResponse,
#     BatchGetIntelligenceInformationResponse,
#     ImportIntelligenceInformationRequest,
#     ImportIntelligenceInformation, BatchPatchIntelligenceInformationRequest,
# )
# from src.main.app.service.impl.intelligence_information_service_impl import IntelligenceInformationServiceImpl
# from src.main.app.service.intelligence_information_service import IntelligenceInformationService

# intelligence_information_router = APIRouter()
# intelligence_information_service: IntelligenceInformationService = IntelligenceInformationServiceImpl(mapper=intelligenceInformationMapper)


# @intelligence_information_router.get("/intelligenceInformation/{id}")
# async def get_intelligence_information(id: int) -> IntelligenceInformationDetail:
#     """
#     Retrieve intelligence_information details.

#     Args:

#         id: Unique ID of the intelligence_information resource.

#     Returns:

#         IntelligenceInformationDetail: The intelligence_information object containing all its details.

#     Raises:

#         HTTPException(403 Forbidden): If the current user does not have permission.
#         HTTPException(404 Not Found): If the requested intelligence_information does not exist.
#     """
#     intelligence_information_record: IntelligenceInformationModel = await intelligence_information_service.get_intelligence_information(id=id)
#     return IntelligenceInformationDetail(**intelligence_information_record.model_dump())


# @intelligence_information_router.get("/intelligenceInformation")
# async def list_intelligence_information(
#     req: Annotated[ListIntelligenceInformationRequest, Query()],
# ) -> ListResponse[IntelligenceInformation]:
#     """
#     List intelligence_information with pagination.

#     Args:

#         req: Request object containing pagination, filter and sort parameters.

#     Returns:

#         ListResponse: Paginated list of intelligence_information and total count.

#     Raises:

#         HTTPException(403 Forbidden): If user don't have access rights.
#     """
#     intelligence_information_records, total = await intelligence_information_service.list_intelligence_information(req=req)
#     return ListResponse(records=intelligence_information_records, total=total)


# @intelligence_information_router.post("/intelligenceInformation")
# async def creat_intelligence_information(
#     req: CreateIntelligenceInformationRequest,
# ) -> IntelligenceInformation:
#     """
#     Create a new intelligence_information.

#     Args:

#         req: Request object containing intelligence_information creation data.

#     Returns:

#          IntelligenceInformation: The intelligence_information object.

#     Raises:

#         HTTPException(403 Forbidden): If the current user don't have access rights.
#         HTTPException(409 Conflict): If the creation data already exists.
#     """
#     intelligence_information: IntelligenceInformationModel = await intelligence_information_service.create_intelligence_information(req=req)
#     return IntelligenceInformation(**intelligence_information.model_dump())


# @intelligence_information_router.put("/intelligenceInformation")
# async def update_intelligence_information(
#     req: UpdateIntelligenceInformationRequest,
# ) -> IntelligenceInformation:
#     """
#     Update an existing intelligence_information.

#     Args:

#         req: Request object containing intelligence_information update data.

#     Returns:

#         IntelligenceInformation: The updated intelligence_information object.

#     Raises:

#         HTTPException(403 Forbidden): If the current user doesn't have update permissions.
#         HTTPException(404 Not Found): If the intelligence_information to update doesn't exist.
#     """
#     intelligence_information: IntelligenceInformationModel = await intelligence_information_service.update_intelligence_information(req=req)
#     return IntelligenceInformation(**intelligence_information.model_dump())


# @intelligence_information_router.delete("/intelligenceInformation/{id}")
# async def delete_intelligence_information(
#     id: int,
# ) -> None:
#     """
#     Delete intelligence_information by ID.

#     Args:

#         id: The ID of the intelligence_information to delete.

#     Raises:

#         HTTPException(403 Forbidden): If the current user doesn't have access permissions.
#         HTTPException(404 Not Found): If the intelligence_information with given ID doesn't exist.
#     """
#     await intelligence_information_service.delete_intelligence_information(id=id)


# @intelligence_information_router.get("/intelligenceInformation:batchGet")
# async def batch_get_intelligence_information(
#     ids: list[int] = Query(..., description="List of intelligence_information IDs to retrieve"),
# ) -> BatchGetIntelligenceInformationResponse:
#     """
#     Retrieves multiple intelligence_information by their IDs.

#     Args:

#         ids (list[int]): A list of intelligence_information resource IDs.

#     Returns:

#         list[IntelligenceInformationDetail]: A list of intelligence_information objects matching the provided IDs.

#     Raises:

#         HTTPException(403 Forbidden): If the current user does not have access rights.
#         HTTPException(404 Not Found): If one of the requested intelligence_information does not exist.
#     """
#     intelligence_information_records: list[IntelligenceInformationModel] = await intelligence_information_service.batch_get_intelligence_information(ids)
#     intelligence_information_detail_list: list[IntelligenceInformationDetail] = [
#         IntelligenceInformationDetail(**intelligence_information_record.model_dump()) for intelligence_information_record in intelligence_information_records
#     ]
#     return BatchGetIntelligenceInformationResponse(intelligence_information=intelligence_information_detail_list)


# @intelligence_information_router.post("/intelligenceInformation:batchCreate")
# async def batch_create_intelligence_information(
#     req: BatchCreateIntelligenceInformationRequest,
# ) -> BatchCreateIntelligenceInformationResponse:
#     """
#     Batch create intelligence_information.

#     Args:

#         req (BatchCreateIntelligenceInformationRequest): Request body containing a list of intelligence_information creation items.

#     Returns:

#         BatchCreateIntelligenceInformationResponse: Response containing the list of created intelligence_information.

#     Raises:

#         HTTPException(403 Forbidden): If the current user lacks access rights.
#         HTTPException(409 Conflict): If any intelligence_information creation data already exists.
#     """

#     intelligence_information_records = await intelligence_information_service.batch_create_intelligence_information(req=req)
#     intelligence_information_list: list[IntelligenceInformation] = [
#         IntelligenceInformation(**intelligence_information_record.model_dump()) for intelligence_information_record in intelligence_information_records
#     ]
#     return BatchCreateIntelligenceInformationResponse(intelligence_information=intelligence_information_list)


# @intelligence_information_router.post("/intelligenceInformation:batchUpdate")
# async def batch_update_intelligence_information(
#     req: BatchUpdateIntelligenceInformationRequest,
# ) -> BatchUpdateIntelligenceInformationResponse:
#     """
#     Batch update multiple intelligence_information with the same changes.

#     Args:

#         req (BatchUpdateIntelligenceInformationRequest): The batch update request data with ids.

#     Returns:

#         BatchUpdateBooksResponse: Contains the list of updated intelligence_information.

#     Raises:

#         HTTPException 403 (Forbidden): If user lacks permission to modify intelligence_information
#         HTTPException 404 (Not Found): If any specified intelligence_information ID doesn't exist
#     """
#     intelligence_information_records: list[IntelligenceInformationModel] = await intelligence_information_service.batch_update_intelligence_information(req=req)
#     intelligence_information_list: list[IntelligenceInformation] = [IntelligenceInformation(**intelligence_information.model_dump()) for intelligence_information in intelligence_information_records]
#     return BatchUpdateIntelligenceInformationResponse(intelligence_information=intelligence_information_list)


# @intelligence_information_router.post("/intelligenceInformation:batchPatch")
# async def batch_patch_intelligence_information(
#     req: BatchPatchIntelligenceInformationRequest,
# ) -> BatchUpdateIntelligenceInformationResponse:
#     """
#     Batch update multiple intelligence_information with individual changes.

#     Args:

#         req (BatchPatchIntelligenceInformationRequest): The batch patch request data.

#     Returns:

#         BatchUpdateBooksResponse: Contains the list of updated intelligence_information.

#     Raises:

#         HTTPException 403 (Forbidden): If user lacks permission to modify intelligence_information
#         HTTPException 404 (Not Found): If any specified intelligence_information ID doesn't exist
#     """
#     intelligence_information_records: list[IntelligenceInformationModel] = await intelligence_information_service.batch_patch_intelligence_information(req=req)
#     intelligence_information_list: list[IntelligenceInformation] = [IntelligenceInformation(**intelligence_information.model_dump()) for intelligence_information in intelligence_information_records]
#     return BatchUpdateIntelligenceInformationResponse(intelligence_information=intelligence_information_list)


# @intelligence_information_router.post("/intelligenceInformation:batchDelete")
# async def batch_delete_intelligence_information(
#     req: BatchDeleteIntelligenceInformationRequest,
# ) -> None:
#     """
#     Batch delete intelligence_information.

#     Args:
#         req (BatchDeleteIntelligenceInformationRequest): Request object containing delete info.

#     Raises:
#         HTTPException(404 Not Found): If any of the intelligence_information do not exist.
#         HTTPException(403 Forbidden): If user don't have access rights.
#     """
#     await intelligence_information_service.batch_delete_intelligence_information(req=req)


# @intelligence_information_router.get("/intelligenceInformation:exportTemplate")
# async def export_intelligence_information_template() -> StreamingResponse:
#     """
#     Export the Excel template for intelligence_information import.

#     Returns:
#         StreamingResponse: An Excel file stream containing the import template.

#     Raises:
#         HTTPException(403 Forbidden): If user don't have access rights.
#     """

#     return await intelligence_information_service.export_intelligence_information_template()


# @intelligence_information_router.get("/intelligenceInformation:export")
# async def export_intelligence_information(
#     req: ExportIntelligenceInformationRequest = Query(...),
# ) -> StreamingResponse:
#     """
#     Export intelligence_information data based on the provided intelligence_information IDs.

#     Args:
#         req (ExportIntelligenceInformationRequest): Query parameters specifying the intelligence_information to export.

#     Returns:
#         StreamingResponse: A streaming response containing the generated Excel file.

#     Raises:
#         HTTPException(403 Forbidden): If the current user lacks access rights.
#         HTTPException(404 Not Found ): If no matching intelligence_information are found.
#     """
#     return await intelligence_information_service.export_intelligence_information(
#         req=req,
#     )

# @intelligence_information_router.post("/intelligenceInformation:import")
# async def import_intelligence_information(
#     req: ImportIntelligenceInformationRequest = Form(...),
# ) -> ImportIntelligenceInformationResponse:
#     """
#     Import intelligence_information from an uploaded Excel file.

#     Args:
#         req (UploadFile): The Excel file containing intelligence_information data to import.

#     Returns:
#         ImportIntelligenceInformationResponse: List of successfully parsed intelligence_information data.

#     Raises:
#         HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
#         HTTPException(403 Forbidden): If the current user lacks access rights.
#     """

#     import_intelligence_information_resp: list[ImportIntelligenceInformation] = await intelligence_information_service.import_intelligence_information(
#         req=req
#     )
#     return ImportIntelligenceInformationResponse(intelligence_information=import_intelligence_information_resp)