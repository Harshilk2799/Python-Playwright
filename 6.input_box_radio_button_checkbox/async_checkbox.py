from playwright.async_api import async_playwright
import asyncio
import random

async def main():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://testautomationpractice.blogspot.com/")
        await page.wait_for_load_state("load")

        # 1. Select specific checkbox
        # sunday_checkbox = page.get_by_label("Sunday")
        # await sunday_checkbox.check()
        # print(await sunday_checkbox.is_checked())

        # 2. Check all the checkbox
        # days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        # for day in days:
        #     checkbox = page.get_by_label(day)
        #     await checkbox.check()
        #     if await checkbox.is_checked():
        #         print(f"{day} is checked")
        #     else:
        #         print(f"{day} is Not checked")
        # await page.wait_for_timeout(3000)

        # print("*"*20)
        # 3. Uncheck all the checkbox
        # days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        # for day in days:
        #     checkbox = page.get_by_label(day)
        #     await checkbox.uncheck()

        #     if await checkbox.is_checked():
        #         print(f"{day} is checked")
        #     else:
        #         print(f"{day} is Not checked")

        # 4. first 5 checkbox
        # days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        # for day in days[:5]:
        #     checkbox = page.get_by_label(day)
        #     await checkbox.check()

        #     if await checkbox.is_checked():
        #         print(f"{day} is checked")
        #     else:
        #         print(f"{day} is Not checked")
        # await page.wait_for_timeout(3000)

        # 5. last 5 checkbox
        # days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        # for day in days[2:]:
        #     checkbox = page.get_by_label(day)
        #     await checkbox.uncheck()

        #     if await checkbox.is_checked():
        #         print(f"{day} is checked")
        #     else:
        #         print(f"{day} is Not checked")
        # await page.wait_for_timeout(3000)

        # 6. Toggle checkbox
        # days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        # for day in days[:2]:
        #     checkbox = page.get_by_label(day)
        #     await checkbox.check()
        #     print(f"{day} is selected")
        #     if await checkbox.is_checked():
        #         await checkbox.uncheck()
        #         print(f"{day} is unselected!")


        # 7. random checkbox
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        random_days = random.sample(days, 3)
        for day in random_days:
            checkbox = page.get_by_label(day)
            await checkbox.check()
            print(f"{day} is selected")
            if await checkbox.is_checked():
                await checkbox.uncheck()
                print(f"{day} is unselected!")

        await page.wait_for_timeout(5000)
        await page.close()

if __name__ == "__main__":
    asyncio.run(main())