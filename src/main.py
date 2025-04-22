from __future__ import annotations

from apify import Actor
from crawlee.crawlers import BeautifulSoupCrawler, BeautifulSoupCrawlingContext
from datetime import timedelta

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

        crawler = BeautifulSoupCrawler(
            max_request_retries=0,
            request_handler_timeout=timedelta(minutes=10),
        )

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

                linkedin_url = None
                if speaker_name:
                    try:
                        call_result = await Actor.call('apify/google-search-scraper', {
                            "forceExactMatch": False,
                            "includeIcons": False,
                            "includeUnfilteredResults": False,
                            "maxPagesPerQuery": 1,
                            "mobileResults": False,
                            "queries": f'site:linkedin.com/in \"{speaker_name}\"',
                            "resultsPerPage": 10,
                            "saveHtml": False,
                            "saveHtmlToKeyValueStore": False
                        })
                        if call_result:
                            dataset = await Actor.open_dataset(id=call_result.default_dataset_id, force_cloud=True)
                            async for page in dataset.iterate_items():
                                for result in page['organicResults']:
                                    if not linkedin_url and 'linkedin.com/in' in result.get('url', ''):
                                            linkedin_url = result.get('url')
                    except Exception as e:
                        Actor.log.error(f'Error getting LinkedIn URL for {speaker_name}: {e}')

                    Actor.log.info(f'Speaker: {speaker_name}, Talk: {talk_title}, LinkedIn: {linkedin_url}, Day: {day}')

                await Actor.charge('speaker')
                await Actor.push_data({
                    'speaker_name': speaker_name,
                    'talk_title': talk_title,
                    'linkedin_url': linkedin_url,
                    'day': day,
                })

        await crawler.run(start_urls)