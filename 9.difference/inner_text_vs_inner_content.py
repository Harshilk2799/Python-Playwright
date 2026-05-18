from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demowebshop.tricentis.com/")

    products = page.locator("h2.product-title a")
    print("Using inner_content()======>",products.nth(1).text_content())
    print("Using inner_text()========>",products.nth(1).inner_text())
    page.close()