import logging

import pytest
from dotenv import load_dotenv
from infra import Config, Db

load_dotenv()
config = Config()
db = Db(config)


@pytest.mark.asyncio
async def test_db_select():
    await db.start()
    data = await db.select_all("entity_relation")
    logging.info(f"people is {data}")

@pytest.mark.asyncio
async def test_db_add_relation():
    await db.start()
    data = await db.add_relation(
        "entity_relation",
        "entity",
        "1468ba3257f04f47986663f7373a3018",
        "6ab6d57cfaf54ad58eddf0a3738c37db",
        data={"relation": "friend"}
    )
    logging.info(f"people is {data}")
