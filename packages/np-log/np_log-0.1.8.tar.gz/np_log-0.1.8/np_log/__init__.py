# v2版本添加了企业微信机器人和飞书机器人   优化了当name=None的时候，生成日志文件
import os
import sys

from .v2 import setup_logging as log

def setup_logging(name=None, is_logfile=True, console_level="DEBUG", file_level="DEBUG", log_max_days=7, log_max_size=50):
    frame = sys._getframe(1)  # 获取上一级调用的帧信息
    caller_filename = os.path.basename(frame.f_code.co_filename)
    name = os.path.splitext(caller_filename)[0]  # 去掉文件扩展名
    print(name)
    return log(name=name, is_logfile=True, console_level="DEBUG", file_level="DEBUG", log_max_days=7, log_max_size=50)
