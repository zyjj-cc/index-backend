import logging

import pytest
from dotenv import load_dotenv
from infra import Config, Data

load_dotenv()
config = Config()
data = Data(config)


@pytest.mark.asyncio
async def test_get_data():
    await data.start()
    body = await data.get_object_bytes("01.mp4")
    with open("tmp.mp4", "wb") as f:
        f.write(body)
