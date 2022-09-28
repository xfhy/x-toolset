# coding=UTF-8
import sys
import opml

# author xfhy
# 2021年1月18日
# 将幕布思维导图导出成opml，然后将其转成markdown并标上序号.
# 使用: 使用命令"python opmlConvert2Md.py a.opml" 即可生成对应的a.md


lineList = []


# 生成重复字符串
def createRepeatStr(text, count):
    return text * count


def isSequenceStart(text):
    length = len(text)
    if length <= 2:
        return False
    return text[0].isdigit() and text[1] == '.' and text[2] == ' '


def recu(outline, hCount, spaceCount):
    length = len(outline)

    # 一级就是 ## 标题
    for i in range(0, length):
        # 前缀 preText
        # 实际内容
        content = outline[i].text
        # 注释
        _note = outline[i]._note

        #  第一个层级的标题#个数为2，我设定的
        if hCount == 2:
            preText = createRepeatStr("#", hCount) + " " + str(i + 1) + ". "
        else:
            if hCount == 3:
                preText = "- "
            else:
                # 如果是以 "1. " 开头的，则无需再增加 -
                if isSequenceStart(content):
                    preText = createRepeatStr("    ", spaceCount)
                else:
                    preText = createRepeatStr("    ", spaceCount) + "- "
        lineList.append(preText + content)

        # 处理注释
        if len(_note) > 0:
            lineList.append(createRepeatStr("    ", spaceCount) + "> " + _note)

        # 可能有子项，递归添加
        if len(outline[i]) > 0:
            recu(outline[i], hCount + 1, spaceCount + 1)


def convert(filename):
    outline = opml.parse(filename)
    recu(outline, 2, -1)

def writeContent2File(filename):
    # 将修改之后内容的写到文件中
    with open(filename + ".md", 'w', encoding='UTF-8') as f:
        for line in lineList:
            f.write(line + "\n")


if __name__ == '__main__':
    filename = sys.argv[1]
    print("开始处理文件: " + filename)
    convert(filename)
    writeContent2File(filename)
    print("处理完成")
