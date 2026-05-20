import aiohttp


class Fetcher:

    async def fetch(self, session, url):

        try:

            async with session.get(url, timeout=15) as response:

                text = await response.text(errors="ignore")

                return {
                    "url": url,
                    "status": response.status,
                    "content": text
                }

        except Exception as e:

            print(f"[ERROR] {url} -> {e}")

            return None