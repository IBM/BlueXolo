import os
import multiprocessing

logs_path = "/var/www/logs"
log_level = os.environ.get("GUNICORN_LOG_LEVEL", default="INFO")

bind = os.environ.get("GUNICORN_BIND", default=":8000")

logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": log_level,
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": log_level,
            "filename": os.path.join(logs_path, "gunicorn.log")
        }
    },
    "loggers": {
        # Root logger
        "": {
            "handlers": ["console", "file"]
        }
    }
}

workers = int(os.environ.get("GUNICORN_WORKERS", default=multiprocessing.cpu_count() * 2))
threads = int(os.environ.get("GUNICORN_MAX_THREADS", default=1))

reload = bool(int(os.environ.get("GUNICORN_RELOAD", default=1)))