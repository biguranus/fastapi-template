# -*- coding:utf-8 -*-
import functools

from werkzeug.local import LocalProxy
import oss2
from oss2.exceptions import ServerError, RequestError
from oss2.resumable import ResumableStore, resumable_upload

from src.libs.utils import retry as _retry
from src.config import (
    ALIYUN_ACCESS_KEY_ID,
    ALIYUN_ACCESS_KEY_SECRET,
    ALIYUN_OSS_ENDPOINT,
    ALIYUN_OSS_PUBLIC_ENDPOINT,
    ALIYUN_OSS_BUCKET,
    ALIYUN_OSS_KEY_PREFIX,
    USE_INTERNAL_ENDPOINT,
)


def prefix_key(key, prefix=ALIYUN_OSS_KEY_PREFIX):
    if prefix:
        if key[: len(prefix)] != prefix:
            key = f"{prefix}/{key}"
    return key


def _get_bucket(endpoint=ALIYUN_OSS_ENDPOINT, bucket_name=ALIYUN_OSS_BUCKET):
    auth = oss2.Auth(ALIYUN_ACCESS_KEY_ID, ALIYUN_ACCESS_KEY_SECRET)
    _bucket = oss2.Bucket(auth, endpoint, bucket_name)
    return _bucket


class OSSStore:
    def __init__(self, bucket, public_bucket, key_prefix=ALIYUN_OSS_KEY_PREFIX):
        self.bucket = bucket if USE_INTERNAL_ENDPOINT else public_bucket
        self.public_bucket = public_bucket
        self.key_prefix = key_prefix

    def clean_key(self, key):
        key_prefix = self.key_prefix
        return prefix_key(key, key_prefix)

    def read(self, key, times=1, wait=0):
        cleaned_key = self.clean_key(key)
        obj = self.retry(
            lambda: self.bucket.get_object(cleaned_key), times=times, wait=wait
        )
        return obj.read()

    def write(self, key, content, times=1, wait=0):
        cleaned_key = self.clean_key(key)
        return self.retry(
            lambda: self.bucket.put_object(cleaned_key, content), times=times, wait=wait
        )

    def upload_file(self, key, filename, times=1, wait=0):
        cleaned_key = self.clean_key(key)
        store = ResumableStore()
        result = self.retry(
            lambda: resumable_upload(self.bucket, cleaned_key, filename, store),
            times=times,
            wait=wait,
        )
        return result

    def exists(self, key, times=1, wait=0):
        cleaned_key = self.clean_key(key)
        return self.retry(
            lambda: self.bucket.object_exists(cleaned_key), times=times, wait=wait
        )

    def delete(self, key):
        cleaned_key = self.clean_key(key)
        return self.bucket.delete_object(cleaned_key)

    def retry(self, func, times=1, wait=0):
        do_retry = functools.partial(
            _retry, on_error=(ServerError, RequestError), times=times, wait=wait
        )
        return do_retry(func)

    def sign_url(self, key, timeout=600):
        cleaned_key = self.clean_key(key)
        return self.public_bucket.sign_url("GET", cleaned_key, timeout)


def get_aliyun_oss() -> OSSStore:
    bucket = LocalProxy(_get_bucket)
    public_bucket = LocalProxy(
        lambda: _get_bucket(
            endpoint=ALIYUN_OSS_PUBLIC_ENDPOINT, bucket_name=ALIYUN_OSS_BUCKET
        )
    )
    return LocalProxy(functools.partial(OSSStore, bucket, public_bucket))


oss_store: OSSStore = get_aliyun_oss()
