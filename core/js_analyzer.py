import re


class JSAnalyzer:

    def extract_endpoints(self, js_content):

        patterns = [
            r"https?://[^\s\"'<>]+",
            r"/api/[a-zA-Z0-9_/.-]+",
            r"/graphql",
            r"/v1/[a-zA-Z0-9_/.-]+",
            r"/v2/[a-zA-Z0-9_/.-]+"
        ]

        discovered = set()

        for pattern in patterns:

            matches = re.findall(pattern, js_content)

            for match in matches:
                discovered.add(match)

        return list(discovered)