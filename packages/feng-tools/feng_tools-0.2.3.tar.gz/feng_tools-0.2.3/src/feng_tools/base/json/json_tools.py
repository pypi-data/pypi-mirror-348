import json

import pydantic_core
from feng_tools.base.json.Json_encoder import JsonEncoder


def to_json(obj_data) -> str:
    """将Python中的对象转换为JSON中的字符串对象"""
    return json.dumps(obj_data, cls=JsonEncoder, ensure_ascii=False, indent=4)


def to_json_str(obj_data) -> str:
    """将Python中的对象转换为JSON中的字符串对象"""
    return json.dumps(obj_data, indent=4, ensure_ascii=False, default=pydantic_core.to_jsonable_python)


def to_obj(str_data):
    """将JSON中的字符串对象转换为Python中的对象"""
    return json.loads(str_data)


def model_to_dict(model):
    """Model实例转dict"""
    model_dict = dict(model.__dict__)
    del model_dict['_sa_instance_state']
    return model_dict


def model_to_dict2(model):
    """单个对象转dict(效果等同上面的那个)"""
    return {c.name: getattr(model, c.name) for c in model.__table__.columns}


def model_to_json(model) -> str:
    """model或model集合转换为json字符串"""
    if isinstance(model, list):
        return to_json([model_to_dict2(tmp) for tmp in model])
    else:
        return to_json(model_to_dict(model))
