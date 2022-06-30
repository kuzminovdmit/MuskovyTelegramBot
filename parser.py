from aiohttp import ClientSession
from bs4 import BeautifulSoup

import asyncio
import logging
import sys


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)

logger = logging.getLogger('parser')

BASE_URL = 'https://ru.wikipedia.org'
CITIES_URL = '/wiki/%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D1%81%D0%BA%D0%B8%D0%B5_%D0%BD%D0%B0%D1%81%D0%B5%D0%BB%D1%91%D0%BD' \
             '%D0%BD%D1%8B%D0%B5_%D0%BF%D1%83%D0%BD%D0%BA%D1%82%D1%8B_%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0' \
             '%BA%D0%BE%D0%B9_%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D0%B8'


async def parser():
    async with ClientSession() as session:
        async with session.get(BASE_URL + CITIES_URL) as response:
            logger.info(f'Got request {response.status} for {response.url}')
            html = await response.text()

        cities = []
        soup = BeautifulSoup(html, 'lxml')

        for tr in soup.find_all('table', class_='standard sortable', limit=1)[0].find_all('tr')[1:]:
            city_data = tr.find_all('td')
            cities.append({
                'id': int(city_data[0].string),
                'link': BASE_URL + city_data[1].a['href'],
                'name': city_data[1].a['title'],
                'population': int(city_data[4]['data-sort-value'])
            })

        logger.info(f'Parsed {len(cities)} cities')

        return cities


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(parser())

