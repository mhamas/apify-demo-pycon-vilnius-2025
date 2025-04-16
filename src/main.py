from __future__ import annotations

from apify import Actor
from crawlee.crawlers import BeautifulSoupCrawler, BeautifulSoupCrawlingContext


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        start_urls = [
            url.get('url')
            for url in actor_input.get('start_urls', [])
        ]

        if not start_urls:
            Actor.log.info('No start URLs specified in Actor input, exiting...')
            await Actor.exit()

        crawler = BeautifulSoupCrawler()

        @crawler.router.default_handler
        async def request_handler(context: BeautifulSoupCrawlingContext) -> None:
            url = context.request.url
            day = url.split('/')[-1]
            Actor.log.info(f'Scraping {url}...')
            soup = context.soup
            talk_links = soup.find_all(
                'a',
                href=lambda x: x and (x.startswith('/2025/talks') or x.startswith('/talks/'))
            )

            for link in talk_links:
                talk_title = link.text.strip()
                speaker_name = None

                parent_div = link.find_parent('div')
                if parent_div:
                    speaker_spans = parent_div.find_all('span')
                    if speaker_spans:
                        speaker_span = speaker_spans[-1]
                        speaker_name = speaker_span.text.strip()

                Actor.log.info(f'Speaker: {speaker_name}, Talk: {talk_title}, Day: {day}')

                await Actor.push_data({
                    'speaker_name': speaker_name,
                    'talk_title': talk_title,
                    'day': day,
                })

        await crawler.run(start_urls)