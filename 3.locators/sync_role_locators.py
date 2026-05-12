from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # page.goto("https://testautomationpractice.blogspot.com/")

    # 1. get_by_placeholder()
    # page.get_by_placeholder("Enter Name").fill("Harshil")
    # page.get_by_placeholder("Enter EMail").fill("harshil@gmail.com")
    # page.get_by_placeholder("Enter Phone").fill("7984955789")

    page.goto("https://testautomationpractice.blogspot.com/p/playwrightpractice.html")

    # 2. get_by_text()
    # page.get_by_text("List item 1")
    # page.get_by_text("List item 1", exact=True)

    # 3. get_by_label()
    # page.get_by_label("email").fill("harshil@gmail.com")
    # page.get_by_label("password").fill("harshil")

    # 4. get_by_alt_text()
    # page.get_by_alt_text("logo image", exact=True).is_visible()
    # print("Working")

    # 5. get_by_title()
    # print(page.get_by_title("Home page link").is_visible())

    # 6. get_by_test_id()
    # print(page.get_by_test_id("product-price").all_text_contents())

    # 7. get_by_role()
    print(page.get_by_role("button", name="Primary Action").inner_text())
    page.close()