import asyncio

from playwright.async_api import async_playwright



async def main() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.firefox.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://chat.openai.com/")
        await page.click("[data-testid=\"login-button\"]")
        await page.type("#email-input", EMAIL)
        await page.click(".continue-btn")
        await page.type("#password", PASSWORD)
        await page.click("[data-action-button-primary=\"true\"]")
        lastMessage = None
        while True:
            await page.type("#prompt-textarea", input("> "))
            await page.locator("#prompt-textarea").press("Enter")
            newMessage = page.locator("[data-message-author-role=\"assistant\"]").last
            while lastMessage == newMessage:
                await asyncio.sleep(0.1)
            message = await newMessage.locator("p").text_content()
            lastMessage = newMessage
            print(message)

if __name__ == "__main__":
    asyncio.run(main())