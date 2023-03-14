from enum import Enum
import time

# 本文件提供 Bot 使用到的常量，如提示信息等等

# 时间控制，单位s
class TimeControl:
    SESSION_GAP = 20
    SESSION_BREAK = 20

class FLAG(Enum):
    ERROR = 0

    CHAT = 1
    PICTURE = 2

    INFOMATION = 3

    ERRORCHAT = 4
    ERRORPICTURE = 5



class BotInfo:
    # 以下是路径信息
    ErrDic = './errs/'
    LogDic = './logs/'
    PicDic = './pic/'


    # 以下是默认消息
    ErrorPic = "UnkownedError.png"

    # 以下是消息头部
    WarningHead = "【警告☠️】 "
    InformationHead = "【提示😲】 "
    ErrorHead = "【错误❌】 "
    NoticeHead = "【通知🤖】 "


    # 以下是提醒消息
    @staticmethod
    def remain(times: int):
        if times == 0:
            return "此次会话结束后，我将失去关于你的记忆 ๐·°(৹˃̵﹏˂̵৹)°·๐"
        return "还剩{}次，会话记录将被自动清除，我们需要重新认识".format(times)

    @staticmethod
    def error_cmd(cmd: str):
        return "<{}>命令无法识别（看都看不懂┌(。Д。)┐），请重试".format(cmd)

    @staticmethod
    def wait(t: float):
        return "您还需要{}分{}秒才能使用 (҂‾ ▵‾)︻デ═一".format(int(t / 60), int(t % 60))

    @staticmethod
    def clear(qq: int):
        return "qq：{} 用户历史记录已被清除，我们需要重新认识".format(qq)

    @staticmethod
    def unavailable(fun: str):
        return "<{}>功能尚未开放 ε(┬┬﹏┬┬)3".format(fun)

    @staticmethod
    def violations(times: int):
        return "您违禁次数已达到【{}】次，将暂时对您关闭功能，过会才能使用 („ಡωಡ„)".format(times)

    @staticmethod
    def unkowned(err: str):
        return "未知错误<{}>发生 X﹏X".format(err)

    # 以下是分割符号
    Part = "\n"
    line_length = 50
    long_line = '\n' + ("-" * (line_length-1)) + '\n'
    Table = '\t'

    # 下面是消息类型，只会用于保存到文件中
    UserMessage = "【用户🙋‍♀️】"
    ChatGPTMessage = "【ChatGPT🔥】"
    PictureMessage = "【图片💧】"
    BotMessage = "【ChatGPT👽】"
    BotOutputMessage = "【GPT图片💾】"
    ErrorMessage = "【未知错误💩】"
    PicMessage = "【图片🎴】 "
    SystemMessage = "【Bot👾】"

    # FLAG = Enum('Error', 'Chat', 'Picture')
    helpInfo = """
帮助信息:

         小查-2.1(小の) 
powered by 2498369702(雨探青鸟)

由 ChatGPT3.5构建语言模型
由 Mirai 构建 QQ 接口
由 Ariadne 构建 Mirai 接口
由 Stable Diffusion 构建文字画图功能（此功能需要用到一定算力，不一定开放）
由 PIL 库进行文字转图片发送

请直接在群里 艾特 我即可，您可以发送
1. $<命令>,其中'$'与命令之间不能有空格，如"$查看帮助"
    <命令>：
        (1) 查看帮助，即可查看该机器人版本与功能
        (2) 清除历史，即可立即清除上下文历史记录
        (3) 文字画图(尚未实现)，即可根据您的句子生成一张图片（用英文描述会更加准确，句子不宜长也不宜短，20 words左右）

2. 发送消息，机器人接入了聊天接口，预计4月1日停止使用。该机器人可以保留上下文历史记录为5条，达到5条自动清空。如果聊天中出现违禁关键词，将自动屏蔽。
"""

    @staticmethod
    def timeInfo():
        return time.strftime("【%Y-%m-%d %H:%M:%S】 ", time.localtime())
