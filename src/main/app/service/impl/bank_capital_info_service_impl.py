# SPDX-License-Identifier: MIT
"""BankCapitalInfo domain service impl"""

from __future__ import annotations

import io
import json
from typing import Type, Any

import pandas as pd
from loguru import logger
from pydantic import ValidationError
from starlette.responses import StreamingResponse

from fastlib.constants import FilterOperators
from fastlib.service.impl.base_service_impl import BaseServiceImpl
from fastlib.utils import excel_util
from fastlib.utils.validate_util import ValidateService
from src.main.app.exception.biz_exception import BusinessErrorCode
from src.main.app.exception.biz_exception import BusinessException
from src.main.app.mapper.bank_capital_info_mapper import BankCapitalInfoMapper
from src.main.app.model.bank_capital_info_model import BankCapitalInfoModel
from src.main.app.schema.bank_capital_info_schema import (
    ListBankCapitalInfosRequest,
    BankCapitalInfo,
    CreateBankCapitalInfoRequest,
    UpdateBankCapitalInfoRequest,
    BatchDeleteBankCapitalInfosRequest,
    ExportBankCapitalInfosRequest,
    BatchCreateBankCapitalInfosRequest,
    CreateBankCapitalInfo,
    BatchUpdateBankCapitalInfosRequest,
    UpdateBankCapitalInfo,
    ImportBankCapitalInfosRequest,
    ImportBankCapitalInfo,
    ExportBankCapitalInfo,
    BatchPatchBankCapitalInfosRequest,
    BatchUpdateBankCapitalInfo,
)
from src.main.app.service.bank_capital_info_service import BankCapitalInfoService


