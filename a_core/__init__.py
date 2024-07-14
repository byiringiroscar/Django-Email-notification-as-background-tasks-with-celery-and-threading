from .celery import celery_app

# this is for making sure that celery open at the first when we open the app
__all__ = ('celery_app',)