from bs4 import BeautifulSoup


class HTMLParser:

    # --------------------------------
    # PARSE HTML
    # --------------------------------

    def parse(self, html):

        return BeautifulSoup(
            html,
            "lxml"
        )

    # --------------------------------
    # EXTRACT LINKS
    # --------------------------------

    def extract_links(self, soup):

        discovered = set()

        # --------------------------------
        # <a href="">
        # --------------------------------

        for tag in soup.find_all("a"):

            href = tag.get("href")

            if href:

                discovered.add(href)

        # --------------------------------
        # <script src="">
        # --------------------------------

        for script in soup.find_all("script"):

            src = script.get("src")

            if src:

                discovered.add(src)

        # --------------------------------
        # <link href="">
        # --------------------------------

        for link in soup.find_all("link"):

            href = link.get("href")

            if href:

                discovered.add(href)

        return list(discovered)