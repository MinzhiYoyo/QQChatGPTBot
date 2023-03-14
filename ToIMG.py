from PIL import Image, ImageDraw, ImageFont
import Info
import time
import unicodedata

# 实现文字转成图片，然后保存在 './pic/' 路径下，命名是 群号_个人QQ_时间.png


# 参数已经调好，如果要更改，就需要自己重新调
max_tab = 5
line_length_max = Info.BotInfo.line_length
font_size = (24, 48)  # 字体 (宽，高)
line_space = 5
myfont = ImageFont.truetype("weiruanyahei.ttf", 48)
start_point = (100, 100)


def toImg(strs: list[str], style: Info.FLAG, path: str) -> str:
    w = line_length_max * (font_size[0]) + 3 * start_point[0]
    h = len(strs) * (font_size[1] + line_space) + 3 * start_point[1]
    color = [0, 0, 0, 10]
    font_color = None
    if style == Info.FLAG.ERROR:
        color[0] = 255
        font_color = '#FF0000'
    elif style == Info.FLAG.CHAT:
        color[2] = 255
        font_color = '#0000FF'
    elif style == Info.FLAG.INFOMATION:
        color[1] = 255
        font_color = '#00FF00'
    elif style == Info.FLAG.ERRORPICTURE:
        color[1] = 255
        font_color = '#FF0000'
    elif style == Info.FLAG.ERRORCHAT:
        color[2] = 255
        font_color = '#FF0000'
    else:
        font_color = '#FFFFFF'

    img = Image.new("RGBA", (w, h), color=tuple(color))
    cavens = ImageDraw.Draw(img, "RGBA")
    news = ""
    for s in strs:
        news += s
    news = news.strip()
    cavens.text(start_point, news, font=myfont, fill=font_color)
    # img.show('测试')
    newpath = Info.BotInfo.PicDic + path + '_' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.png'
    try:
        img.save(newpath)
    except BaseException as e:
        raise
    return newpath


def wrap(text) -> list[str]:
    text += '\n'
    tabs = max_tab
    str_list = []
    tmp = ""
    line_size = 0
    text = text.replace('    ', '\t')
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
                # str_list.append('\n')
                tmp = ""
                line_size = 0
            tmp += ch
            if unicodedata.east_asian_width(ch) == 'W':
                line_size += 2
            else:
                line_size += 1
    return str_list


def textToIMG(text: str, style: Info.FLAG, path: str) -> str:
    strs = wrap(text)
    file = toImg(strs, style, path)
    return file


if __name__ == '__main__':
    txt = open('./test.txt', 'r', encoding="utf8").read()

    t = textToIMG(Info.BotInfo.helpInfo, Info.FLAG.INFOMATION, "调试")
