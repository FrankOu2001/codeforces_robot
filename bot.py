#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
"""
@author: Frank_Ou
@time: 2021-11-29 13:10
@function: basic settings of codeforces robot
"""

nonebot.init()
app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)

# robot configuration
nonebot.load_from_toml("pyproject.toml")


if __name__ == '__main__':
    nonebot.run()
