from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://testautomationpractice.blogspot.com/")

    # Method 1
    # page.locator("input#male").click()
    # is_male_selected = page.locator("input[value='male']").is_checked()
    # is_female_selected = page.locator("input[value='female']").is_checked()

    # print(f"Male selected: {is_male_selected}")
    # print(f"Female selected: {is_female_selected}")

    # Method 2
    # page.get_by_role("radio", name="Female").check()
    # is_male_selected = page.locator("input[value='male']").is_checked()
    # is_female_selected = page.locator("input[value='female']").is_checked()

    # print(f"Male selected: {is_male_selected}")
    # print(f"Female selected: {is_female_selected}")

    page.wait_for_timeout(5000)
    page.close()