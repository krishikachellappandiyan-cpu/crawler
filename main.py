import asyncio
import aiohttp

from urllib.parse import urlparse

from core.fetcher import Fetcher
from core.parser import HTMLParser
from core.queue_manager import QueueManager
from core.normalizer import URLNormalizer
from core.store import Store

from core.js_analyzer import JSAnalyzer
from core.parameter_analyzer import ParameterAnalyzer
from core.form_extractor import FormExtractor
from core.json_writer import JSONWriter
from core.behavior_mapper import BehaviorMapper

from core.auth_detector import AuthDetector
from core.secret_detector import SecretDetector

from browser.playwright_engine import BrowserCrawler

from intelligence.graph_builder import GraphBuilder


async def crawler(target_url):

    # --------------------------------
    # INITIALIZE COMPONENTS
    # --------------------------------

    fetcher = Fetcher()

    parser = HTMLParser()

    queue = QueueManager()

    normalizer = URLNormalizer()

    store = Store()

    browser = BrowserCrawler()

    js_analyzer = JSAnalyzer()

    parameter_analyzer = ParameterAnalyzer()

    form_extractor = FormExtractor()

    json_writer = JSONWriter()

    graph_builder = GraphBuilder()

    behavior_mapper = BehaviorMapper()

    auth_detector = AuthDetector()

    secret_detector = SecretDetector()

    # --------------------------------
    # CONFIG
    # --------------------------------

    max_pages = 5

    crawled_pages = 0

    target_domain = urlparse(
        target_url
    ).netloc

    # --------------------------------
    # RESULTS STORAGE
    # --------------------------------

    results = {

        "target": target_url,

        "endpoints": [],

        "runtime_requests": [],

        "js_endpoints": [],

        "parameters": [],

        "forms": [],

        "behaviors": [],

        "auth_patterns": [],

        "secrets": []
    }

    # --------------------------------
    # START CRAWL
    # --------------------------------

    queue.add(target_url)

    async with aiohttp.ClientSession() as session:

        while True:

            # --------------------------------
            # PAGE LIMIT
            # --------------------------------

            if crawled_pages >= max_pages:

                print(
                    "\n[MAX PAGE LIMIT REACHED]"
                )

                break

            # --------------------------------
            # GET URL
            # --------------------------------

            current_url = queue.get()

            if not current_url:
                break

            crawled_pages += 1

            print(
                f"\n[CRAWLING] {current_url}"
            )

            # --------------------------------
            # ADD PAGE NODE
            # --------------------------------

            graph_builder.add_node(
                current_url,
                "page"
            )

            # --------------------------------
            # FETCH PAGE
            # --------------------------------

            result = await fetcher.fetch(
                session,
                current_url
            )

            if not result:
                continue

            html = result["content"]

            # --------------------------------
            # AUTH DETECTION
            # --------------------------------

            auth_patterns = (
                auth_detector.detect_auth_patterns(
                    html
                )
            )

            for pattern in auth_patterns:

                print(
                    f"[AUTH] {pattern}"
                )

                results[
                    "auth_patterns"
                ].append(pattern)

            # --------------------------------
            # SECRET DETECTION
            # --------------------------------

            secrets = (
                secret_detector.detect_secrets(
                    html
                )
            )

            for secret in secrets:

                print(
                    f"[SECRET] "
                    f"{secret['type']}"
                )

                results["secrets"].append(
                    secret
                )

            # --------------------------------
            # PARSE HTML
            # --------------------------------

            soup = parser.parse(html)

            links = parser.extract_links(
                soup
            )

            # --------------------------------
            # FORM EXTRACTION
            # --------------------------------

            forms = (
                form_extractor.extract_forms(
                    soup
                )
            )

            for form in forms:

                results["forms"].append(
                    form
                )

                print(
                    f"\n[FORM] "
                    f"{form['action']}"
                )

                # --------------------------------
                # GRAPH FORM FLOW
                # --------------------------------

                if form["action"]:

                    graph_builder.add_node(
                        form["action"],
                        "form_action"
                    )

                    graph_builder.add_edge(
                        current_url,
                        form["action"],
                        "submits_to"
                    )

                    # --------------------------------
                    # BEHAVIOR MAPPING
                    # --------------------------------

                    behavior_mapper.add_form_flow(
                        current_url,
                        form["action"]
                    )

            # --------------------------------
            # PROCESS LINKS
            # --------------------------------

            for link in links:

                normalized_url = (
                    normalizer.normalize(
                        current_url,
                        link
                    )
                )

                parsed = urlparse(
                    normalized_url
                )

                # --------------------------------
                # SCOPE LIMITATION
                # --------------------------------

                if (
                    parsed.netloc
                    != target_domain
                ):
                    continue

                print(
                    f"[FOUND] "
                    f"{normalized_url}"
                )

                store.add_endpoint(
                    normalized_url
                )

                queue.add(
                    normalized_url
                )

                results["endpoints"].append(
                    normalized_url
                )

                # --------------------------------
                # GRAPH RELATIONSHIP
                # --------------------------------

                graph_builder.add_node(
                    normalized_url,
                    "endpoint"
                )

                graph_builder.add_edge(
                    current_url,
                    normalized_url,
                    "discovered"
                )

                # --------------------------------
                # BEHAVIOR FLOW
                # --------------------------------

                behavior_mapper.add_navigation(
                    current_url,
                    normalized_url
                )

                # --------------------------------
                # JS ANALYSIS
                # --------------------------------

                if normalized_url.endswith(
                    ".js"
                ):

                    print(
                        f"\n[ANALYZING JS] "
                        f"{normalized_url}"
                    )

                    js_result = (
                        await fetcher.fetch(
                            session,
                            normalized_url
                        )
                    )

                    if not js_result:
                        continue

                    js_content = (
                        js_result["content"]
                    )

                    # --------------------------------
                    # AUTH DETECTION IN JS
                    # --------------------------------

                    js_auth_patterns = (
                        auth_detector.detect_auth_patterns(
                            js_content
                        )
                    )

                    for pattern in js_auth_patterns:

                        print(
                            f"[JS AUTH] {pattern}"
                        )

                        results[
                            "auth_patterns"
                        ].append(pattern)

                    # --------------------------------
                    # SECRET DETECTION IN JS
                    # --------------------------------

                    js_secrets = (
                        secret_detector.detect_secrets(
                            js_content
                        )
                    )

                    for secret in js_secrets:

                        print(
                            f"[JS SECRET] "
                            f"{secret['type']}"
                        )

                        results["secrets"].append(
                            secret
                        )

                    # --------------------------------
                    # JS ENDPOINTS
                    # --------------------------------

                    js_endpoints = (
                        js_analyzer.extract_endpoints(
                            js_content
                        )
                    )

                    for endpoint in js_endpoints:

                        print(
                            f"[JS ENDPOINT] "
                            f"{endpoint}"
                        )

                        results[
                            "js_endpoints"
                        ].append(
                            endpoint
                        )

                        # --------------------------------
                        # GRAPH API FLOW
                        # --------------------------------

                        graph_builder.add_node(
                            endpoint,
                            "api"
                        )

                        graph_builder.add_edge(
                            normalized_url,
                            endpoint,
                            "calls"
                        )

                        # --------------------------------
                        # BEHAVIOR API FLOW
                        # --------------------------------

                        behavior_mapper.add_api_flow(
                            normalized_url,
                            endpoint
                        )

                    # --------------------------------
                    # PARAMETER EXTRACTION
                    # --------------------------------

                    parameters = (
                        parameter_analyzer.extract_parameters(
                            js_content
                        )
                    )

                    for param in parameters:

                        print(
                            f"[PARAM] {param}"
                        )

                        results[
                            "parameters"
                        ].append(
                            param
                        )

            # --------------------------------
            # PLAYWRIGHT DYNAMIC CRAWLING
            # --------------------------------

            try:

                browser_data = (
                    await browser.open_page(
                        current_url
                    )
                )

                dynamic_links = (
                    browser_data["links"]
                )

                runtime_requests = (
                    browser_data["requests"]
                )

                # --------------------------------
                # DYNAMIC LINKS
                # --------------------------------

                for dynamic_link in dynamic_links:

                    parsed_dynamic = (
                        urlparse(
                            dynamic_link
                        )
                    )

                    if (
                        parsed_dynamic.netloc
                        != target_domain
                    ):
                        continue

                    print(
                        f"[BROWSER FOUND] "
                        f"{dynamic_link}"
                    )

                    store.add_endpoint(
                        dynamic_link
                    )

                    queue.add(
                        dynamic_link
                    )

                    results["endpoints"].append(
                        dynamic_link
                    )

                    # --------------------------------
                    # GRAPH DYNAMIC FLOW
                    # --------------------------------

                    graph_builder.add_node(
                        dynamic_link,
                        "dynamic_endpoint"
                    )

                    graph_builder.add_edge(
                        current_url,
                        dynamic_link,
                        "browser_discovered"
                    )

                    # --------------------------------
                    # BEHAVIOR DYNAMIC FLOW
                    # --------------------------------

                    behavior_mapper.add_navigation(
                        current_url,
                        dynamic_link
                    )

                # --------------------------------
                # RUNTIME REQUESTS
                # --------------------------------

                for request_url in runtime_requests:

                    print(
                        f"[API] {request_url}"
                    )

                    results[
                        "runtime_requests"
                    ].append(
                        request_url
                    )

            except Exception as error:

                print(
                    f"[BROWSER ERROR] "
                    f"{error}"
                )

    # --------------------------------
    # EXPORT BEHAVIORS
    # --------------------------------

    results["behaviors"] = (
        behavior_mapper.export_behaviors()
    )

    # --------------------------------
    # SAVE JSON
    # --------------------------------

    json_writer.save(results)

    # --------------------------------
    # SAVE GRAPH
    # --------------------------------

    graph_builder.export_json()

    # --------------------------------
    # FINAL OUTPUT
    # --------------------------------

    print(
        "\n========== "
        "DISCOVERED ENDPOINTS =========="
    )

    for endpoint in store.endpoints:

        print(endpoint)


# --------------------------------
# ENTRY POINT
# --------------------------------

if __name__ == "__main__":

    target = input(
        "Enter target URL: "
    ).strip()

    asyncio.run(
        crawler(target)
    )