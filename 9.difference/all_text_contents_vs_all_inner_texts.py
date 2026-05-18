from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demowebshop.tricentis.com/")

    products = page.locator(".product-title")
    # print("Using inner_content()======>",products.nth(1).text_content())
    # print("Using inner_text()========>",products.nth(1).inner_text())


    # product_names = [product for product in products.all_inner_texts()]
    # print(products.all_inner_texts())
    # print(product_names)


    # print("=============")
    # product_names = [product.strip() for product in products.all_text_contents()]
    # print(product_names)
    # print(products.all_text_contents())

    
    page.close()