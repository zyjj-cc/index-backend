import logging

import pytest
from dotenv import load_dotenv
from infra import Config, Db

load_dotenv()
config = Config()
db = Db(config)


@pytest.mark.asyncio
async def test_db_select():
    await db.init()
    data = await db.select("exk9ktkxqj1ljx3sjia1")
    logging.info(f"people is {data}")
