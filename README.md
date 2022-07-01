# MuscovyTelegramBot
Telegram bot, which helps people to find wikipedia page of cities in Moscow Oblast.

## Dependencies
### Software
* Python
* PostgreSQL

### Python libraries
* beautifulsoup4
* aiohttp
* asyncpg
* aiogram

## Install

1. Create settings.py for environmental variables

```python
DB_NAME = 'name'
DB_USER = 'user_name'
DB_PASSWORD = 'user_password'
DB_HOST = 'host'
API_TOKEN = 'token'
```

2. Run main.py