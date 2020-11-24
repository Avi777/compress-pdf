from celery import Celery

from algorithm import *

app = Celery(__name__, backend="rpc://", broker="redis://localhost:6379/")


@app.task
def integrate(*args, **kwargs):
    try:
        return compress(*args, **kwargs)
    except Exception:
        return