class BankCapitalInfoServiceImpl(BaseServiceImpl[BankCapitalInfoMapper, BankCapitalInfoModel], BankCapitalInfoService):
    """
    Implementation of the BankCapitalInfoService interface.
    """

    def __init__(self, mapper: BankCapitalInfoMapper):
        """
        Initialize the BankCapitalInfoServiceImpl instance.

        Args:
            mapper (BankCapitalInfoMapper): The BankCapitalInfoMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper, model=BankCapitalInfoModel)
        self.mapper = mapper

    async def get_bank_capital_info(
        self,
        *,
        id: int,
    ) -> BankCapitalInfoModel:
        bank_capital_info_record: BankCapitalInfoModel = await self.mapper.select_by_id(id=id)
        if bank_capital_info_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return bank_capital_info_record

    async def list_bank_capital_infos(
        self, req: ListBankCapitalInfosRequest
    ) -> tuple[list[BankCapitalInfoModel], int]:
        filters = {
            FilterOperators.EQ: {},
            FilterOperators.NE: {},
            FilterOperators.GT: {},
            FilterOperators.GE: {},
            FilterOperators.LT: {},
            FilterOperators.LE: {},
            FilterOperators.BETWEEN: {},
            FilterOperators.LIKE: {},
        }
        if req.id is not None and req.id != "":
            filters[FilterOperators.EQ]["id"] = req.id
        if req.trade_date is not None and req.trade_date != "":
            filters[FilterOperators.EQ]["trade_date"] = req.trade_date
        if req.bank_code is not None and req.bank_code != "":
            filters[FilterOperators.EQ]["bank_code"] = req.bank_code
        if req.bank_name is not None and req.bank_name != "":
            filters[FilterOperators.LIKE]["bank_name"] = req.bank_name
        if req.bank_type is not None and req.bank_type != "":
            filters[FilterOperators.EQ]["bank_type"] = req.bank_type
        if req.total_deposits is not None and req.total_deposits != "":
            filters[FilterOperators.EQ]["total_deposits"] = req.total_deposits
        if req.total_loans is not None and req.total_loans != "":
            filters[FilterOperators.EQ]["total_loans"] = req.total_loans
        if req.non_performing_loan_ratio is not None and req.non_performing_loan_ratio != "":
            filters[FilterOperators.EQ]["non_performing_loan_ratio"] = req.non_performing_loan_ratio
        if req.loan_loss_provision_ratio is not None and req.loan_loss_provision_ratio != "":
            filters[FilterOperators.EQ]["loan_loss_provision_ratio"] = req.loan_loss_provision_ratio
        if req.net_interest_margin is not None and req.net_interest_margin != "":
            filters[FilterOperators.EQ]["net_interest_margin"] = req.net_interest_margin
        if req.capital_adequacy_ratio is not None and req.capital_adequacy_ratio != "":
            filters[FilterOperators.EQ]["capital_adequacy_ratio"] = req.capital_adequacy_ratio
        if req.tier1_capital_ratio is not None and req.tier1_capital_ratio != "":
            filters[FilterOperators.EQ]["tier1_capital_ratio"] = req.tier1_capital_ratio
        if req.core_tier1_ratio is not None and req.core_tier1_ratio != "":
            filters[FilterOperators.EQ]["core_tier1_ratio"] = req.core_tier1_ratio
        if req.data_source is not None and req.data_source != "":
            filters[FilterOperators.EQ]["data_source"] = req.data_source
        if req.data_frequency is not None and req.data_frequency != "":
            filters[FilterOperators.EQ]["data_frequency"] = req.data_frequency
        if req.created_at is not None and req.created_at != "":
            filters[FilterOperators.EQ]["created_at"] = req.created_at
        if req.updated_at is not None and req.updated_at != "":
            filters[FilterOperators.EQ]["updated_at"] = req.updated_at
        sort_list = None
        sort_str = req.sort_str
        if sort_str is not None:
            sort_list = json.loads(sort_str)
        return await self.mapper.select_by_ordered_page(
            current=req.current,
            page_size=req.page_size,
            count=req.count,
            **filters,
            sort_list=sort_list,
        )

    

    async def create_bank_capital_info(self, req: CreateBankCapitalInfoRequest) -> BankCapitalInfoModel:
        bank_capital_info: BankCapitalInfoModel = BankCapitalInfoModel(**req.bank_capital_info.model_dump())
        return await self.save(data=bank_capital_info)

    async def update_bank_capital_info(self, req: UpdateBankCapitalInfoRequest) -> BankCapitalInfoModel:
        bank_capital_info_record: BankCapitalInfoModel = await self.retrieve_by_id(id=req.bank_capital_info.id)
        if bank_capital_info_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        bank_capital_info_model = BankCapitalInfoModel(**req.bank_capital_info.model_dump(exclude_unset=True))
        await self.modify_by_id(data=bank_capital_info_model)
        merged_data = {**bank_capital_info_record.model_dump(), **bank_capital_info_model.model_dump()}
        return BankCapitalInfoModel(**merged_data)

    async def delete_bank_capital_info(self, id: int) -> None:
        bank_capital_info_record: BankCapitalInfoModel = await self.retrieve_by_id(id=id)
        if bank_capital_info_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_bank_capital_infos(self, ids: list[int]) -> list[BankCapitalInfoModel]:
        bank_capital_info_records = list[BankCapitalInfoModel] = await self.retrieve_by_ids(ids=ids)
        if bank_capital_info_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(bank_capital_info_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in bank_capital_info_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(bank_capital_info_records)} != {str(not_exits_ids)}",
            )
        return bank_capital_info_records

    async def batch_create_bank_capital_infos(
        self,
        *,
        req: BatchCreateBankCapitalInfosRequest,
    ) -> list[BankCapitalInfoModel]:
        bank_capital_info_list: list[CreateBankCapitalInfo] = req.bank_capital_infos
        if not bank_capital_info_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [BankCapitalInfoModel(**bank_capital_info.model_dump()) for bank_capital_info in bank_capital_info_list]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_bank_capital_infos(
        self, req: BatchUpdateBankCapitalInfosRequest
    ) -> list[BankCapitalInfoModel]:
        bank_capital_info: BatchUpdateBankCapitalInfo = req.bank_capital_info
        ids: list[int] = req.ids
        if not bank_capital_info or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(
            ids=ids, data=bank_capital_info.model_dump(exclude_none=True)
        )
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_bank_capital_infos(
        self, req: BatchPatchBankCapitalInfosRequest
    ) -> list[BankCapitalInfoModel]:
        bank_capital_infos: list[UpdateBankCapitalInfo] = req.bank_capital_infos
        if not bank_capital_infos:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            bank_capital_info.model_dump(exclude_unset=True) for bank_capital_info in bank_capital_infos
        ]
        await self.mapper.batch_update(items=update_data)
        bank_capital_info_ids: list[int] = [bank_capital_info.id for bank_capital_info in bank_capital_infos]
        return await self.mapper.select_by_ids(ids=bank_capital_info_ids)

    async def batch_delete_bank_capital_infos(self, req: BatchDeleteBankCapitalInfosRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_bank_capital_infos_template(self) -> StreamingResponse:
        file_name = "bank_capital_info_import_tpl"
        return await excel_util.export_excel(
            schema=CreateBankCapitalInfo, file_name=file_name
        )

    async def export_bank_capital_infos(self, req: ExportBankCapitalInfosRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        bank_capital_info_list: list[BankCapitalInfoModel] = await self.mapper.select_by_ids(ids=ids)
        if bank_capital_info_list is None or len(bank_capital_info_list) == 0:
            logger.error(f"No bank_capital_infos found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        bank_capital_info_page_list = [ExportBankCapitalInfo(**bank_capital_info.model_dump()) for bank_capital_info in bank_capital_info_list]
        file_name = "bank_capital_info_data_export"
        return await excel_util.export_excel(
            schema=ExportBankCapitalInfo, file_name=file_name, data_list=bank_capital_info_page_list
        )

    async def import_bank_capital_infos(self, req: ImportBankCapitalInfosRequest) -> list[ImportBankCapitalInfo]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        bank_capital_info_records = import_df.to_dict(orient="records")
        if bank_capital_info_records is None or len(bank_capital_info_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in bank_capital_info_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        bank_capital_info_import_list = []
        for bank_capital_info_record in bank_capital_info_records:
            try:
                bank_capital_info_create = ImportBankCapitalInfo(**bank_capital_info_record)
                bank_capital_info_import_list.append(bank_capital_info_create)
            except ValidationError as e:
                valid_data = {
                    k: v
                    for k, v in bank_capital_info_record.items()
                    if k in ImportBankCapitalInfo.model_fields
                }
                bank_capital_info_create = ImportBankCapitalInfo.model_construct(**valid_data)
                bank_capital_info_create.err_msg = ValidateService.get_validate_err_msg(e)
                bank_capital_info_import_list.append(bank_capital_info_create)
                return bank_capital_info_import_list

        return bank_capital_info_import_list