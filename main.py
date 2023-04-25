# -*- coding:utf-8 -*-
import sys

import uvicorn

from src.app import create_app
from src.config import DEBUG


app = create_app()


if __name__ == '__main__':
    port = 8080 if len(sys.argv) <= 1 else int(sys.argv[1])
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=DEBUG)
    # uvicorn.run(app, host="0.0.0.0", port=port, reload=DEBUG)
