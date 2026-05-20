from playwright.async_api import async_playwright


class BrowserCrawler:

    async def open_page(self, url):

        playwright = await async_playwright().start()

        browser = await playwright.chromium.launch(
            headless=False
        )

        page = await browser.new_page()

        discovered_links = []

        discovered_requests = []

        # --------------------------------
        # INTERCEPT REQUESTS
        # --------------------------------

        page.on(
            "request",
            lambda request: discovered_requests.append(
                request.url
            )
        )

        # --------------------------------
        # OPEN PAGE
        # --------------------------------

        await page.goto(
            url,
            wait_until="networkidle"
        )

        print("\n[PAGE LOADED SUCCESSFULLY]")

        # --------------------------------
        # EXTRACT LINKS
        # --------------------------------

        links = await page.eval_on_selector_all(
            "a",
            "elements => elements.map(el => el.href)"
        )

        discovered_links.extend(links)

        # --------------------------------
        # PRINT LINKS
        # --------------------------------

        print("\n========== LINKS ==========")

        for link in discovered_links:

            print(f"[LINK] {link}")

        # --------------------------------
        # PRINT RUNTIME REQUESTS
        # --------------------------------

        print("\n========== RUNTIME REQUESTS ==========")

        for req in set(discovered_requests):

            print(f"[API] {req}")

        await browser.close()

        await playwright.stop()

        return {
            "links": discovered_links,
            "requests": discovered_requests
        }