# -*- encoding: utf-8 -*-
__author__ = "zhangyz"
__date__ = "2017/11/25 22:05"

import json
import datetime

# 用于将json数据当中的时间格式进行转换
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)