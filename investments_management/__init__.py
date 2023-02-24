# loading Celery app when starting Django

from .celery import app as celery_app

__all__ = ("celery_app",)
