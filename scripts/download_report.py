from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)  # 调试时设为 False
    context = browser.new_context()
    page = context.new_page()
    page.goto("http://www.sse.com.cn/disclosure/listedinfo/announcement/", wait_until="networkidle")
    page.get_by_role("textbox", name="位代码 / 简称").click()
    page.get_by_role("textbox", name="位代码 / 简称").fill("600519")
    page.locator("li > .iconfont").first.click()
    page.wait_for_timeout(2000)

    # 初步筛选包含年度报告的行
    rows = page.locator("tr", has_text="年度报告")
    total = rows.count()
    print(f"初步找到 {total} 行包含 '年度报告' 的公告")

    matched_rows = []

    for i in range(total):
        row = rows.nth(i)
        line = row.inner_text().strip()
        fields = line.split("\t")

        for field in fields[:3]:
            if field.endswith("2024年年度报告"):
                matched_rows.append(row)
                break

    print(f"最终匹配到 {len(matched_rows)} 行符合以 '2024年年度报告' 结尾")

    # 下载每条匹配的公告
    for row in matched_rows:
        print(row.locator)
        download_link = row.locator(".iconfont").last

        # 方法1: 使用 expect_page 捕获新页面
        with context.expect_page() as new_page_info:
            download_link.click()
        
        new_page = new_page_info.value  # 获取新打开的页面
        new_page.wait_for_load_state("domcontentloaded")
        
        print(f"新页面 URL: {new_page.url}")
        
        # 在新页面中操作，比如点击下载按钮
        # 根据实际页面结构修改选择器
        download_btn = new_page.locator("text=下载").first
        if download_btn.count() > 0:
            # 如果下载会触发文件下载
            with new_page.expect_download() as download_info:
                download_btn.click()
            download = download_info.value
            download.save_as(f"./downloads/{download.suggested_filename}")
            print(f"已下载: {download.suggested_filename}")
        
        # 关闭新页面，返回原页面继续
        new_page.close()

    page.close()
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)