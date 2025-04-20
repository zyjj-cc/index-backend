import logging

import pytest
from dotenv import load_dotenv
from infra import Config, Data

load_dotenv()
config = Config()
data = Data(config)


@pytest.mark.asyncio
async def test_get_data():
    await data.get_object("123")
