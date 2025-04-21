import logging
import uuid

import pytest
from dotenv import load_dotenv
from core import CoreService
from common import EntityInfo
from datetime import datetime

load_dotenv()
core = CoreService()


@pytest.mark.asyncio
async def test_add_data():
    await core.start()
    await core.api.add_entity(EntityInfo(
        id=uuid.uuid4().hex,
        entity_type=1,
        name="test",
        data={"name": "xiaoyou2"},
        create_time=datetime.now()
    ))

@pytest.mark.asyncio
async def test_get_data():
    await core.start()
    res = await core.api.get_entity('1468ba3257f04f47986663f7373a3018')
    logging.info(f"record info {res}")
    logging.info(f"record info {res.create_time.timestamp()}")


@pytest.mark.asyncio
async def test_upload_data():
    await core.start()
    with open("test.png", "rb") as f:
        key = await core.api.file.add_file("test.png", f.read())
        logging.info(f"file key {key}")


@pytest.mark.asyncio
async def test_get_object():
    await core.start()
    file, link = await core.api.file.get_file_link("6dd3363a5c1e48c89847d74b09c0347a")
    logging.info(f"file {file} link {link}")
