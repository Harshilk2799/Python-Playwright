from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://testautomationpractice.blogspot.com/")
    page.wait_for_load_state("load")

    # Method 1
    # page.fill("input#name", "Harshil")
    # page.fill("input#email", "harshil@gmail.com")
    # page.fill("input#phone", "7984985798")

    # Method 2
    # page.locator("input#name").fill("harshil")
    # page.locator("input#email").fill("harshil@gmail.com")
    # page.locator("input#phone").fill("7984985798")

    # Method 3
    # page.locator("input#name").type("harshil")
    # page.locator("input#email").type("harshil@gmail.com")
    # page.locator("input#phone").type("7984985798")

    # Method 4
    # page.locator("input#name").press_sequentially("harshil")
    # page.locator("input#email").press_sequentially("harshil@gmail.com")
    # page.locator("input#phone").press_sequentially("7984985798")



    # page.locator("input#phone").fill("7984985798")
    # page.locator("input#phone").clear()

    phone_locator = page.locator("input#phone")
    phone_locator.fill("64654532132")
    print("Phone value is: ", phone_locator.input_value())

    page.wait_for_timeout(5000)
    page.close()