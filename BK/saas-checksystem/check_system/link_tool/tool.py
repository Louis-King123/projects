import json


# 递归获取拓扑结构匹配树形
def Make_Recursion_List(data):
    chiled = []
    # 如果存在child
    if data['child']:
        for i in data['child']:
            chiled.append(Make_Recursion_List(i))
        return {
            "id": data['bk_inst_id'],
            "name": data['bk_inst_name'],
            "bk_inst_id": data['bk_inst_id'],
            'bk_obj_id': data['bk_obj_id'],
            'children': chiled,
            # 'expanded': "True"
        }
    else:
        return {
            "id": data['bk_inst_id'],
            "name": data['bk_inst_name'],
            "bk_inst_id": data['bk_inst_id'],
            'bk_obj_id': data['bk_obj_id'],
        }


# 将Json写入文件
def Write_Json_File(filename, data):
    with open(f"{filename}.json", "w", encoding='utf8') as fp:
        fp.write(json.dumps(data, indent=4, ensure_ascii=False))