import nonebot
import config
from os import path

"""
@author: Frank_Ou
@time: 2021-11-29 13:10
@function: basic settings of codeforces robot
"""

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(path.join(path.dirname(__file__), 'plugins'),
                         'plugins')
    app = nonebot.get_bot().asgi
    nonebot.run()
