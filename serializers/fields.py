import logging
from typing import Any
from django.conf import settings

from django.core.cache import cache
from rest_framework.fields import Field
from minio.error import MinioException
from utils import generate_minio_client


MINO_URL_TTL = getattr(settings, 'MINO_URL_TTL', 60)


class MinioField(Field):
    '''
        Simple Minio Field to generate urls for objects, given their object_name in an Minio server.

        :param bucket: The bucket your objects should be in. :class:`str`
    '''

    def __init__(self, bucket: str, *args):
        self.bucket = bucket
        super().__init__(*args)

    def to_internal_value(self, data: Any) -> str:
        return data

    def to_representation(self, value: str) -> str:
        minio = generate_minio_client()
        try:
            return minio.presigned_get_object(bucket_name=self.bucket,
                                              object_name=value)
        except Exception as exc:
            logging.error(exc)
            return value


class CachedMinioField(MinioField):
    '''
        CachedMinioField is a MinioField that caches the result of the presigned_get_object call.

        :param bucket: The bucket your objects should be in. :class:`str`

    '''

    def to_internal_value(self, data):
        return super().to_internal_value(data)

    def to_representation(self, value: str) -> str:
        '''
            Generate a presigned url for the object, and cache it.
            :param value: The object name. :class:`str`
            :return: The presigned url. :class:`str`
        '''

        key = f'{self.bucket}_{value}'
        res = cache.get(key)
        if res:
            return res
        minio = generate_minio_client()
        try:
            url = minio.presigned_get_object(bucket_name=self.bucket,
                                             object_name=value)
            cache.set(key, url, MINO_URL_TTL)
            return url
        except Exception as exc:
            logging.error(exc)
            return value
