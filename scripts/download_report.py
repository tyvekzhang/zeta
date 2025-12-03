import time
from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    page.goto(
        "http://www.sse.com.cn/disclosure/listedinfo/announcement/",
        wait_until="networkidle",
    )

    # 输入 600519
    locator = page.get_by_role("textbox", name="位代码 / 简称")
    locator.click()
    locator.fill("600519")
    page.locator("li > .iconfont").first.click()

    # 点击“贵州茅台2024年年度报告”
    with page.expect_popup() as detail_info:
        page.get_by_role("link", name="贵州茅台2024年年度报告", exact=True).click()
    detail_page = detail_info.value
    pdf_url = detail_page.url
    print(f"pdf_url: {pdf_url}")
    page.close()
    context.close()
    browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
