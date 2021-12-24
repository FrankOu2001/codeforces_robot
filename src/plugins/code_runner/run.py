import re
import requests


codeType = {
    'py': ['python', 'py'],
    'cpp': ['cpp', 'cpp'],
    'java': ['java', 'java'],
    'js': ['javascript', 'js'],
    'ts': ['typescript', 'ts'],
    'c': ['c', 'c'],
    'c#': ['csharp', 'cs'],
    'go': ['go', 'go'],
    'asm': ['assembly', 'asm'],
    'rust': ['rust', 'rust'],
    'lua': ['lua', 'lua']
}


async def run(text):
    text = text.replace('&amp;', '&').replace('&#91;', '[').replace('&#93;', ']')
    try:
        code_type = \
        re.findall(r'(py|java|cpp|js|ts|c#|c|go|asm|rust|lua)(\n|\r)(((?:.|\n)+)(---\n|---\r))?((?:.|\n)+)', text)[0]
    except:
        return "格式出错或不支持该语言\n" + text

    # print(code_type)
    lang, stdin, code = code_type[0], code_type[3], code_type[5]
    headers = {
        "Authorization": "Token d913f0b5-02d3-4cf8-b6cd-e56c058c5bf8",
        "content-type": "application/"
    }
    dataJson = {
        "files": [
            {
                "name": f"main.{codeType[lang][1]}",
                "content": code
            }
        ],
        "stdin": stdin,
        "command": ""
    }
    res = requests.post(url=f'https://glot.io/run/{codeType[lang][0]}?version=latest', headers=headers, json=dataJson)
    if res.status_code == 200:
        if res.json()['stdout'] != "":
            if len(repr(res.json()['stdout'])) < 500:
                return res.json()['stdout']
            else:
                return "返回字符过长!"
        else:
            if len(repr(res.json()['stderr'])) < 500:
                return res.json()['stderr']
            else:
                return "报错报的太多辣!"


if __name__ == '__main__':
    str = (run('py\nfldpm \n---\nstr=input()\nprint(str)'))
    print(str)
