import logging
from quart import Quart, jsonify, request
from core import CoreService

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
    datefmt="%m-%d %H:%M:%S"
)

# 初始化sdk并注册服务
server = CoreService()
# 初始化app服务
app = Quart(__name__)

@app.before_serving
async def startup():
    logging.info('[core] server init')
    # 服务启动前，先启动后端服务
    await server.start()

@app.after_serving
async def stop():
    logging.info('[core] server stopping')
    # 需要把服务启动功能添加到后台任务
    await server.stop()
    logging.info("[core] server stopped")

@app.route('/notify', methods=['GET'])
async def notify():
    """
    通知有新任务，后台自动处理
    :return:
    """
    await server.notify()
    return 'ok'

@app.route('/execute', methods=['POST'])
async def invoke():
    """
    直接执行任务并返回任务执行结果
    :return:
    """
    task_info = await request.get_json()
    logging.info(f"[api] execute input {task_info}")
    data = await server.execute_one_task(task_info)
    logging.info(f"[api] execute output {data}")
    return jsonify(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
