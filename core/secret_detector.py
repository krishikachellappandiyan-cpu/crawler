import re


class SecretDetector:

    def detect_secrets(
        self,
        content
    ):

        patterns = {

            "jwt": r"eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9._-]+\.[a-zA-Z0-9._-]+",

            "bearer_token": r"Bearer\s+[a-zA-Z0-9._-]+",

            "api_key": r"api[_-]?key['\"]?\s*[:=]\s*['\"][a-zA-Z0-9_-]{16,}",

            "authorization": r"Authorization"
        }

        findings = []

        for secret_type, pattern in patterns.items():

            matches = re.findall(
                pattern,
                content
            )

            for match in matches:

                findings.append({

                    "type": secret_type,

                    "value": str(match)[:100]
                })

        return findings