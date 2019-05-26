import os
import time

flag = False
flag1 = True
name = None

sftime = str(time.strftime("%Y{}%m{}%d{}%H{}").format('年', '月', '日', '时'))
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
db_path = BASE_DIR + '/db/'
log_path = BASE_DIR + '/log/'
register_path = os.path.join(db_path, 'register')
product_path = os.path.join(db_path, 'product_info')
logfile_boss = os.path.join(log_path, ('boss_' + sftime + '.log'))
logfile_name = os.path.join(log_path, ('staff_' + sftime + '.log'))

# 标准版 格式
standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                  '[%(levelname)s][%(message)s]'  # 其中name为getlogger指定的名字

# 简单版 格式
simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'

# boss版格式
id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'
# 定义日志输出格式 结束

# log配置字典
LOGGING_DIC = {
    'version': 1,  # 版本
    'disable_existing_loggers': False,  # 可否重复使用之前的logger对象
    'formatters': {
        'standard': {
            'format': standard_format
        },
        'simple': {
            'format': simple_format
        },
        'boss_formatter': {
            'format': id_simple_format
        },
    },
    'filters': {},  # 删选、过滤 目前用不到
    'handlers': {
        # 打印到终端（屏幕）的日志
        'stream': {
            'level': 50,  # DEBUG的时候再改成10
            'class': 'logging.StreamHandler',  # 打印到屏幕
            'formatter': 'simple'  # 简洁
        },
        # 打印到文件的日志,收集info及以上的日志  文件句柄
        'file': {
            'level': 10,
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'standard',  # 标准
            'filename': logfile_name,  # 日志文件名
            'maxBytes': 1024 ** 5,  # 日志大小
            'backupCount': 5,  # 轮转文件数
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
        'boss_file': {
            'level': 20,
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
            'formatter': 'boss_formatter',  # boss 超简洁
            'filename': logfile_boss,  # 日志文件名
            'maxBytes': 1024 ** 3,  # 日志大小
            'backupCount': 5,  # 轮转文件数
            'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
        },
    },
    'loggers': {
        # logging.getLogger(__name__)拿到的logger配置
        '': {
            'handlers': ['stream', 'file', 'boss_file'],  # 这里把上面定义的handler都加上，即log数据既写入文件又打印到屏幕
            'level': 10,  # 总级别
            'propagate': True,  # 向上（更高level的logger）传递
        },
    },
}  # 字典中第一层的所有key都是固定不可变的。
