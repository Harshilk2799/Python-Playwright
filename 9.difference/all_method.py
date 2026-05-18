from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demowebshop.tricentis.com/")

    products = page.locator(".product-title").all()
    for product in products:
        print(product.text_content())
        print("*"*20)
        print(product.inner_text())    

    page.close()