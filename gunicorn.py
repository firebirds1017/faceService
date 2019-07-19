import gevent.monkey
gevent.monkey.patch_all()

debug = True
bind = ":8081"
workers = 2
max_requests = 5000
max_requests_jitter = 2
timeout = 70
graceful_timeout = 30
limit_request_line = 8190
limit_request_fields = 200
limit_request_fields_size = 8190
pidfile = "gunicorn.pid"
pythonpath = "/home/firebird/pythonProject/flasky/venv/bin"
#accesslog = "gunicorn_access.log"
#errorlog = "gunicorn_error.log"
loglevel = "debug"
#access_log_format = '%(h)s %(t)s %(l)s %(u)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
daemon = False
# raw_env = "CONFIG_ENV=uat"
raw_env = "FLASK_ENV=development"
capture_output = True
worker_class = 'gunicorn.workers.ggevent.GeventWorker'

x_forwarded_for_header = 'X-FORWARDED-FOR'

logconfig_dict = {
    'version':1,
    'disable_existing_loggers': False,
    'loggers':{
        "gunicorn.error": {
            "level": "DEBUG",  # 打日志的等级可以换的，下面的同理
            "handlers": ["error_file"],  # 对应下面的键
            "propagate": 1,
            "qualname": "gunicorn.error"
        },

        "gunicorn.access": {
            "level": "DEBUG",
            "handlers": ["access_file"],
            "propagate": 0,
            "qualname": "gunicorn.access"
        }
    },
    'handlers': {
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024*1024*1024,  # 打日志的大小，我这种写法是1个G
            "backupCount": 1,  # 备份多少份，经过测试，最少也要写1，不然控制不住大小
            "formatter": "generic",  # 对应下面的键
            # 'mode': 'w+',
            "filename": "logs/gunicorn.error.log"  # 打日志的路径
        },
        "access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024*1024*1024,
            "backupCount": 1,
            "formatter": "generic",
            "filename": "logs/gunicorn.access.log",
        }
    },
    'formatters':{
        "generic": {
            "format": "'[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s'",  # 打日志的格式
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",  # 时间显示方法
            "class": "logging.Formatter"
        },
        "access": {
            "format": "'[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s'",
            "class": "logging.Formatter"
        }
    }
}