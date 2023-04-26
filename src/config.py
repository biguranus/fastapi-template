# -*- coding:utf-8 -*-
import os

env = os.getenv

ENVIRONMENT = env("ENVIRONMENT", "dev")
DEBUG = env("DEBUG", "true").lower() == "true"

# MySQL
SQLALCHEMY_DATABASE_URI = env("SQLALCHEMY_DATABASE_URI", "sqlite://")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_size": int(env("pool_size", 200)),
    "pool_recycle": int(env("pool_recycle", 3600)),
    "pool_timeout": int(env("pool_timeout", 180)),
}

# Redis
REDIS_URI = env("REDIS_URI", "/tmp/redis.db")

# aliyun account
ALIYUN_ACCESS_KEY_ID = env("ALIYUN_ACCESS_KEY_ID")
ALIYUN_ACCESS_KEY_SECRET = env("ALIYUN_ACCESS_KEY_SECRET")

ALIYUN_OSS_ENDPOINT = env("ALIYUN_OSS_POINT")
ALIYUN_OSS_PUBLIC_ENDPOINT = env("ALIYUN_OSS_PUBLIC_POINT")
ALIYUN_OSS_BUCKET = env("ALIYUN_OSS_BUCKET", "")
ALIYUN_OSS_KEY_PREFIX = env("ALIYUN_OSS_KEY_PREFIX", "")

ALIYUN_IOT_REGION_ID = env("ALIYUN_IOT_REGION_ID", "cn-shenzhen")

# RocketMQ
MQ_HTTP_ENDPOINT = env("MQ_HTTP_ENDPOINT")
MQ_INSTANCE_ID = env("MQ_INSTANCE_ID")
MQ_BATCH = int(env("MQ_BATCH", 1))
MQ_WAIT_SECONDS = int(env("MQ_WAIT_SECONDS", 15))

MQ_TOPIC_NAME = env("MQ_TOPIC_NAME")
MQ_GROUP_ID = env("MQ_GROUP_ID")
DELAY_TIME = int(env("DELAY_TIME", 5))  # 单位: 分钟
