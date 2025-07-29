# -*- coding: utf-8 -*-

# Copyright (c) 2025, lujiawan <lu_jiawan@163.com>


import os
import sys
import xlrd
import json
import copy
import logging


# log
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s  %(filename)s:%(lineno)d %(message)s')
logger = logging.getLogger('xlconv')

def getDataSet(xlsx_book):
    """
    :func 获取数据集信息,即将要转换的数据
    :param xlsx_book: excel工作簿对象
    :return:
    """
    cases_set = dict()
    id_key, json_sheet= "json_id", "json_sheet"
    sheet = xlsx_book.sheet_by_name("Json集")
    rows = sheet.nrows
    cols = sheet.ncols
    if rows <= 0:
        return [None,cases_set]
    for c in range(0, cols):
        if sheet.cell_value(0, c) == id_key:
            clo_id = c
        elif sheet.cell_value(0, c) == json_sheet:
            clo_sheet = c

    for r in range(1, rows):
        id = sheet.cell_value(r, clo_id)
        value = sheet.cell_value(r, clo_sheet)
        cases_set[id] = value
    return [id_key,cases_set]

def xlParser(xlsx_book,sheet_name,id_key,id_value,data_tag='{}',id_num_f=None):
    """
    :function 通过唯一关键字的值将excel造数串联成字典
    :param xlsx_book: xlsx/xls对象,工作薄
    :param sheet_name: sheet名称,待转数据的起始页面名称
    :param id_key: 数据唯一标识字段名称
    :param id_value: 数据唯一标识,串联具体json的关键字值
    :param data_tag: 数据标识，对象{}，数组[]
    :return root_array/root_obj: 返回本层的字典数据
    """

    root_array = []
    root_obj = dict()
    sheet = xlsx_book.sheet_by_name(sheet_name)
    sheet_names = xlsx_book.sheet_names()
    cols = sheet.ncols
    rows = sheet.nrows

    id_key_col = None
    id_num_f_col = None
    id_num_col = None
    # 获取数据构造关键字参数列的索引值
    for c in range(0, cols):
        if sheet.cell_value(0, c) == f"{id_key}":
            id_key_col = c
        elif sheet.cell_value(0, c) == f"父序号":
            id_num_f_col = c
        elif sheet.cell_value(0, c) == f"序号":
            id_num_col = c
    if id_key_col is None:
        raise ValueError(f"'{sheet_name}'没有'{id_key}'列,请检查.")

    # 遍历获取数据
    r_cnt = 0
    for r in range(0,rows):
        # 判断关键参数值是否与该行相等
        if sheet.cell_value(r, id_key_col) == str(id_value):
            # 判断是否传入父序号
            if id_num_f is not None:
                # 判断传入的父序号是否与该行的父序号相等
                if sheet.cell_value(r, id_num_f_col) != id_num_f:
                    # 该行数据不满足，跳过
                    continue
            if data_tag == '{}' and r_cnt == 1:
                raise ValueError(f"页面'{sheet_name}'的数据，期望是对象类型，但实际是数组类型，请检查!")
            # 循环取该行的所有字段的值
            for c in range(id_key_col + 1, cols):
                # 检查单元格是否合法
                if sheet.cell_type(r, c) in [3,4]:
                    err_r = r + 1
                    err_c = c + 1
                    raise TypeError(f"页面'{sheet_name}'的单元格({err_r},{err_c})数据转换可能失真，请设置成文本类型!")
                # 获取value
                i_value = sheet.cell_value(r, c)
                i_v = str(i_value)
                # 如果单元格的值为空，直接赋空
                if i_v == "":
                    i_value = None
                # 如果为空数组
                elif i_v == "[null]":
                    root_obj = []
                    break
                # 如果为空json
                elif i_v == "{null}":
                    root_obj = {}
                    break
                # 判断是否为数组[]或对象{}，若是，则下钻
                elif ((i_v[0] == '[' and i_v[-1] == ']') or (i_v[0] == '{' and i_v[-1] == '}')) and ":" not in i_v and len(i_v) >2:
                    i_value = i_v[1:-1]
                    # 判断sheet页是否存在
                    if i_value in sheet_names: 
                        if id_num_col is None:
                            id_num = None
                        else:
                            id_num = sheet.cell_value(r, id_num_col)
                        # 开始递归下钻
                        i_value=xlParser(xlsx_book,i_value,id_key,id_value,i_v[0]+i_v[-1],id_num)
                    else:
                        i_value=i_v
                # 正常取值的情况
                else:
                    # 如果value的首尾为""，则强制转换为字符串
                    if i_v[0] == "\"" and i_v[-1] == "\"":
                        if "{" in i_v and "}" in i_v and ":" in i_v:
                            i_v = i_v[1:-1]
                            i_value = i_v.replace("\"","\\\"")
                        else:
                            i_value = i_v[1:-1]
                    # 如果value是json，则转换成字典
                    elif ("{" in i_v and ":" in i_v and "}" in i_v ) or i_v == '[]' or i_v == '{}':
                        i_value = dict()
                        try:
                            i_value = json.loads(i_v)
                        except Exception:
                            i_value = i_v
                    # 如果value是int，则转换成int
                    elif i_v.isdigit() is True:
                            i_value = int(i_v)
                    # 如果value是float，则转换成float
                    elif is_float(i_v):
                            i_value = float(i_v)
                    else:
                         pass
                # 获取key
                i_key = sheet.cell_value(0, c)
                # 如果单元格key包括".", 需要将key转换为层级关系
                if "." in i_key:
                    tmp_obj1 = dict()
                    tmp_obj2 = dict()
                    arr = []
                    arr = i_key.split(".")
                    i = len(arr) - 1
                    tmp_obj1 = root_obj
                    j = 0
                    # 通过循环，找到不同在j层，将变量tmp_obj1指向j层
                    while j <= i and tmp_obj1 != "" and arr[j] in tmp_obj1:
                        tmp_obj1 = tmp_obj1[arr[j]]
                        j = j + 1
                    # 从叶子节点向上层封装到j层即可
                    for k in range(i,j,-1):
                        if tmp_obj2 == {}:
                            # 封装叶子节点
                            tmp_obj2[arr[k]] = i_value
                        else:
                            # 同一字典赋值，必须用深拷贝
                            tmp_obj2[arr[k]] = copy.deepcopy(tmp_obj2)
                            del tmp_obj2[arr[k+1]]
                    # 将数据填充到j层
                    if i == j:
                        tmp_obj1[arr[j]] = i_value
                    else:
                        tmp_obj1[arr[j]] = copy.deepcopy(tmp_obj2)
                    # 销毁指针变量，进而不影响数据
                    del tmp_obj1
                else:
                    root_obj[i_key] = i_value
            # 判断该sheet页是不是数组类型的数据
            if data_tag == '[]':
                # 追加到数组，必须用深拷贝
                root_array.append(copy.deepcopy(root_obj))
                # 销毁指针变量，进而不影响数据
                del root_obj
                # 重新新建变量
                root_obj = dict()
            r_cnt = r_cnt + 1
    # 组装成json后返回
    if data_tag == '[]':
        return root_array
    elif data_tag == '{}':
        return root_obj
    else:
        return None

def is_float(string):
    """
    :function: 验证是否为浮点数
    :param string: 待验证字符串
    :return: True/False
    """
    try:
        float(string)
        return True
    except ValueError:
        return False
