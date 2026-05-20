import re


class ParameterAnalyzer:

    def extract_parameters(self, content):

        pattern = r"[?&]([a-zA-Z][a-zA-Z0-9_-]{2,30})="

        matches = re.findall(pattern, content)

        blacklist = {
            "const",
            "function",
            "return",
            "true",
            "false"
        }

        filtered = []

        for match in matches:

            if match not in blacklist:

                filtered.append(match)

        return list(set(filtered))