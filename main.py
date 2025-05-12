import logging

from quart import Quart
from quart_cors import cors
from router import entity_bp, file_bp, relation_bp, server

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
    datefmt="%m-%d %H:%M:%S"
)


# 初始化app服务
app = Quart(__name__)
app = cors(app)
app.register_blueprint(entity_bp)
app.register_blueprint(file_bp)
app.register_blueprint(relation_bp)

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
