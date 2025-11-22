# # SPDX-License-Identifier: MIT
# """BankCapitalInfo REST Controller"""
# from __future__ import annotations
# from typing import Annotated

# from fastlib.response import ListResponse
# from fastapi import APIRouter, Query, Form
# from starlette.responses import StreamingResponse

# from src.main.app.mapper.bank_capital_info_mapper import bankCapitalInfoMapper
# from src.main.app.model.bank_capital_info_model import BankCapitalInfoModel
# from src.main.app.schema.bank_capital_info_schema import (
#     ListBankCapitalInfosRequest,
#     BankCapitalInfo,
#     CreateBankCapitalInfoRequest,
#     BankCapitalInfoDetail,
#     UpdateBankCapitalInfoRequest,
#     BatchDeleteBankCapitalInfosRequest,
#     BatchUpdateBankCapitalInfosRequest,
#     BatchUpdateBankCapitalInfosResponse,
#     BatchCreateBankCapitalInfosRequest,
#     BatchCreateBankCapitalInfosResponse,
#     ExportBankCapitalInfosRequest,
#     ImportBankCapitalInfosResponse,
#     BatchGetBankCapitalInfosResponse,
#     ImportBankCapitalInfosRequest,
#     ImportBankCapitalInfo, BatchPatchBankCapitalInfosRequest,
# )
# from src.main.app.service.impl.bank_capital_info_service_impl import BankCapitalInfoServiceImpl
# from src.main.app.service.bank_capital_info_service import BankCapitalInfoService

# bank_capital_info_router = APIRouter()
# bank_capital_info_service: BankCapitalInfoService = BankCapitalInfoServiceImpl(mapper=bankCapitalInfoMapper)


# @bank_capital_info_router.get("/bankCapitalInfos/{id}")
# async def get_bank_capital_info(id: int) -> BankCapitalInfoDetail:
#     """
#     Retrieve bank_capital_info details.

#     Args:

#         id: Unique ID of the bank_capital_info resource.

#     Returns:

#         BankCapitalInfoDetail: The bank_capital_info object containing all its details.

#     Raises:

#         HTTPException(403 Forbidden): If the current user does not have permission.
#         HTTPException(404 Not Found): If the requested bank_capital_info does not exist.
#     """
#     bank_capital_info_record: BankCapitalInfoModel = await bank_capital_info_service.get_bank_capital_info(id=id)
#     return BankCapitalInfoDetail(**bank_capital_info_record.model_dump())


# @bank_capital_info_router.get("/bankCapitalInfos")
# async def list_bank_capital_infos(
#     req: Annotated[ListBankCapitalInfosRequest, Query()],
# ) -> ListResponse[BankCapitalInfo]:
#     """
#     List bank_capital_infos with pagination.

#     Args:

#         req: Request object containing pagination, filter and sort parameters.

#     Returns:

#         ListResponse: Paginated list of bank_capital_infos and total count.

#     Raises:

#         HTTPException(403 Forbidden): If user don't have access rights.
#     """
#     bank_capital_info_records, total = await bank_capital_info_service.list_bank_capital_infos(req=req)
#     return ListResponse(records=bank_capital_info_records, total=total)


# @bank_capital_info_router.post("/bankCapitalInfos")
# async def creat_bank_capital_info(
#     req: CreateBankCapitalInfoRequest,
# ) -> BankCapitalInfo:
#     """
#     Create a new bank_capital_info.

#     Args:

#         req: Request object containing bank_capital_info creation data.

#     Returns:

#          BankCapitalInfo: The bank_capital_info object.

#     Raises:

#         HTTPException(403 Forbidden): If the current user don't have access rights.
#         HTTPException(409 Conflict): If the creation data already exists.
#     """
#     bank_capital_info: BankCapitalInfoModel = await bank_capital_info_service.create_bank_capital_info(req=req)
#     return BankCapitalInfo(**bank_capital_info.model_dump())


# @bank_capital_info_router.put("/bankCapitalInfos")
# async def update_bank_capital_info(
#     req: UpdateBankCapitalInfoRequest,
# ) -> BankCapitalInfo:
#     """
#     Update an existing bank_capital_info.

#     Args:

#         req: Request object containing bank_capital_info update data.

#     Returns:

