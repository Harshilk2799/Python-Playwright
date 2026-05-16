from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://testautomationpractice.blogspot.com/")
    page.wait_for_load_state("load")

    # Method 1
    # page.locator("#country").select_option("India")
    # page.select_option("#country", "India")

    # Method 2
    # page.locator("#country").select_option(value="india")
    # page.select_option("#country", value="india")

    # Method 3
    # page.locator("#country").select_option(index=9)
    # page.select_option("#country", index=9)


    # dropdown_options = page.locator("#country > option")
    # print("count: ", dropdown_options.count())
    # print("Content: ", dropdown_options.all_text_contents())

    # options_text = [text.strip() for text in dropdown_options.all_text_contents()]
    # print(options_text)


    page.wait_for_timeout(5000)
    page.close()