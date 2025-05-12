from quart import request, Blueprint, Response
from router.common import server, success, err

file_bp = Blueprint('file', __name__, url_prefix='/api/v1/file')


@file_bp.route('/upload', methods=['POST'])
async def file_upload():
    """文件上传"""
    try:
        file = (await request.files).get("file")
        file_key = await server.api.file.add_file(file.filename, file.read())
        return success(file_key)
    except Exception as e:
        return err(e)

@file_bp.route('/<path:file_id>', methods=['GET'])
async def file_get(file_id):
    """获取文件"""
    if not file_id:
        return err(Exception("file_id is empty"))
    try:
        file, data = await server.api.file.get_file(file_id)
        return Response(
            data,
            content_type=file.content_type,
            headers={
                'Content-Disposition': f'attachment; filename={file.name}'
            }
        )
    except Exception as e:
        return err(e)

