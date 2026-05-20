from bs4 import BeautifulSoup


class HTMLParser:

    def parse(self, html):

        return BeautifulSoup(html, "lxml")

    def extract_links(self, soup):

        links = []

        for tag in soup.find_all("a"):

            href = tag.get("href")

            if href:
                links.append(href)

        return links