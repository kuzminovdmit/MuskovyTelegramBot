import asyncio
import asyncpg
import logging
import settings
import sys


logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)

logger = logging.getLogger('db')


async def create_table():
    conn = await asyncpg.connect(
        user=settings.DB_USER, password=settings.DB_PASSWORD,
        database=settings.DB_NAME, host=settings.DB_HOST
    )

    logger.info('Connected to database')

    await conn.execute('''
        CREATE TABLE cities(
            id INT NOT NULL,
            name CHARACTER(64) NOT NULL,
            link CHARACTER(256) NOT NULL,
            population INT NOT NULL,
            PRIMARY KEY(id)
        );
    ''')

    logger.info('Created cities table')

    await conn.close()


async def fill_db(cities: list[dict]):
    conn = await asyncpg.connect(
        user=settings.DB_USER, password=settings.DB_PASSWORD,
        database=settings.DB_NAME, host=settings.DB_HOST
    )

    logger.info('Connected to database')

    for city in cities:
        await conn.execute(
            '''INSERT INTO cities(id, name, link, population) VALUES ($1, $2, $3, $4)''',
            city['id'], city['name'], city['link'], city['population']
        )

    logger.info('Added city data to database')

    await conn.close()


async def get_all_cities_name() -> list[str]:
    conn = await asyncpg.connect(
        user=settings.DB_USER, password=settings.DB_PASSWORD,
        database=settings.DB_NAME, host=settings.DB_HOST
    )

    logger.info('Connected to database')

    cities = await conn.fetch(
        'SELECT name FROM cities;'
    )

    logger.info('Retrieved city data to database')

    await conn.close()

    return cities


async def get_cities_by_name(name: str) -> list[str]:
    conn = await asyncpg.connect(
        user=settings.DB_USER, password=settings.DB_PASSWORD,
        database=settings.DB_NAME, host=settings.DB_HOST
    )

    logger.info('Connected to database')

    cities = await conn.fetch(
        'SELECT * FROM cities WHERE name LIKE $1', f'%{name}%'
    )

    logger.info('Retrieved cities like {name}')

    await conn.close()

    return cities


async def get_city_by_name(name: str) -> dict:
    conn = await asyncpg.connect(
        user=settings.DB_USER, password=settings.DB_PASSWORD,
        database=settings.DB_NAME, host=settings.DB_HOST
    )

    logger.info('Connected to database')

    city = await conn.fetchrow(
        'SELECT * FROM cities WHERE name = $1', name
    )

    logger.info('Retrieved city {name} data')

    await conn.close()

    return dict(city)
