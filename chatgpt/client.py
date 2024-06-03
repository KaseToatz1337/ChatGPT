import asyncio

from playwright.async_api import async_playwright, Playwright, Browser, Page
from html2text import html2text

from .constants import *
from .response import Response
from .exceptions import RequiresLogin

class ChatGPT:

    def __init__(self, email: str, password: str) -> None:
        self._playwright: Playwright = None
        self._driver: Browser = None
        self._page: Page = None
        self.email = email
        self.password = password
        self.histories: dict[str, list[Response]]

    async def login(self) -> None:
        self._playwright = await async_playwright().start()
        self._driver = await self._playwright.firefox.launch()
        self._page = await self._driver.new_page()
        await self._page.goto(BASE_URL)
        await self._page.wait_for_url(LOGIN_URL_REGEX)
        await self._page.click(LOGIN_BUTTON_SELECTOR)
        await self._page.type(EMAIL_INPUT_SELECTOR, self.email)
        await self._page.click(CONTINUE_BUTTON_SELECTOR)
        await self._page.type(PASSWORD_INPUT_SELECTOR, self.password)
        await self._page.click(CONFIRM_LOGIN_BUTTON_SELECTOR)

    async def chat(self, prompt: str, historyID: str | None = None) -> Response:
        try:
            if not self._driver or not self._page:
                raise RequiresLogin
            if not BASE_URL_REGEX.match(self._page.url):
                await self._page.goto(f"{BASE_URL}/c/{historyID}" if historyID else BASE_URL)
            elif historyID and (not HISTORY_REGEX.match(self._page.url) or HISTORY_REGEX.match(self._page.url).group(1) != historyID):
                await self._page.goto(f"{BASE_URL}/c/{historyID}")
            elif not historyID and HISTORY_REGEX.match(self._page.url):
                await self._page.goto(BASE_URL)
            await self._page.wait_for_load_state()
            lastMessageID = await self._page.locator(MESSAGE_SELECTOR).last.get_attribute(MESSAGE_ID_ATTRIBUTE) if await self._page.locator(MESSAGE_SELECTOR).count() > 0 else None
            await self._page.type(PROMPT_INPUT_SELECTOR, prompt)
            await self._page.locator(PROMPT_INPUT_SELECTOR).press("Enter")
            while await self._page.locator(MESSAGE_SELECTOR).last.get_attribute(MESSAGE_ID_ATTRIBUTE) == lastMessageID or not await self._page.locator(REACTION_BUTTONS_SELECTOR).last.is_visible():
                await asyncio.sleep(0.1)
            history = HISTORY_REGEX.match(self._page.url).group(1)
            response = Response(html2text(await self._page.locator(MESSAGE_SELECTOR).last.inner_html()).strip(), history)
            if history not in self.histories.keys():
                self.histories[history] = []
            self.histories[history].append(Response(prompt, history, True))
            self.histories[history].append(response)
            return response
        except:
            await self.close()
            await self.login()
            await self.chat(prompt, historyID)
    
    async def close(self) -> None:
        await self._driver.close()
        await self._playwright.stop()