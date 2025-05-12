from quart import request, Blueprint
from common import init_dataclass_from_dict, EntityRelation
from router.common import server, success, err

relation_bp = Blueprint('relation', __name__, url_prefix='/api/v1/relation')

@relation_bp.route('/', methods=['POST'])
async def relation_add():
    """添加联系"""
    data = await request.get_json()
    try:
        info = init_dataclass_from_dict(EntityRelation, data)
        await server.api.entity.add_relation(info)
        return success()
    except Exception as e:
        return err(e)

@relation_bp.route('/<path:entity_id>/target', methods=['GET'])
async def relation_get_target(entity_id):
    """获取某个实体的所有目标节点"""
    try:
        data = await server.api.entity.get_relation_target(entity_id)
        return success(data)
    except Exception as e:
        return err(e)

@relation_bp.route('/', methods=['GET'])
async def relation_get_all():
    """获取所有联系"""
    relation_type = request.args.get('relation_type')
    if relation_type and relation_type.isdigit():
        relation_type = int(relation_type)
    else:
        relation_type = None
    try:
        data = await server.api.entity.get_all_relation(relation_type)
        return success(data)
    except Exception as e:
        return err(e)