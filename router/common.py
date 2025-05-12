import logging

from quart import jsonify
import traceback
from dotenv import load_dotenv
from core import CoreService

load_dotenv()
# 初始化sdk并注册服务
server = CoreService()

def success(data: dict = None):
    return jsonify(code=0, data=data, msg='success')

def err(_err: Exception):
    logging.info(f"trace back {traceback.format_exc()}")
    return jsonify(code=-1, data=None, msg=str(_err))
