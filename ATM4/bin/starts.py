# !/usr/bin/python
# -*- encoding: utf-8 -*-
# __author: iamironman
# @file: starts.py
# @time: 2019年01月10日
# @email: 875674794@qq.com

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

if __name__ == '__main__':
    from core import src

    src.run()
