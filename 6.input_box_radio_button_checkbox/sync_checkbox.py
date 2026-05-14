from playwright.sync_api import sync_playwright
import random

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://testautomationpractice.blogspot.com/")
    page.wait_for_load_state("load")

    # 1. Select specific checkbox
    # sunday_checkbox = page.get_by_label("Sunday")
    # sunday_checkbox.check()
    # print(sunday_checkbox.is_checked())

    # 2. Check all the checkbox
    # days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    # for day in days:
    #     checkbox = page.get_by_label(day)
    #     checkbox.check()
    #     if checkbox.is_checked():
    #         print(f"{day} is checked")
    #     else:
    #         print(f"{day} is Not checked")
    # page.wait_for_timeout(3000)

    # print("*"*20)
    # 3. Uncheck all the checkbox
    # days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    # for day in days:
    #     checkbox = page.get_by_label(day)
    #     checkbox.uncheck()

    #     if checkbox.is_checked():
    #         print(f"{day} is checked")
    #     else:
    #         print(f"{day} is Not checked")

    # 4. first 5 checkbox
    # days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    # for day in days[:5]:
    #     checkbox = page.get_by_label(day)
    #     checkbox.check()

    #     if checkbox.is_checked():
    #         print(f"{day} is checked")
    #     else:
    #         print(f"{day} is Not checked")
    # page.wait_for_timeout(3000)

    # 5. last 5 checkbox
    # days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    # for day in days[2:]:
    #     checkbox = page.get_by_label(day)
    #     checkbox.uncheck()

    #     if checkbox.is_checked():
    #         print(f"{day} is checked")
    #     else:
    #         print(f"{day} is Not checked")
    # page.wait_for_timeout(3000)

    # 6. Toggle checkbox
    # days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    # for day in days[:2]:
    #     checkbox = page.get_by_label(day)
    #     checkbox.check()
    #     print(f"{day} is selected")
    #     if checkbox.is_checked():
    #         checkbox.uncheck()
    #         print(f"{day} is unselected!")


    # 7. random checkbox
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    random_days = random.sample(days, 3)
    for day in random_days:
        checkbox = page.get_by_label(day)
        checkbox.check()
        print(f"{day} is selected")
        if checkbox.is_checked():
            checkbox.uncheck()
            print(f"{day} is unselected!")

    page.wait_for_timeout(5000)
    page.close()