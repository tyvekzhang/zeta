# SPDX-License-Identifier: MIT
"""Stock domain service impl"""

from __future__ import annotations

from datetime import datetime
import io
import json
import random
import time
from typing import Any
import akshare as ak

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
from src.main.app.mapper.stock_mapper import StockMapper
from src.main.app.model.stock_model import StockModel
from src.main.app.schema.stock_schema import (
    ListStocksRequest,
    CreateStockRequest,
    UpdateStockRequest,
    BatchDeleteStocksRequest,
    ExportStocksRequest,
    BatchCreateStocksRequest,
    CreateStock,
    BatchUpdateStocksRequest,
    UpdateStock,
    ImportStocksRequest,
    ImportStock,
    ExportStock,
    BatchPatchStocksRequest,
    BatchUpdateStock,
)
from src.main.app.service.stock_service import StockService


class StockServiceImpl(BaseServiceImpl[StockMapper, StockModel], StockService):
    """
    Implementation of the StockService interface.
    """

    def __init__(self, mapper: StockMapper):
        """
        Initialize the StockServiceImpl instance.

        Args:
            mapper (StockMapper): The StockMapper instance to use for database operations.
        """
        super().__init__(mapper=mapper, model=StockModel)
        self.mapper = mapper

    async def get_existing_stocks(self) -> set:
        """
        获取数据库中已存在的股票代码集合
        """
        try:
            existing_records = await self.mapper.select_all_stocks()
            return {record["stock_code"] for record in existing_records}
        except Exception as e:
            logger.error(f"获取已存在股票代码失败: {e}")
            return set()

    def get_complete_stock_info(self, existing_stocks: set) -> list[dict]:
        """
        获取完整的股票基本信息（同步版本，带防反爬和重试）

        Args:
            existing_stocks: 数据库中已存在的股票代码集合
        """
        all_stocks = []

        # 获取所有A股代码
        try:
            stock_list = ak.stock_info_a_code_name()
        except Exception as e:
            logger.error(f"获取股票列表失败: {e}")
            return all_stocks

        total = len(stock_list)
        logger.info(f"共 {total} 只股票，开始获取详细信息...")

        processed_count = 0
        skipped_count = 0

        for index, row in stock_list.iterrows():
            code = row["code"]
            name = row["name"]

            # 检查是否已存在于数据库
            if code in existing_stocks:
                logger.info(f"[{index+1}/{total}] 跳过已存在数据: {code} - {name}")
                skipped_count += 1
                continue

            logger.info(f"[{index+1}/{total}] 正在处理: {code} - {name}")

            try:
                # 更完整的交易所判断逻辑
                if code.startswith("6"):
                    exchange = "SH"
                    market_type = "沪市A股"
                elif code.startswith("0"):
                    exchange = "SZ"
                    market_type = "深市主板"
                elif code.startswith("3"):
                    exchange = "SZ"
                    market_type = "创业板"
                elif code.startswith("4") or code.startswith("8"):
                    exchange = "BJ"
                    market_type = "北交所"
                elif code.startswith("9"):
                    exchange = "SH"
                    market_type = "沪市B股"
                elif code.startswith("200"):
                    exchange = "SZ"
                    market_type = "深市B股"
                else:
                    exchange = "UNKNOWN"
                    market_type = "未知"

                # 初始化股票数据字典
                stock_data = {
                    "stock_code": code,
                    "stock_name": name or "未知名称",
                    "exchange": exchange,
                    "market_type": market_type,
                    # 设置默认值
                    "listing_date": None,
                    "industry": None,
                    "province": None,
                    "city": None,
                    "company_name": None,
                    "english_name": None,
                    "former_name": None,
                    "legal_representative": None,
                    "registered_capital": None,
                    "establish_date": None,
                    "website": None,
                    "email": None,
                    "telephone": None,
                    "fax": None,
                    "registered_address": None,
                    "business_address": None,
                    "postal_code": None,
                    "main_business": None,
                    "business_scope": None,
                    "company_profile": None,
                    "data_source": "akshare",
                }

                # 获取详细信息
                profile_df = None
                for retry in range(3):
                    try:
                        profile_df = ak.stock_profile_cninfo(symbol=code)
                        break
                    except Exception as e:
                        logger.warning(
                            f"  第 {retry+1} 次尝试获取 {code} 的 cninfo 数据失败: {e}"
                        )
                        time.sleep(random.uniform(1, 2))

                if profile_df is not None and not profile_df.empty:
                    # 直接映射字段
                    stock_data["listing_date"] = self._parse_date(
                        profile_df.get("上市日期", [None])[0]
                    )
                    stock_data["industry"] = profile_df.get("所属行业", [None])[0]
                    stock_data["website"] = profile_df.get("官方网站", [None])[0]

                    # 公司名称
                    stock_data["company_name"] = profile_df.get("公司名称", [None])[0]

                    # 英文名称
                    stock_data["english_name"] = profile_df.get("英文名称", [None])[0]

                    # 曾用简称
                    former_names = profile_df.get("曾用简称", [None])[0]
                    if former_names:
                        stock_data["former_name"] = former_names

                    # 法人代表
                    stock_data["legal_representative"] = profile_df.get(
                        "法人代表", [None]
                    )[0]

                    # 注册资金处理
                    registered_capital = profile_df.get("注册资金", [None])[0]
                    stock_data["registered_capital"] = str(registered_capital)

                    # 成立日期
                    stock_data["establish_date"] = self._parse_date(
                        profile_df.get("成立日期", [None])[0]
                    )

                    # 联系方式信息
                    stock_data["email"] = profile_df.get("电子邮箱", [None])[0]
                    stock_data["telephone"] = profile_df.get("联系电话", [None])[0]
                    stock_data["fax"] = profile_df.get("传真", [None])[0]

                    # 地址信息
                    registered_address = profile_df.get("注册地址", [None])[0]
                    stock_data["registered_address"] = registered_address
                    stock_data["business_address"] = profile_df.get("办公地址", [None])[
                        0
                    ]
                    stock_data["postal_code"] = profile_df.get("邮政编码", [None])[0]

                    # 根据注册地址解析省份和城市
                    if registered_address:
                        province, city = self._parse_province_city(registered_address)
                        stock_data["province"] = province
                        stock_data["city"] = city

                    # 业务信息
                    stock_data["main_business"] = profile_df.get("主营业务", [None])[0]
                    stock_data["business_scope"] = profile_df.get("经营范围", [None])[0]
                    stock_data["company_profile"] = profile_df.get("机构简介", [None])[
                        0
                    ]

                all_stocks.append(stock_data)
                processed_count += 1

            except Exception as e:
                logger.error(f"处理 {code} 时发生未预期错误: {e}")
                continue

            # ⚠️ 关键：每次请求后随机延迟，防止被封
            time.sleep(random.uniform(0.2, 1))

        logger.info(
            f"数据处理完成: 共处理 {processed_count} 条新数据，跳过 {skipped_count} 条已存在数据"
        )
        return all_stocks

    def _parse_date(self, date_str):
        """
        解析日期字符串，返回date对象
        """
        if not date_str:
            return None

        try:
            # 尝试多种日期格式
            if isinstance(date_str, str):
                # 移除可能的空格和特殊字符
                date_str = date_str.strip()

                # 尝试常见日期格式
                for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"]:
                    try:
                        return datetime.strptime(date_str, fmt).date()
                    except ValueError:
                        continue

            return None
        except Exception:
            return None

    def _parse_province_city(self, address):
        """
        从地址字符串中解析省份和城市
        """
        if not address or not isinstance(address, str):
            return None, None

        # 中国所有省份、直辖市、自治区
        provinces = [
            "北京市",
            "天津市",
            "上海市",
            "重庆市",
            "河北省",
            "山西省",
            "辽宁省",
            "吉林省",
            "黑龙江省",
            "江苏省",
            "浙江省",
            "安徽省",
            "福建省",
            "江西省",
            "山东省",
            "河南省",
            "湖北省",
            "湖南省",
            "广东省",
            "海南省",
            "四川省",
            "贵州省",
            "云南省",
            "陕西省",
            "甘肃省",
            "青海省",
            "台湾省",
            "内蒙古自治区",
            "广西壮族自治区",
            "西藏自治区",
            "宁夏回族自治区",
            "新疆维吾尔自治区",
            "香港特别行政区",
            "澳门特别行政区",
        ]

        # 特殊处理直辖市
        direct_cities = {
            "北京市": ("北京市", None),
            "天津市": ("天津市", None),
            "上海市": ("上海市", None),
            "重庆市": ("重庆市", None),
        }

        address = address.strip()

        # 首先检查是否为直辖市
        for city, location in direct_cities.items():
            if address.startswith(city):
                return location

        # 查找省份
        found_province = None
        found_city = None

        for province in provinces:
            if province in address:
                found_province = province
                # 提取省份后的内容作为城市判断依据
                province_index = address.find(province)
                remaining_address = address[province_index + len(province) :]

                # 简单的城市提取逻辑：取省份后的2-4个字符作为城市
                if remaining_address:
                    # 移除可能的空格和标点
                    remaining_address = remaining_address.strip(" ,，.。")

                    # 常见城市后缀
                    city_suffixes = ["市", "地区", "州", "盟"]

                    # 尝试提取城市名（通常是2-3个字符）
                    for i in range(2, min(5, len(remaining_address) + 1)):
                        potential_city = remaining_address[:i]
                        if any(
                            potential_city.endswith(suffix) for suffix in city_suffixes
                        ):
                            found_city = potential_city
                            break

                    # 如果没有找到明确的城市后缀，取前2-3个字符作为城市
                    if not found_city and len(remaining_address) >= 2:
                        found_city = remaining_address[:3]  # 取前3个字符

                break

        # 如果没有找到省份，尝试其他匹配方式
        if not found_province:
            # 检查是否包含"省"字
            if "省" in address:
                parts = address.split("省", 1)
                if len(parts) > 1:
                    found_province = parts[0] + "省"
                    remaining = parts[1].strip()
                    # 从剩余部分提取城市
                    if "市" in remaining:
                        city_parts = remaining.split("市", 1)
                        found_city = city_parts[0] + "市"

        return found_province, found_city

    async def sync_manually(
        self,
    ) -> None:
        # 获取数据库中已存在的股票代码
        existing_stocks = await self.get_existing_stocks()
        logger.info(f"数据库中已存在 {len(existing_stocks)} 只股票数据")

        # 获取需要处理的新数据
        all_stocks = self.get_complete_stock_info(existing_stocks)

        if not all_stocks:
            logger.info("没有需要处理的新数据")
            return

        data = [StockModel(**item) for item in all_stocks]

        # 每100条入库一次
        batch_size = 100
        total_batches = (len(data) + batch_size - 1) // batch_size

        for i in range(0, len(data), batch_size):
            batch = data[i : i + batch_size]
            batch_num = (i // batch_size) + 1
            logger.info(
                f"正在入库第 {batch_num}/{total_batches} 批数据，本批 {len(batch)} 条"
            )

            try:
                await self.mapper.batch_insert(data_list=batch)
                logger.info(f"第 {batch_num} 批数据入库成功")
            except Exception as e:
                logger.error(f"第 {batch_num} 批数据入库失败: {e}")
                # 可以选择继续处理下一批或者抛出异常
                continue

        logger.info(f"数据同步完成，共处理 {len(data)} 条新数据")

    async def get_stock(
        self,
        *,
        id: int,
    ) -> StockModel:
        stock_record: StockModel = await self.mapper.select_by_id(id=id)
        if stock_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        return stock_record

    async def list_stocks(self, req: ListStocksRequest) -> tuple[list[StockModel], int]:
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
        if req.stock_code is not None and req.stock_code != "":
            filters[FilterOperators.EQ]["stock_code"] = req.stock_code
        if req.stock_name is not None and req.stock_name != "":
            filters[FilterOperators.LIKE]["stock_name"] = req.stock_name
        if req.exchange is not None and req.exchange != "":
            filters[FilterOperators.EQ]["exchange"] = req.exchange
        if req.listing_date is not None and req.listing_date != "":
            filters[FilterOperators.EQ]["listing_date"] = req.listing_date
        if req.industry is not None and req.industry != "":
            filters[FilterOperators.EQ]["industry"] = req.industry
        if req.province is not None and req.province != "":
            filters[FilterOperators.EQ]["province"] = req.province
        if req.city is not None and req.city != "":
            filters[FilterOperators.EQ]["city"] = req.city
        if req.company_name is not None and req.company_name != "":
            filters[FilterOperators.LIKE]["company_name"] = req.company_name
        if req.english_name is not None and req.english_name != "":
            filters[FilterOperators.LIKE]["english_name"] = req.english_name
        if req.former_name is not None and req.former_name != "":
            filters[FilterOperators.LIKE]["former_name"] = req.former_name
        if req.market_type is not None and req.market_type != "":
            filters[FilterOperators.EQ]["market_type"] = req.market_type
        if req.legal_representative is not None and req.legal_representative != "":
            filters[FilterOperators.EQ][
                "legal_representative"
            ] = req.legal_representative
        if req.registered_capital is not None and req.registered_capital != "":
            filters[FilterOperators.EQ]["registered_capital"] = req.registered_capital
        if req.establish_date is not None and req.establish_date != "":
            filters[FilterOperators.EQ]["establish_date"] = req.establish_date
        if req.website is not None and req.website != "":
            filters[FilterOperators.EQ]["website"] = req.website
        if req.email is not None and req.email != "":
            filters[FilterOperators.EQ]["email"] = req.email
        if req.telephone is not None and req.telephone != "":
            filters[FilterOperators.EQ]["telephone"] = req.telephone
        if req.fax is not None and req.fax != "":
            filters[FilterOperators.EQ]["fax"] = req.fax
        if req.registered_address is not None and req.registered_address != "":
            filters[FilterOperators.EQ]["registered_address"] = req.registered_address
        if req.business_address is not None and req.business_address != "":
            filters[FilterOperators.EQ]["business_address"] = req.business_address
        if req.postal_code is not None and req.postal_code != "":
            filters[FilterOperators.EQ]["postal_code"] = req.postal_code
        if req.main_business is not None and req.main_business != "":
            filters[FilterOperators.EQ]["main_business"] = req.main_business
        if req.business_scope is not None and req.business_scope != "":
            filters[FilterOperators.EQ]["business_scope"] = req.business_scope
        if req.company_profile is not None and req.company_profile != "":
            filters[FilterOperators.EQ]["company_profile"] = req.company_profile
        if req.data_source is not None and req.data_source != "":
            filters[FilterOperators.EQ]["data_source"] = req.data_source
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

    async def create_stock(self, req: CreateStockRequest) -> StockModel:
        stock: StockModel = StockModel(**req.stock.model_dump())
        return await self.save(data=stock)

    async def update_stock(self, req: UpdateStockRequest) -> StockModel:
        stock_record: StockModel = await self.retrieve_by_id(id=req.stock.id)
        if stock_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        stock_model = StockModel(**req.stock.model_dump(exclude_unset=True))
        await self.modify_by_id(data=stock_model)
        merged_data = {**stock_record.model_dump(), **stock_model.model_dump()}
        return StockModel(**merged_data)

    async def delete_stock(self, id: int) -> None:
        stock_record: StockModel = await self.retrieve_by_id(id=id)
        if stock_record is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        await self.mapper.delete_by_id(id=id)

    async def batch_get_stocks(self, ids: list[int]) -> list[StockModel]:
        stock_records = list[StockModel] = await self.retrieve_by_ids(ids=ids)
        if stock_records is None:
            raise BusinessException(BusinessErrorCode.RESOURCE_NOT_FOUND)
        if len(stock_records) != len(ids):
            not_exits_ids = [id for id in ids if id not in stock_records]
            raise BusinessException(
                BusinessErrorCode.RESOURCE_NOT_FOUND,
                f"{BusinessErrorCode.RESOURCE_NOT_FOUND.message}: {str(stock_records)} != {str(not_exits_ids)}",
            )
        return stock_records

    async def batch_create_stocks(
        self,
        *,
        req: BatchCreateStocksRequest,
    ) -> list[StockModel]:
        stock_list: list[CreateStock] = req.stocks
        if not stock_list:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        data_list = [StockModel(**stock.model_dump()) for stock in stock_list]
        await self.mapper.batch_insert(data_list=data_list)
        return data_list

    async def batch_update_stocks(
        self, req: BatchUpdateStocksRequest
    ) -> list[StockModel]:
        stock: BatchUpdateStock = req.stock
        ids: list[int] = req.ids
        if not stock or not ids:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        await self.mapper.batch_update_by_ids(
            ids=ids, data=stock.model_dump(exclude_none=True)
        )
        return await self.mapper.select_by_ids(ids=ids)

    async def batch_patch_stocks(
        self, req: BatchPatchStocksRequest
    ) -> list[StockModel]:
        stocks: list[UpdateStock] = req.stocks
        if not stocks:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        update_data: list[dict[str, Any]] = [
            stock.model_dump(exclude_unset=True) for stock in stocks
        ]
        await self.mapper.batch_update(items=update_data)
        stock_ids: list[int] = [stock.id for stock in stocks]
        return await self.mapper.select_by_ids(ids=stock_ids)

    async def batch_delete_stocks(self, req: BatchDeleteStocksRequest):
        ids: list[int] = req.ids
        await self.mapper.batch_delete_by_ids(ids=ids)

    async def export_stocks_template(self) -> StreamingResponse:
        file_name = "stock_import_tpl"
        return await excel_util.export_excel(schema=CreateStock, file_name=file_name)

    async def export_stocks(self, req: ExportStocksRequest) -> StreamingResponse:
        ids: list[int] = req.ids
        stock_list: list[StockModel] = await self.mapper.select_by_ids(ids=ids)
        if stock_list is None or len(stock_list) == 0:
            logger.error(f"No stocks found with ids {ids}")
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        stock_page_list = [ExportStock(**stock.model_dump()) for stock in stock_list]
        file_name = "stock_data_export"
        return await excel_util.export_excel(
            schema=ExportStock, file_name=file_name, data_list=stock_page_list
        )

    async def import_stocks(self, req: ImportStocksRequest) -> list[ImportStock]:
        file = req.file
        contents = await file.read()
        import_df = pd.read_excel(io.BytesIO(contents))
        import_df = import_df.fillna("")
        stock_records = import_df.to_dict(orient="records")
        if stock_records is None or len(stock_records) == 0:
            raise BusinessException(BusinessErrorCode.PARAMETER_ERROR)
        for record in stock_records:
            for key, value in record.items():
                if value == "":
                    record[key] = None
        stock_import_list = []
        for stock_record in stock_records:
            try:
                stock_create = ImportStock(**stock_record)
                stock_import_list.append(stock_create)
            except ValidationError as e:
                valid_data = {
                    k: v
                    for k, v in stock_record.items()
                    if k in ImportStock.model_fields
                }
                stock_create = ImportStock.model_construct(**valid_data)
                stock_create.err_msg = ValidateService.get_validate_err_msg(e)
                stock_import_list.append(stock_create)
                return stock_import_list

        return stock_import_list
