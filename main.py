from graia.ariadne.app import Ariadne
from graia.ariadne.entry import config
from graia.ariadne.message import Source
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image, At
from graia.ariadne.message.parser.base import MentionMe
from graia.ariadne.model import Member
from graia.ariadne.model import Group

import Info
from UserQQ import UserQQ

app = Ariadne(config(verify_key="yirimirai", account=机器人的qq号, ), )

allGroups = {
   # int: list[UserQQ] # 其中int是qq群号，后面跟着User的list
   # 实际上是群的白名单，在白名单才能使用该机器人，只需要添加  群号: [], 即可
}


@app.broadcast.receiver("GroupMessage", decorators=[MentionMe(), ])
async def group_message_listener(app_bot: Ariadne, group: Group, chain: MessageChain, src: Source, member: Member):
    input_message = ""
    tmpcontent = chain.content[1:]
    for msg in tmpcontent:
        if msg.type == 'Plain':
            input_message += str(msg)
        elif msg.type == 'At': # 这里转成字符串其实是：@qq号，建议删除
            input_message += (msg.representation + '(人名) ')

    input_message = input_message.strip()
    if len(input_message) > 2:
        if group.id in allGroups:
            info = Info.BotInfo.ErrDic + Info.BotInfo.ErrorPic
            flag = True
            for auser in allGroups[group.id]:
                if auser.getQQ() == member.id:
                    flag = False
                    info = auser.bot(input_message)
            if flag:
                tmpuser = UserQQ(member.id, group.id)
                info = tmpuser.bot(input_message)
                allGroups[group.id].append(tmpuser)
            message_charin = MessageChain([At(member.id), Image(path=info)])
            await app_bot.send_message(group, message_charin, quote=src)


app.launch_blocking()