#         BankCapitalInfo: The updated bank_capital_info object.

#     Raises:

#         HTTPException(403 Forbidden): If the current user doesn't have update permissions.
#         HTTPException(404 Not Found): If the bank_capital_info to update doesn't exist.
#     """
#     bank_capital_info: BankCapitalInfoModel = await bank_capital_info_service.update_bank_capital_info(req=req)
#     return BankCapitalInfo(**bank_capital_info.model_dump())


# @bank_capital_info_router.delete("/bankCapitalInfos/{id}")
# async def delete_bank_capital_info(
#     id: int,
# ) -> None:
#     """
#     Delete bank_capital_info by ID.

#     Args:

#         id: The ID of the bank_capital_info to delete.

#     Raises:

#         HTTPException(403 Forbidden): If the current user doesn't have access permissions.
#         HTTPException(404 Not Found): If the bank_capital_info with given ID doesn't exist.
#     """
#     await bank_capital_info_service.delete_bank_capital_info(id=id)


# @bank_capital_info_router.get("/bankCapitalInfos:batchGet")
# async def batch_get_bank_capital_infos(
#     ids: list[int] = Query(..., description="List of bank_capital_info IDs to retrieve"),
# ) -> BatchGetBankCapitalInfosResponse:
#     """
#     Retrieves multiple bank_capital_infos by their IDs.

#     Args:

#         ids (list[int]): A list of bank_capital_info resource IDs.

#     Returns:

#         list[BankCapitalInfoDetail]: A list of bank_capital_info objects matching the provided IDs.

#     Raises:

#         HTTPException(403 Forbidden): If the current user does not have access rights.
#         HTTPException(404 Not Found): If one of the requested bank_capital_infos does not exist.
#     """
#     bank_capital_info_records: list[BankCapitalInfoModel] = await bank_capital_info_service.batch_get_bank_capital_infos(ids)
#     bank_capital_info_detail_list: list[BankCapitalInfoDetail] = [
#         BankCapitalInfoDetail(**bank_capital_info_record.model_dump()) for bank_capital_info_record in bank_capital_info_records
#     ]
#     return BatchGetBankCapitalInfosResponse(bank_capital_infos=bank_capital_info_detail_list)


# @bank_capital_info_router.post("/bankCapitalInfos:batchCreate")
# async def batch_create_bank_capital_infos(
#     req: BatchCreateBankCapitalInfosRequest,
# ) -> BatchCreateBankCapitalInfosResponse:
#     """
#     Batch create bank_capital_infos.

#     Args:

#         req (BatchCreateBankCapitalInfosRequest): Request body containing a list of bank_capital_info creation items.

#     Returns:

#         BatchCreateBankCapitalInfosResponse: Response containing the list of created bank_capital_infos.

#     Raises:

#         HTTPException(403 Forbidden): If the current user lacks access rights.
#         HTTPException(409 Conflict): If any bank_capital_info creation data already exists.
#     """

#     bank_capital_info_records = await bank_capital_info_service.batch_create_bank_capital_infos(req=req)
#     bank_capital_info_list: list[BankCapitalInfo] = [
#         BankCapitalInfo(**bank_capital_info_record.model_dump()) for bank_capital_info_record in bank_capital_info_records
#     ]
#     return BatchCreateBankCapitalInfosResponse(bank_capital_infos=bank_capital_info_list)


# @bank_capital_info_router.post("/bankCapitalInfos:batchUpdate")
# async def batch_update_bank_capital_infos(
#     req: BatchUpdateBankCapitalInfosRequest,
# ) -> BatchUpdateBankCapitalInfosResponse:
#     """
#     Batch update multiple bank_capital_infos with the same changes.

#     Args:

#         req (BatchUpdateBankCapitalInfosRequest): The batch update request data with ids.

#     Returns:

#         BatchUpdateBooksResponse: Contains the list of updated bank_capital_infos.

#     Raises:

#         HTTPException 403 (Forbidden): If user lacks permission to modify bank_capital_infos
#         HTTPException 404 (Not Found): If any specified bank_capital_info ID doesn't exist
#     """
#     bank_capital_info_records: list[BankCapitalInfoModel] = await bank_capital_info_service.batch_update_bank_capital_infos(req=req)
#     bank_capital_info_list: list[BankCapitalInfo] = [BankCapitalInfo(**bank_capital_info.model_dump()) for bank_capital_info in bank_capital_info_records]
#     return BatchUpdateBankCapitalInfosResponse(bank_capital_infos=bank_capital_info_list)


