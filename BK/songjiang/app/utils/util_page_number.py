# -*- coding: utf-8 -*-
def get_actual_page(count, limit, page):
    """处理分页问题"""
    if count > 0:
        # 处理分页页数不存在的问题
        actual_page = count // limit
        actual_page = actual_page if count % limit == 0 else actual_page + 1
        if actual_page != 0 and actual_page < page:
            page = actual_page
    else:
        page = 1
    return page
