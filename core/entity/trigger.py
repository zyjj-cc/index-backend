from common import EntityInfo, EntityType


class Trigger:
    async def entity_trigger(self, entity: EntityInfo, _input: dict) -> dict:
        match EntityType(entity.entity_type):
            case EntityType.Code:
                return await self.code_trigger(entity.data, _input)
            case _:
                return {}

    @staticmethod
    async def code_trigger(info: dict, _input: dict) -> dict:
        _inputs = [_input[unique] if unique in _input else None for unique in info["inputs"]]
        tmp = {
            "base": 1
        }
        exec(info.get('code', ''), tmp)
        out = await tmp['handle'](*_inputs)
        if not isinstance(out, tuple):
            out = (out,)

        return {unique: out[idx] for idx, unique in enumerate(info["outputs"])}