# @bank_capital_info_router.post("/bankCapitalInfos:batchPatch")
# async def batch_patch_bank_capital_infos(
#     req: BatchPatchBankCapitalInfosRequest,
# ) -> BatchUpdateBankCapitalInfosResponse:
#     """
#     Batch update multiple bank_capital_infos with individual changes.

#     Args:

#         req (BatchPatchBankCapitalInfosRequest): The batch patch request data.

#     Returns:

#         BatchUpdateBooksResponse: Contains the list of updated bank_capital_infos.

#     Raises:

#         HTTPException 403 (Forbidden): If user lacks permission to modify bank_capital_infos
#         HTTPException 404 (Not Found): If any specified bank_capital_info ID doesn't exist
#     """
#     bank_capital_info_records: list[BankCapitalInfoModel] = await bank_capital_info_service.batch_patch_bank_capital_infos(req=req)
#     bank_capital_info_list: list[BankCapitalInfo] = [BankCapitalInfo(**bank_capital_info.model_dump()) for bank_capital_info in bank_capital_info_records]
#     return BatchUpdateBankCapitalInfosResponse(bank_capital_infos=bank_capital_info_list)


# @bank_capital_info_router.post("/bankCapitalInfos:batchDelete")
# async def batch_delete_bank_capital_infos(
#     req: BatchDeleteBankCapitalInfosRequest,
# ) -> None:
#     """
#     Batch delete bank_capital_infos.

#     Args:
#         req (BatchDeleteBankCapitalInfosRequest): Request object containing delete info.

#     Raises:
#         HTTPException(404 Not Found): If any of the bank_capital_infos do not exist.
#         HTTPException(403 Forbidden): If user don't have access rights.
#     """
#     await bank_capital_info_service.batch_delete_bank_capital_infos(req=req)


# @bank_capital_info_router.get("/bankCapitalInfos:exportTemplate")
# async def export_bank_capital_infos_template() -> StreamingResponse:
#     """
#     Export the Excel template for bank_capital_info import.

#     Returns:
#         StreamingResponse: An Excel file stream containing the import template.

#     Raises:
#         HTTPException(403 Forbidden): If user don't have access rights.
#     """

#     return await bank_capital_info_service.export_bank_capital_infos_template()


# @bank_capital_info_router.get("/bankCapitalInfos:export")
# async def export_bank_capital_infos(
#     req: ExportBankCapitalInfosRequest = Query(...),
# ) -> StreamingResponse:
#     """
#     Export bank_capital_info data based on the provided bank_capital_info IDs.

#     Args:
#         req (ExportBankCapitalInfosRequest): Query parameters specifying the bank_capital_infos to export.

#     Returns:
#         StreamingResponse: A streaming response containing the generated Excel file.

#     Raises:
#         HTTPException(403 Forbidden): If the current user lacks access rights.
#         HTTPException(404 Not Found ): If no matching bank_capital_infos are found.
#     """
#     return await bank_capital_info_service.export_bank_capital_infos(
#         req=req,
#     )

# @bank_capital_info_router.post("/bankCapitalInfos:import")
# async def import_bank_capital_infos(
#     req: ImportBankCapitalInfosRequest = Form(...),
# ) -> ImportBankCapitalInfosResponse:
#     """
#     Import bank_capital_infos from an uploaded Excel file.

#     Args:
#         req (UploadFile): The Excel file containing bank_capital_info data to import.

#     Returns:
#         ImportBankCapitalInfosResponse: List of successfully parsed bank_capital_info data.

#     Raises:
#         HTTPException(400 Bad Request): If the uploaded file is invalid or cannot be parsed.
#         HTTPException(403 Forbidden): If the current user lacks access rights.
#     """

#     import_bank_capital_infos_resp: list[ImportBankCapitalInfo] = await bank_capital_info_service.import_bank_capital_infos(
#         req=req
#     )
#     return ImportBankCapitalInfosResponse(bank_capital_infos=import_bank_capital_infos_resp)