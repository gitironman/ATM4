# -*- encoding: utf-8 -*-
# __author: iamironman
# @file: commom.py
# @time: 2019年01月08日
# @email: 875674794@qq.com

import os
import time
import logging.config
from conf import settings
from core import src
import json


def login_auth(func):
    def inner(*args, **kwargs):
        if settings.flag:
            ret = func(*args, **kwargs)
            return ret
        else:
            src.login()

    return inner


def checkname(name):
    if os.path.isfile(settings.db_path + name + '.json'):
        return True
    else:
        return False


def checkpwd(name, password):
    f1 = open(settings.db_path + name + '.json', encoding='utf-8')
    f1_dict = json.load(f1)
    f1.close()
    if password == f1_dict['password']:
        return True
    else:
        return False


def loginin(name):
    settings.flag = True
    settings.flag1 = False
    f1 = open(settings.db_path + name + '.json', encoding='utf-8')
    f1_dict = json.load(f1)
    f1_dict['status'] = 1
    f1.close()
    f2 = open(settings.db_path + name + '.json', encoding='utf-8', mode='w')
    json.dump(f1_dict, f2, ensure_ascii=False)
    f2.close()
    get_logger('loginin').info('{}登录认证成功！'.format(name))


# 流水：只要账户出现钱的操作：购物，转账，存钱等，就记录到一个文件中。
def billflow_tofile(money, ways, name=settings.name):
    get_logger('billflow_tofile').info('{}新建流水记录：{}{}元'.format(name, ways, money))
    f1 = open(settings.db_path + name + '.json', encoding='utf-8')
    check_dict = json.load(f1)
    f1.close()
    dic1 = {'time': time.strftime("%Y-%m-%d %X"), 'money': money, 'ways': ways, 'balance': check_dict['money']}
    with open(settings.db_path + name + '_billflow.json', encoding='utf-8', mode='a') as f1:
        f1.write(json.dumps(dic1) + '\n')


def get_logger(task_id):
    logging.config.dictConfig(settings.LOGGING_DIC)  # 导入上面定义的logging配置
    logger = logging.getLogger(task_id)  # 生成一个log实例 这个logger对象是通过自己个性化配置的logger对象
    return logger


def check_date(year, month, day):
    try:
        date = '{} {} {}'.format(year, month, day)
        stptime = time.strptime(date, '%Y %m %d')
        stamptime = time.mktime(stptime)
        if stamptime < time.time():
            return True
        else:
            return False
    except ValueError:
        return ValueError
    except OverflowError:
        return True
