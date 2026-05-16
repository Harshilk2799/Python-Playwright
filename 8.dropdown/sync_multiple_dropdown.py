from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://testautomationpractice.blogspot.com/")
    page.wait_for_load_state("load")

    # Method 1
    # page.locator("#colors").select_option(value=["red", "blue", "green", "white"])
    # page.select_option("#colors", value=["red", "blue", "green", "white"])

    # Method 2
    # page.locator("#colors").select_option(label=["Red", "Blue", "Green"])
    # page.select_option("#colors", label=["Red", "Blue", "Green"])

    # Method 3
    # page.locator("#colors").select_option(index=[0, 2, 3])
    # page.select_option("#colors", index=[0, 2, 3])


    # dropdown_options = page.locator("#colors > option")
    # print("count: ", dropdown_options.count())
    # print("Content: ", dropdown_options.all_text_contents())

    # options_text = [text.strip() for text in dropdown_options.all_text_contents()]
    # print(options_text)


    # sorted dropdow
    # dropdown_options = page.locator("#colors>option")
    dropdown_options = page.locator("#animals>option")
    
    options_text = [text.strip() for text in dropdown_options.all_text_contents()]
    
    original_list = options_text.copy()
    sorted_list = sorted(options_text)

    print("Original list:", original_list)
    print("Sorted list: ", sorted_list)

    if original_list == sorted_list:
        print("Dropdown options are sorted order...")
    else:
        print("Dropdown options are not sorted order...")

    page.wait_for_timeout(5000)
    page.close()