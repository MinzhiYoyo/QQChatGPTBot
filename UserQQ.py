import Info
from ToIMG import textToIMG
import chat
from Info import BotInfo, FLAG
import time


# 群中某一个人的qq代表唯一的 UserQQ
# 为了调度和记录

class UserQQ:
    """
    参数：
        # 会话维持
        self.__message: 每一个元素都是 {"role": "user/assistant", "content":"内容"}
        self.__maxsize: 一次连续会话的最长次数，仅对 ChatGPT 有效，不用于 Stable Diffcusion画图
        self.__count: 记录会话剩余次数，递减方式

        # 流量限制
        self.__lastTime: 上一次使用的时间戳
        self.__available_time  # 可发送回复的时间戳，用于禁言
        self.__vio_num: 违禁次数，递减方式
        self.__vio_max: 违禁最大次数

        # id辨识，群号和qq号辨识唯一的用户
        self.__qq: qq号
        self.__group_qq: 群号
    方法：
        def getQQ(self) -> int: 返回个人QQ
        def cmdSelector(self, msg: str) -> tuple[FLAG, str]: 命令选择器，将用户输入命令进行选择
        def bot(self, msg: str): 外部接口，输入一条语句
        def __clearHistory(self): 清除 ChatGPT 的历史
        def __toLog(self, msg_type: str, msg: str): 日志保存，以 群号_个人QQ.log 命名
    """

    def __init__(self, qq: int, groupqq: int, maxsize: int = 5, available_time: float = -1, vio_max=3):
        """
        :param qq: 用户qq
        :param groupqq: 群号qq
        :param maxsize: 最大会话维持记录
        :param available_time: 可用时间
        """

        # 会话维持
        self.__message = []  # 每一个元素都是 {"role": "user/assistant", "content":"内容"}
        self.__maxsize = maxsize  # 一次连续会话的最长次数
        self.__count = maxsize  # 记录会话剩余次数

        # 流量限制
        self.__lastTime = -1
        self.__available_time = available_time  # 可发送回复的时间戳
        self.__vio_num = vio_max
        self.__vio_max = vio_max

        # id辨识
        self.__qq = qq  # qq设置为私有类型，防止被改变
        self.__group_qq = groupqq  # 群号

    def getQQ(self) -> int:
        return self.__qq

    def cmdSelector(self, msg: str) -> tuple[FLAG, str]:
        if msg.startswith('*'):  # 命令模式
            cmd = msg[1:]
            cmd = cmd.strip()
            if cmd == "查看帮助":
                return FLAG.INFOMATION, BotInfo.helpInfo
            elif cmd == "清除历史":
                self.__clearHistory()
                return FLAG.INFOMATION, BotInfo.NoticeHead + BotInfo.clear(self.__qq)
            elif cmd == "文字画图":
                return FLAG.ERRORPICTURE, BotInfo.unavailable("文字画图")  # 增加了功能，记得改变返回值
            else:
                return FLAG.ERROR, BotInfo.ErrorHead + BotInfo.error_cmd(msg)
        else:  # 聊天模式
            self.__message.append(
                {'role': 'user', 'content': msg}
            )
            if len(self.__message) == 0:
                return FLAG.ERRORCHAT, BotInfo.ErrorHead + BotInfo.unkowned("聊天记录为空")
            flag, info = chat.toChatGPT(self.__message)
            if flag == FLAG.ERRORCHAT:
                return flag, BotInfo.ErrorHead + info
            return flag, info + BotInfo.Part + BotInfo.long_line + BotInfo.NoticeHead + BotInfo.remain(self.__count-1)

    def bot(self, msg: str):
        now = time.time()
        self.__toLog(BotInfo.UserMessage, msg)

        # 做时间过滤
        # 距离上次时间间隔太短了
        if self.__lastTime > 0 and now - self.__lastTime < Info.TimeControl.SESSION_GAP:
            self.__vio_num -= 1
            if self.__vio_num == 0:  # 违禁次数过多，禁言
                self.__available_time = now + Info.TimeControl.SESSION_GAP * self.__maxsize
                self.__vio_num = self.__vio_max
                info = Info.BotInfo.violations(self.__vio_max - self.__vio_num)

        # 没到可用时间
        if now < self.__available_time:
            info = Info.BotInfo.wait(self.__available_time - now)

        # 更新部分信息
        self.__lastTime = time.time()

        # 做输入消息过滤
        # 尚未过滤

        # 消息处理
        flag, info = self.cmdSelector(msg)  # 这一步，需要耗费时间长
        msg_type = Info.BotInfo.UserMessage
        now = time.time()
        if flag == Info.FLAG.ERROR:
            msg_type = Info.BotInfo.ErrorMessage
        elif flag == Info.FLAG.CHAT:  # 更新message
            self.__message.append(
                {"role": "assistant", "content": info}
            )
            self.__count -= 1
            if self.__count == 0:
                self.__count = self.__maxsize
                info = info + BotInfo.Part + BotInfo.clear(self.__qq)
                self.__clearHistory()
            msg_type = Info.BotInfo.BotMessage
        elif flag == Info.FLAG.INFOMATION:
            msg_type = Info.BotInfo.SystemMessage
        elif flag == Info.FLAG.ERRORPICTURE:
            pass
        elif flag == Info.FLAG.ERRORCHAT:  # 回滚message
            # 回滚消息
            if len(self.__message) > 0 and self.__message[-1]['role'] == 'user':
                self.__message.pop()
            msg_type = Info.BotInfo.ErrorMessage
        # else:

        # 做输出消息过滤
        # 尚未过滤

        # 保存日志
        self.__toLog(msg_type, info)

        # 变成图片，然后输出
        try:
            path = textToIMG(info, flag, str(self.__group_qq) + '_' + str(self.__qq))
            # 保存图片路径日志
            self.__toLog(BotInfo.BotOutputMessage, info + "\n" + BotInfo.PicMessage + path)
            return path
        except BaseException as e:
            self.__toLog(BotInfo.ErrorMessage, info)
            return BotInfo.ErrDic + BotInfo.ErrorPic

    def __clearHistory(self):  # 清除历史：清除message和count
        self.__message.clear()
        self.__count = self.__maxsize

    def __toLog(self, msg_type: str, msg: str):
        try:
            with open(BotInfo.LogDic + str(self.__group_qq) + "_" + str(self.__qq) + ".log", "a+", encoding="utf-8") as f:
                f.write(BotInfo.timeInfo() + BotInfo.Table + msg_type + "\n" + msg + BotInfo.Part + '\n\n')
        except BaseException as e:
            print(e)
            pass

