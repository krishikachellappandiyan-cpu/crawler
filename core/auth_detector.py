class AuthDetector:

    def detect_auth_patterns(
        self,
        content
    ):

        auth_keywords = [

            "login",
            "logout",
            "signin",
            "signup",
            "register",
            "token",
            "jwt",
            "auth",
            "session",
            "oauth",
            "bearer",
            "password",
            "forgot-password",
            "reset-password",
            "refresh-token"
        ]

        discovered = []

        content = content.lower()

        for keyword in auth_keywords:

            if keyword in content:

                discovered.append(keyword)

        return list(set(discovered))
    