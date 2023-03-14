# QQChatGPTBot

基于Mirai与ChatGPT打造的QQ群聊天机器人

# 获取`Key`

[OpenAI](https://platform.openai.com/account/api-keys)点击<kbd>+ Create new secret key</kbd>创建新的`SECRET KEY`，并且记住，因为之后没法找到。

并且，安装`openai`的`python`接口：

```shell
pip install openai
```

# 安装Mirai

&emsp;使用 `Mirai Console Loader`来使用过 `Mirai`，点击 [mcl-2.1.2.zip](https://github.com/iTXTech/mirai-console-loader/releases/download/v2.1.2/mcl-2.1.2.zip)下载，然后解压，然后命令行输入 `./mcl`，不限系统

```shell
cd mcl-2.1.2
# 加载后...
> login <QQ号> <密码> <协议> # 协议包括 MACOS ANDROID_PHONE等，建议用MACOS

# 还可以设置自动登录
> autoLogin <QQ号> <密码>
> setConfig <QQ号> <协议>
```

&emsp;然后在`./config/net.mamoe.mirai-api-http`下新建`setting.yml`，填入以下内容：（如果没有文件夹，记得创建文件夹）

```yaml
adapters:
  - ws  # websocket协议，后面用的这个
  - http # http协议
debug: true
enableVerify: true
verifyKey: yirimirai # verifyKey，后面写代码用
singleMode: false
cacheSize: 4096 
adapterSettings:
  ws:
    host: localhost
    port: 8080
    reservedSyncId: -1
  http:
    host: localhost
    port: 80
    cors: [*]
    unreadQueueMaxSize: 500
```

# 云服务器上设置后台运行

```shell
# 使用screen，安装
apt install screen # Ubuntu
yum install screen # centos

screen -S <name> # 创建名为name的screen，名自己取
./mcl # 运行你的mcl
# Ctrl + A, Ctrl + D之后，screen进入后台
screen -ls # 查看正在运行的screen
screen -r <id> # 打开id为<id>的screen
```

# 安装 Mirai 第三方 API

&emsp;我们将使用一个名为 [Ariadne](https://github.com/GraiaProject/Ariadne) 的第三方库，它是一个异步通信库

安装

```shell
pip install graia-ariadne
```

# 编写代码

## Ariadne代码

```python
from graia.ariadne.app import Ariadne
from graia.ariadne.message.element import Plain
from graia.ariadne.message.parser.base import MentionMe
from graia.ariadne.model import Member
from graia.ariadne.model import Group


app = Ariadne(
    config(
        verify_key="verifyKey",  # 输入
        account=机器人QQ号 
    )
)

# 如果有艾特机器人的消息，那么就进入该函数
@app.broadcast.receiver("GroupMessage", decorators=[MentionMe()])
async def group_message_listener(app_bot: Ariadne, group: Group, chain: MessageChain, src: Source, member: Member):
    input_message = "" # 保存了文本消息
    tmpcontent = chain.content[1:] # 第一个应该是艾特机器人的，所以跳过
    for msg in tmpcontent:
        if msg.type == 'Plain': # 只使用文本消息
            input_message += str(msg)
	
    print(group.id) # 群qq号
    print(member.id) # 发送人qq号
    # 其中quote是表示回复的方式发送消息
    await app_bot.send_message(group, MessageChain([Plain("hello world")]), quote=src)


app.launch_blocking()
```

## OpenAi代码

```python
import openai
openai.api_key = "sk********************1" # 你的 SECRET KEY
# msgList: [ {'role': 'user', 'content': your question}, {'role': 'assistant', 'content': gpt reply} ]
try:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=msgList # 列表格式，形如上面注释
    )
    reply = completion.choices[0].message["content"]
except BaseException as e: # 异常处理
	print(e) 

```

## 文字以图片形式发送

&emsp;考虑到很多关键字不好过滤，那么就以图片发送文字

```python
from PIL import Image, ImageDraw, ImageFont
import time
import unicodedata

# 图片需要自己设置长宽，如果使用我的默认设置，那就不需要更改，否则有些显示不全自动调整

max_tab = 5 # 最大允许缩进tab
line_length_max = 50 # 一行字符最长能容纳50个单字符，自行设置
font_size = (24, 48)  # 字体 (宽，高)
line_space = 5

# 需要自行下载微软雅黑字体（可用其他字体，但需要是ttf或otf，woff不行）
# 目前我没找到支持 emoji 的ttf字体
myfont = ImageFont.truetype("weiruanyahei.ttf", 48) 
start_point = (100, 100) # 开始写字的点

def toImg(strs: list[str], path: str) -> str:
    w = line_length_max * (font_size[0]) + 3 * start_point[0] # 图宽
    h = len(strs) * (font_size[1] + line_space) + 3 * start_point[1] # 图高
    # 以黑色，半透明的形式画
    img = Image.new("RGBA", (w, h), color=(255,255,255,50))
    cavens = ImageDraw.Draw(img, "RGBA") 
    
    # 拼接字符串，方便而已
    news = ""
    for s in strs:
        news += s
    news = news.strip() # 去除多余空白字符
    
    cavens.text(start_point, news, font=myfont, fill="#00FF00") # 以绿色书写
    # img.show('测试') # 显示
    newpath = path + '_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.png'
    img.save(newpath) # 保存
    return newpath # 返回路径


def wrap(text) -> list[str]:
    text += '\n' # 只是为了方便写代码，所以多加一行无实际意义的换行
    tabs = max_tab
    str_list = []
    tmp = ""
    line_size = 0
    text = text.replace('    ', '\t') # 以四个空格作为tab
    for ch in text:
        if ch == '\t':
            if line_size + 2 > line_length_max:
                str_list.append(tmp)
                tmp = ""
                line_size = 0
            if tabs > 0:
                tmp += '  '
                line_size += 2
            tabs -= 1
        elif ch == '\n':
            tabs = max_tab
            if len(tmp) > 0:
                str_list.append(tmp + '\n')
                tmp = ""
            else:
                str_list.append('\n')
            line_size = 0
        else:
            tabs = max_tab
            if line_size >= line_length_max:
                str_list.append(tmp + '\n')
                tmp = ""
                line_size = 0
            tmp += ch
            if unicodedata.east_asian_width(ch) == 'W':
                line_size += 2
            else:
                line_size += 1
    return str_list


def textToIMG(text: str, path: str) -> str:
    strs = wrap(text)
    file = toImg(strs, path)
    return file


if __name__ == '__main__':
    t = textToIMG("这是一个测试字符串\nfjlaksdfjalsgj", "测试路径")

```

# 博客

关注博客：[雨探青鸟](https://lmzyoyo.top/archives/chatgptmiraiqqbot)