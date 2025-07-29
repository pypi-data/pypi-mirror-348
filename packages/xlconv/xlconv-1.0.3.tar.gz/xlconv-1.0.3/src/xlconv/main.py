# -*- coding: utf-8 -*-
# Copyright (c) 2025, lujiawan <lu_jiawan@163.com>

import os
import sys
import xlrd
import json
from dicttoxml import dicttoxml
from xlconv.xl_parser import getDataSet,xlParser,logger


def main():
    """
    :function: 从excel获取并转换为需求的格式,再写入到文件
    :param file: xlsx/xls文件名称
    :return: 同一类数据写入同一个目录,唯一标识作为文件名
    """
    # 当前路径
    cur_path=os.getcwd()
    print(cur_path)
    if len(sys.argv) < 3:
        logger.error("缺少参数，e.g. xlconv -json demo.xls")
        sys.exit()
    # 获取转换的模式
    mode=sys.argv[1]
    if not mode in ('-json','-xml'):
        logger.error(f"[{mode}]参数错误, 取值：-json 或 -xml")
        sys.exit()
    # 获取文件
    tmp_file=sys.argv[2]
    # 获取绝对路径
    file_path=os.path.normpath(os.path.join(cur_path,tmp_file))

    try:
        xlsx_book = xlrd.open_workbook(filename=file_path)
    except FileNotFoundError:
        logger.error(f"没有查找到文件! 文件路径: {file_path}.")
        sys.exit()
   
    id_key,cases_set = getDataSet(xlsx_book)
    print(id_key,cases_set)
    if cases_set is None:
        logger.error(f"页面'Json集'无数据")
        # 兼容非标准的格式转换
        sys.exit()
    xl_data = dict()
    for case in cases_set:
        logger.info(f"{cases_set[case]}")
        xl_data[case] = xlParser(xlsx_book,cases_set[case],id_key,case)
        os.makedirs(str(cases_set[case]), exist_ok=True)
        if mode == "-json":
            # 转换为json
            with open(str(cases_set[case]) + "/" + case + ".json", "w", encoding="utf-8") as f:
                f.write(str(json.dumps(xl_data[case],ensure_ascii=False)))  
        elif mode == "-xml":
            # 转换为xml
            with open(str(cases_set[case]) + "/" + case + ".xml", "w", encoding="utf-8") as f:
                f.write(str(dicttoxml(xl_data[case], custom_root=case, attr_type=False)))  


if __name__ == "__main__":
    main()
