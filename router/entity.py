from quart import request, Blueprint
from common import EntityInfo, init_dataclass_from_dict, dataclass_to_dict
from router.common import server, success, err

entity_bp = Blueprint('entity', __name__, url_prefix='/api/v1/entity')


@entity_bp.route('/', methods=['POST'])
async def entity_add():
    """新增实体"""
    data = await request.get_json()
    try:
        info = init_dataclass_from_dict(EntityInfo, data)
        entity_id = await server.api.entity.add_entity(info)
        return success(entity_id)
    except Exception as e:
        return err(e)

@entity_bp.route('/<path:entity_id>', methods=['GET'])
async def entity_get(entity_id):
    """获取实体"""
    try:
        data = await server.api.entity.get_entity(entity_id)
        return success(dataclass_to_dict(data))
    except Exception as e:
        return err(e)

@entity_bp.route('/<path:entity_id>', methods=['PUT'])
async def entity_update(entity_id):
    """实体更新"""
    data = await request.get_json()
    try:
        entity_id = await server.api.entity.update_entity(entity_id, data.get("name"), data.get("data"))
        return success(entity_id)
    except Exception as e:
        return err(e)

@entity_bp.route('/<path:entity_id>', methods=['DELETE'])
async def entity_delete(entity_id):
    """实体删除"""
    try:
        entity_id = await server.api.entity.delete_entity(entity_id)
        return success(entity_id)
    except Exception as e:
        return err(e)

@entity_bp.route('/<path:entity_id>/trigger', methods=['POST'])
async def entity_trigger(entity_id):
    """实体触发"""
    data = await request.get_json()
    try:
        entity_id = await server.api.entity.entity_trigger(entity_id, data)
        return success(entity_id)
    except Exception as e:
        return err(e)
