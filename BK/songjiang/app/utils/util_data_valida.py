# -*- coding: utf-8 -*-
def is_data_validation_defeat(key, value, v_type='not_none', param=None):
    """
    数据验证
    """
    print(key)
    try:
        if v_type == 'is_list':
            if value is None or len(value) == 0 or type(value).__name__ != 'list':
                return key + '为数组类型且不能为空'
        if v_type == 'not_none':
            if value is None or value == "":
                return key + '不能为空'
        if v_type == 'not_in':
            if value not in param:
                return key + '取值范围不正确，请检查'
        if v_type == 'is_int':
            if value is None or type(value).__name__ != 'int':
                return key + '为数字类型且不能为空'
        return False
    except Exception as e:
        return "数据类型不匹配确请检查！"


def batch_verification(configs):
    """
    根据数据验证设置属性
    configs: [{"key":"aa","value":123,"v_type":"ont_in","param":[1,2]}]
    """
    for item in configs:
        m_key = item.get("key")
        m_value = item.get("value")
        vd_res = is_data_validation_defeat(m_key, m_value, item.get("v_type"), item.get("param"))
        if vd_res:
            return {"msg": vd_res}
    return {"msg": "success"}


def set_attr_by_data_valid(obj, configs):
    """
    根据数据验证设置属性
    configs: [{"key":"aa","value":123,"v_type":"ont_in","param":[1,2]}]
    """
    for item in configs:
        m_key = item.get("key")
        m_value = item.get("value")
        if m_value is not None:
            vd_res = is_data_validation_defeat(m_key, m_value, item.get("v_type"), item.get("param"))
            if vd_res:
                return {"msg": vd_res, "obj": obj}
            setattr(obj, m_key, m_value)
    return {"msg": "success", "obj": obj}



