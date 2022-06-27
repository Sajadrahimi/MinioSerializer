from django.conf import settings
from minio import Minio


MINIO_HOST = getattr(settings, 'MINIO_HOST', None)
MINIO_ACCESS_KEY = getattr(settings, 'MINIO_ACCESS_KEY', None)
MINIO_SECRET_KEY = getattr(settings, 'MINIO_SECRET_KEY', None)
MINIO_USE_SECURE = getattr(settings, 'MINIO_USE_SECURE', True)
MINO_SESSION_TOKEN = getattr(settings, 'MINO_SESSION_TOKEN', None)
MINIO_REGION = getattr(settings, 'MINIO_REGION', None)

assert MINIO_HOST is not None, 'MINIO_HOST is not set in settings.py'
assert MINIO_ACCESS_KEY is not None, 'MINIO_ACCESS_KEY must be defined in settings.py'
assert MINIO_SECRET_KEY is not None, 'MINIO_SECRET_KEY must be defined in settings.py'


def generate_minio_client() -> Minio:
    '''
        Generate a Minio client object, using the specified settings in settings.py
        :return: Minio client object :class:`minio.Minio`
    '''
    return Minio(
        MINIO_HOST,
        access_key=MINIO_ACCESS_KEY,
        secret_key=MINIO_SECRET_KEY,
        secure=MINIO_USE_SECURE,
        session_token=MINO_SESSION_TOKEN,
        region=MINIO_REGION,

    )
