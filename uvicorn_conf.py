# -*- coding:utf-8 -*-
import os

host = "0.0.0.0"
port = 8080

workers = os.cpu_count() * 2 + 1
