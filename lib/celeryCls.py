from celery import Celery
from lib.settings import application

celery_app = Celery(
    application,
    backend='db+postgresql://castom:castom@127.0.0.1:5432/advertisement',
    broker='redis://localhost:6379/4'
)
celery_app.conf.update(application.config)


class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        with application.app_context():
            return self.run(*args, **kwargs)


celery_app.Task = ContextTask