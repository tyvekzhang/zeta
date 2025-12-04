import os
import re
from playwright.sync_api import Playwright, sync_playwright
from typing import Literal

# 报告类型映射
REPORT_TYPE_MAP = {
    "年报": "年度报告",
    "半年报": "半年度报告",
    "一季报": "第一季度报告",
    "三季报": "第三季度报告",
}


def download_stock_report(
    playwright: Playwright,
    stock_code: str,
    year: int,
    report_type: Literal["年报", "半年报", "一季报", "三季报"],
    download_folder: str = "downloads",
    headless: bool = False,
) -> str | None:
    """
    下载股票定期报告
    
    Args:
        playwright: Playwright 实例
        stock_code: 股票代码，如 "600519"
        year: 年份，如 2024
        report_type: 报告类型，可选 "年报", "半年报", "一季报", "三季报"
        download_folder: 下载文件夹路径
        headless: 是否无头模式运行
        
    Returns:
        下载文件的路径，如果失败返回 None
    """
    browser = playwright.chromium.launch(headless=headless, args=["--start-maximized"])
    context = browser.new_context(no_viewport=True)
    page = context.new_page()
    
    save_path = None
    
    try:
        # 访问巨潮资讯网
        page.goto(
            "https://www.cninfo.com.cn/new/disclosure/stock?stockCode=000001&orgId=gssz0000001#periodicReports",
            wait_until="networkidle"
        )
        
        # 输入股票代码并选择
        search_box = page.get_by_role("textbox", name="请输入您要切换公司的代码、简称、拼音")
        search_box.click()
        search_box.fill(stock_code)
        
        # 等待搜索结果并点击
        page.get_by_text(stock_code).first.click()
        page.wait_for_load_state("networkidle")
        
        # 选择报告分类
        page.get_by_role("button", name="分类 ").click()
        page.get_by_role("checkbox", name=report_type, exact=True).click()
        page.get_by_role("button", name="查询 ").click()
        page.wait_for_timeout(1000)
        
        # 构建报告名称的匹配模式
        report_name_pattern = f"{year}年{REPORT_TYPE_MAP[report_type]}"
        
        # 查找匹配的报告链接
        report_links = page.get_by_role("link").filter(
            has_text=re.compile(f".*{report_name_pattern}$")
        )
        
        # 获取第一个匹配的链接
        if report_links.count() == 0:
            print(f"未找到 {stock_code} 的 {year}年{report_type}")
            return None
            
        # 点击链接打开报告页面
        with page.expect_popup() as report_page_info:
            report_links.first.click()
        
        report_page = report_page_info.value
        report_page.wait_for_load_state("networkidle")
        
        # 下载报告
        with report_page.expect_download() as download_info:
            download_button = report_page.locator("div").filter(has_text="公告下载").last
            download_button.click()
        
        download = download_info.value
        original_filename = download.suggested_filename
        
        # 创建下载文件夹
        os.makedirs(download_folder, exist_ok=True)
        save_path = os.path.join(download_folder, original_filename)
        
        # 保存文件
        download.save_as(save_path)
        print(f"下载成功: {save_path}")
        
        report_page.close()
        
    except Exception as e:
        print(f"下载失败: {e}")
        
    finally:
        page.close()
        context.close()
        browser.close()
    
    return save_path


def batch_download_reports(
    stock_codes: list[str],
    years: list[int],
    report_types: list[Literal["年报", "半年报", "一季报", "三季报"]],
    download_folder: str = "downloads",
    headless: bool = False,
) -> dict:
    """
    批量下载股票报告
    
    Args:
        stock_codes: 股票代码列表
        years: 年份列表
        report_types: 报告类型列表
        download_folder: 下载文件夹
        headless: 是否无头模式
        
    Returns:
        下载结果字典
    """
    results = {}
    
    with sync_playwright() as playwright:
        for stock_code in stock_codes:
            for year in years:
                for report_type in report_types:
                    key = f"{stock_code}_{year}_{report_type}"
                    print(f"正在下载: {key}")
                    
                    path = download_stock_report(
                        playwright=playwright,
                        stock_code=stock_code,
                        year=year,
                        report_type=report_type,
                        download_folder=download_folder,
                        headless=headless,
                    )
                    
                    results[key] = {
                        "success": path is not None,
                        "path": path,
                    }
    
    return results


# 使用示例
if __name__ == "__main__":
    # 示例1: 下载单个报告
    with sync_playwright() as playwright:
        download_stock_report(
            playwright=playwright,
            stock_code="600519",  # 贵州茅台
            year=2024,
            report_type="年报",
            download_folder="downloads",
            headless=False,
        )
    
    # 示例2: 批量下载多个报告
    # results = batch_download_reports(
    #     stock_codes=["600519", "000858"],  # 茅台、五粮液
    #     years=[2023, 2024],
    #     report_types=["年报", "半年报"],
    #     download_folder="downloads",
    #     headless=True,
    # )
    # print(results)