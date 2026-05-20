import asyncio
import aiohttp
from urllib.parse import urlparse

from core.fetcher import Fetcher
from core.parser import HTMLParser
from core.queue_manager import QueueManager
from core.normalizer import URLNormalizer
from core.store import Store

from browser.playwright_engine import BrowserCrawler

from core.js_analyzer import JSAnalyzer
from core.parameter_analyzer import ParameterAnalyzer


async def crawler(target):

    # --------------------------------
    # CORE COMPONENTS
    # --------------------------------

    fetcher = Fetcher()

    parser = HTMLParser()

    queue = QueueManager()

    normalizer = URLNormalizer()

    store = Store()

    browser = BrowserCrawler()

    js_analyzer = JSAnalyzer()

    parameter_analyzer = ParameterAnalyzer()

    # --------------------------------
    # CONFIG
    # --------------------------------

    max_pages = 20

    crawled_pages = 0

    target_domain = urlparse(target).netloc

    # --------------------------------
    # START CRAWL
    # --------------------------------

    queue.add(target)

    async with aiohttp.ClientSession() as session:

        while True:

            # --------------------------------
            # PAGE LIMIT
            # --------------------------------

            if crawled_pages >= max_pages:

                print("\n[MAX PAGE LIMIT REACHED]")

                break

            # --------------------------------
            # GET NEXT URL
            # --------------------------------

            url = queue.get()

            if not url:
                break

            crawled_pages += 1

            print(f"\n[CRAWLING] {url}")

            # --------------------------------
            # FETCH PAGE
            # --------------------------------

            result = await fetcher.fetch(
                session,
                url
            )

            if not result:
                continue

            html = result["content"]

            # --------------------------------
            # PARSE HTML
            # --------------------------------

            soup = parser.parse(html)

            links = parser.extract_links(soup)

            # --------------------------------
            # PROCESS STATIC LINKS
            # --------------------------------

            for link in links:

                full_url = normalizer.normalize(
                    url,
                    link
                )

                parsed = urlparse(full_url)

                # --------------------------------
                # SCOPE LIMITATION
                # --------------------------------

                if parsed.netloc != target_domain:
                    continue

                print(f"[FOUND] {full_url}")

                store.add_endpoint(full_url)

                queue.add(full_url)

                # --------------------------------
                # ANALYZE STATIC JS FILES
                # --------------------------------

                if full_url.endswith(".js"):

                    print(
                        f"\n[ANALYZING JS] {full_url}"
                    )

                    js_result = await fetcher.fetch(
                        session,
                        full_url
                    )

                    if js_result:

                        js_content = (
                            js_result["content"]
                        )

                        # --------------------------------
                        # JS ENDPOINT EXTRACTION
                        # --------------------------------

                        js_endpoints = (
                            js_analyzer.extract_endpoints(
                                js_content
                            )
                        )

                        print(
                            "\n========== JS ENDPOINTS =========="
                        )

                        for endpoint in js_endpoints:

                            print(
                                f"[JS ENDPOINT] {endpoint}"
                            )

                        # --------------------------------
                        # PARAMETER EXTRACTION
                        # --------------------------------

                        parameters = (
                            parameter_analyzer.extract_parameters(
                                js_content
                            )
                        )

                        print(
                            "\n========== PARAMETERS =========="
                        )

                        for param in parameters:

                            print(
                                f"[PARAM] {param}"
                            )

            # --------------------------------
            # PLAYWRIGHT DYNAMIC CRAWLING
            # --------------------------------

            try:

                browser_data = await browser.open_page(
                    url
                )

                dynamic_links = (
                    browser_data["links"]
                )

                runtime_requests = (
                    browser_data["requests"]
                )

                # --------------------------------
                # PROCESS DYNAMIC LINKS
                # --------------------------------

                if dynamic_links:

                    for dynamic_link in dynamic_links:

                        parsed_dynamic = urlparse(
                            dynamic_link
                        )

                        if (
                            parsed_dynamic.netloc
                            != target_domain
                        ):
                            continue

                        print(
                            f"[BROWSER FOUND] {dynamic_link}"
                        )

                        store.add_endpoint(
                            dynamic_link
                        )

                        queue.add(dynamic_link)

                # --------------------------------
                # ANALYZE RUNTIME JS FILES
                # --------------------------------

                for request_url in runtime_requests:

                    if request_url.endswith(".js"):

                        print(
                            f"\n[ANALYZING JS] {request_url}"
                        )

                        js_result = await fetcher.fetch(
                            session,
                            request_url
                        )

                        if js_result:

                            js_content = (
                                js_result["content"]
                            )

                            # --------------------------------
                            # JS ENDPOINT EXTRACTION
                            # --------------------------------

                            js_endpoints = (
                                js_analyzer.extract_endpoints(
                                    js_content
                                )
                            )

                            print(
                                "\n========== JS ENDPOINTS =========="
                            )

                            for endpoint in js_endpoints:

                                print(
                                    f"[JS ENDPOINT] {endpoint}"
                                )

                            # --------------------------------
                            # PARAMETER EXTRACTION
                            # --------------------------------

                            parameters = (
                                parameter_analyzer.extract_parameters(
                                    js_content
                                )
                            )

                            print(
                                "\n========== PARAMETERS =========="
                            )

                            for param in parameters:

                                print(
                                    f"[PARAM] {param}"
                                )

            except Exception as e:

                print(f"[BROWSER ERROR] {e}")

    # --------------------------------
    # FINAL OUTPUT
    # --------------------------------

    print("\n========== ENDPOINTS ==========")

    for endpoint in store.endpoints:

        print(endpoint)


# --------------------------------
# ENTRY POINT
# --------------------------------

if __name__ == "__main__":

    target = input("Enter target URL: ")

    asyncio.run(crawler(target))