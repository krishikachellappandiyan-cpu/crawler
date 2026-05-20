from urllib.parse import urljoin


class URLNormalizer:

    def normalize(self, base, url):

        return urljoin(base, url)