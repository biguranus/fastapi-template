# -*- coding:utf-8 -*-
import sys
import configparser
from functools import partial
from subprocess import check_call as _call

from src.config import ENVIRONMENT

call = partial(_call, shell=True)


def main():
    """
    手工 build 镜像临时用这个脚本， python release.py patch
    集成cicd后，本脚本会更新
    """
    part = sys.argv[1]
    call(f"bumpversion --allow-dirty {part}")
    config = configparser.ConfigParser()
    config.read(".bumpversion.cfg")
    version = config.get("bumpversion", "current_version")
    image_name_base = (
        f"registry.cn-shenzhen.aliyuncs.com/gxtech/fastapi-template-{ENVIRONMENT}"
    )
    image_version = f"{image_name_base}:{version}"
    call(f"docker build -t {image_version} .")
    call(f"docker push {image_version}")


if __name__ == "__main__":
    main()
