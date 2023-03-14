import openai
import Info
from Info import BotInfo, FLAG

# 本文件只作为提供 ChatGPT 的接口

openai.api_key = "sk-*******************************M31" # 你的 OpenAI 的 Key

logFile = Info.BotInfo.ErrDic + "ChatGPT.log"


# 传入list，返回是否成功
# msgList: [ {'role': 'user', 'content': your question}, {'role': 'assistant', 'content': gpt reply} ]
def toChatGPT(msgList: list) -> tuple[FLAG, str]:
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=msgList
        )
        return FLAG.CHAT, completion.choices[0].message["content"]
    except BaseException as e:
        with open(logFile, "a+", encoding="utf8") as f:
            f.write(BotInfo.timeInfo() + '\n')
            for msg in msgList:
                f.write('<' + msg['role'] + '>: {\n' + msg['content'] + '\n}')
            f.write('<err>: {\n' + str(e) + '\n}')
            f.write('\n=====================================\n\n\n')
        return FLAG.ERRORCHAT, str(e)
