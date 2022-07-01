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


async def connect_to_db() -> asyncpg.Connection:
    conn = await asyncpg.connect(
        user=settings.DB_USER, password=settings.DB_PASSWORD,
        database=settings.DB_NAME, host=settings.DB_HOST
    )

    logger.info('Connected to database')

    return conn


async def is_table_exists(conn: asyncpg.Connection) -> bool:
    is_exists = await conn.fetchrow("SELECT COUNT(*) = 1 FROM information_schema.tables WHERE table_name = 'cities';")

    logger.info('Is table exists: ' + str(is_exists[0]))

    return is_exists[0]


async def truncate_table(conn: asyncpg.Connection):
    await conn.execute('TRUNCATE cities;')

    logger.info('Truncated cities table')


async def create_table(conn: asyncpg.Connection):
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


async def populate_table(conn: asyncpg.Connection, cities: list[dict]):
    for city in cities:
        await conn.execute(
            '''INSERT INTO cities(id, name, link, population) VALUES ($1, $2, $3, $4)''',
            city['id'], city['name'].rstrip(), city['link'], city['population']
        )

    logger.info('Added cities to database')


async def search(conn: asyncpg.Connection, query: str) -> list[asyncpg.Record]:
    cities = await conn.fetch(
        'SELECT * FROM cities WHERE LOWER(name) LIKE $1', f'%{query.lower()}%'
    )

    logger.info('Retrieved cities named like {name}')

    return cities


async def retrieve(conn: asyncpg.Connection, name: str) -> dict:
    city = await conn.fetchrow(
        'SELECT * FROM cities WHERE name = $1', name
    )

    logger.info('Retrieved city {name} data')

    return dict(city)
