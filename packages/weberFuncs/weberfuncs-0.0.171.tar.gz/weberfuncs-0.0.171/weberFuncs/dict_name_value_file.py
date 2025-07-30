#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__createTime__ = "2025/5/8 09:47"
__author__ = "WeiYanfeng"
__email__ = "weber.juche@gmail.com"
__version__ = "0.0.1"

~~~~~~~~~~~~~~~~~~~~~~~~
程序单元功能描述

封装函数，读写 name=value # remarks 格式配置文件
- dict_load_name_value 读取参数到dict
- dict_save_name_value 保存dict参数到文件

~~~~~~~~~~~~~~~~~~~~~~~~
# 依赖包 Package required
# pip install weberFuncs

"""
import sys
from .WyfPublicFuncs import PrintTimeMsg
from .PrettyPrint import PrettyPrintStr
# from weberFuncs import PrintTimeMsg, PrettyPrintStr


def dict_load_name_value(sFullFN):
    # 从 name=value # remarks 格式文本读取配置参数
    dictNV = {}
    try:
        with open(sFullFN, 'r', encoding='utf8') as f:
            for sLine in f:
                sLine = sLine.strip()
                if not sLine or sLine.startswith('#') or ('=' not in sLine):
                    # 空串没有等号，则是不正常的key=value配置，直接忽略
                    continue
                sKey, cSep, sValue = sLine.partition('=')
                if '#' in sValue:  # 剔除行内注释
                    sV, cSep, sC = sValue.partition('#')
                    sValue = sV
                sKey = sKey.strip()
                sValue = sValue.strip('\'\" \t')  # 删除引号及空白
                if sKey:
                    if '%' in sValue:
                        sValue = sValue.replace('%23', '#')
                        sValue = sValue.replace('%0A', '\n')
                        sValue = sValue.replace('%0D', '\r')
                        sValue = sValue.replace('%25', '%')
                    if '%3D' in sKey:
                        sKey = sKey.replace('%3D', '=')
                    dictNV[sKey] = sValue
    except Exception as e:
        PrintTimeMsg(f'dict_load_name_value({sFullFN}).e={repr(e)}=')
    # PrintTimeMsg(f'dict_load_name_value.dictNV={PrettyPrintStr(dictNV)}=')
    # PrintTimeMsg(f'dict_load_name_value.len(dictNV)={len(dictNV)}=')
    return dictNV


def dict_save_name_value(sFullFN, dictNV):
    # 将dictNV内容按 name=value # remarks 格式保存到文件
    with open(sFullFN, 'w', encoding='utf8') as f:
        for sKey, sValue in dictNV.items():
            if isinstance(sKey, str) and ('=' in sKey):
                sKey = sKey.replace('=', '%3D')  # = hex
            if isinstance(sValue, str):
                if '%' in sValue:
                    sValue = sValue.replace('%', '%25')  # hex
                if '\n' in sValue:
                    sValue = sValue.replace('\n', '%0A')  # hex
                if '\r' in sValue:
                    sValue = sValue.replace('\r', '%0D')  # hex
                if '#' in sValue:
                    sValue = sValue.replace('#', '%23')  # hex
            f.write(f'{sKey}={sValue}\n')
    # PrintTimeMsg(f'dict_save_name_value.len(dictNV)={len(dictNV)}=')


def main():
    sFN = r'E:\tmp\t1.env'
    dictNV = {'A=': 'a\nb', 'TestEN': 'english%', 'TestCN': '测试#汉字', '0': 'zero'}
    dict_save_name_value(sFN, dictNV)
    dict_load_name_value(sFN)


# --------------------------------------
if __name__ == '__main__':
    main()
