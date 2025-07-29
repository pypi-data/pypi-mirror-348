#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : img_utils.py
# @Author: Richard Chiming Xu
# @Date  : 2024/6/17
# @Desc  : 图片相关的工具类
import base64


def img2base64(img_path: str) -> str:
    '''
    读取图片成base64
    :param img_path: 图片地址
    :return:
    '''
    imagedata = open(img_path, 'rb').read()
    return str(base64.b64encode(imagedata), 'utf-8')
