# Codeforces_bot

## 功能

### 查询codeforces个人信息

### 查询比赛信息

目前支持的比赛网站:
```angular2html
Codeforces
AtCoder
NowCoder(隐藏了高校系列赛，目前只能查询牛客系列赛)
```

### 赛前通知

### 查询天气

### 定时发送出勤情况

### 查询钉钉群中缺勤人员和请假人员的名单

### 查询钉钉群中某个月内所有人的出勤统计

### 在线运行代码
```
run (py|java|cpp|js|ts|c#|c|go|asm|rust|lua) 
可选的标准输入
---
代码
```

![](img/code-runner.png)

### 查询机器人运行状态

戳一戳机器人或 发送 `状态`

## 部署

首先需要安装`go-cqhttp` [Link](https://github.com/Mrs4s/go-cqhttp/releases)

关于`go-cqhttp`和本bot的通信配置，请查阅[CQHTTP 协议使用指南](https://v2.nonebot.dev/guide/cqhttp-guide.html)

之后运行`pip install -r requirements.txt`安装环境变量

对于钉钉模块，使用前请配置好`src/dingtalk_services/__init__.py`文件中, `DingTalk_Client`的`__get_token`中`app_key`与`app_secret`两个个参数

最后运行`go-cqhttp`和`bot.py`文件

## 配置机器人

> 在配置机器人前，希望你能够熟悉`nonebot2`框架，如果你对此不熟悉，请先查阅[nonebot2](https://v2.nonebot.dev/guide/) 教程
>
> 关于`go-cqhttp`和机器人的通信配置，请查阅[CQHTTP 协议使用指南](https://v2.nonebot.dev/guide/cqhttp-guide.html)

### 基本配置

对于机器人的昵称、命令前缀、超级用户等配置，都存储在[.env.prod](.env.prod)中

具体的配置请参考上方给予的`nonebot2教程`

### 比赛爬取

各个网站比赛信息爬取的脚本都保存在[src/contests_services/](src/contests_services)文件夹中，以比赛网站的名称命名

如果你想增加爬取其他网站的脚本，为了减少对整个项目的改动，建议你将爬取后的信息用以下格式保存或获取

```python3
    [{
        'name': name,
        'link': link,
        # 'holder': holder,
        # 'register_time': register_time,
        'contest_time': contest_time
    },
    {
        #....
    }]
```

在本项目中，爬取比赛时没有保留`holder`和`register_time`的信息，如果你对这两个信息有需求，建议参考上面的样式保存

如果你想要一个获取比赛信息的实例，建议参考[nowcoder.py](src/contests_services/nowcoder.py)

### 钉钉API的适配

> 如果你对钉钉相关的API不太熟悉，建议查阅[钉钉开发文档](https://open.dingtalk.com/document/)

本项目中，钉钉部分的功能全是通过发送`HTTP`请求实现的，在使用相关功能时，请务必确保你对相关的接口拥有调用的权限

### 接入钉钉API

请在`src/dingtalk_services/__init__`[.py](src/dingtalk_services/__init__.py)填写`app_key`和`app_secret`

### 调用实现好的服务

本机器人已经实现好了对钉钉API的调用，这些模块都存储在[src/dingtalk_services](src/dingtalk_services)下

`__init__.py`中，可以获取`AccessToken`，详情请看文件

`user.py`可以获取根部门的用户信息，具体可以获取的信息请查看`钉钉开发文档`，在本项目中，只是获取了`userid`和用户名，具体请看[源文件](src/dingtalk_services/user.py)

`checker.py`中构造了`permission_checker()`方法，用于检查权限，确保命令只能在指定的群内，由群主、管理员或开发人员调用，防止命令滥用导致钉钉接口达到调用频率上限(40次每秒)

`absence.py`可以获取缺勤人员，所有缺勤人员的信息将以`(name, userid)`的形式返回一个列表。需要注意的是，请假人员也是在缺勤范围内的

`vatation.py`可以从缺勤人员中，获取请假人员的名单。返回形式同`absence.py`

`report.py`可以获取集训队所有成员的出勤次数和旷工次数，结果按照旷工次数从大到小排序，返回`(姓名, 旷工次数, 出勤天数)`形式的列表。

使用者可以使用或二次开发这些服务, 来修改或增加本项目中的插件功能

## TODO
- [ ] 将Codeforces比赛获取方式改为从API获取
- [ ] 将项目部署在Docker中
- [ ] 向V2分支尽可能的靠拢(已经靠拢一些了吧)

