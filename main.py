import nonebot
from nonebot.adapters.cqhttp import Bot
"""
@author: Frank_Ou
@time: 2021-11-29 13:10
@function: basic settings of codeforces robot
"""

nonebot.init(apscheduler_autostart=True)
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", Bot)

# robot configuration
config = driver.config
config.port = 8080
config.host = "127.0.0.1"
config.debug = False
config.superusers = {"1204630052", "523669596"}
config.nickname = {'伞兵', 'cf', '傻逼', '/'}
config.command_start = {'.', '。', ''}

nonebot.load_builtin_plugins()
nonebot.load_plugins("plugins/")

app = nonebot.get_asgi()

if __name__ == '__main__':
    nonebot.run()
