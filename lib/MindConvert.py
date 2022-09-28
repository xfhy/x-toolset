# coding=UTF-8
import sys


# author xfhy
# 2021年1月18日
# 将幕布思维导图的内容直接全选复制到一个文件中，然后将其转成markdown并标上序号.
# 使用: 将思维导图复制文本到一个文件中,假设为a.md,然后使用命令"python MindConvert.py a.md" 即可生成带目录编号的a_toc.md

def detectHeadLines(filename):
    # 未加序号时,每一行的内容
    beforeFixList = []

    with open(filename, 'r', encoding='UTF-8') as lines:
        for line in lines:
            beforeFixList.append(line.replace("\n", ""))

    titleLevel = ["##", "###", "####", "#####"]

    # 结果list
    afterFixList = []
    # 当前标题序号
    oneTitleNum = 0
    twoTitleNum = 0
    threeTitleNum = 0
    fourTitleNum = 0

    for line in beforeFixList:
        spaceCount = line.count("   ")
        # 没有｜符号
        noVerticalLine = (line.count("｜") == 0)
        line = line.replace("   ", "").replace("｜", "").replace(" ", "")

        if (not noVerticalLine):
            # 有 | 符号,说明这里是注释
            afterFixList.append("> " + line)
            pass
        elif (spaceCount == 0):
            oneTitleNum += 1
            twoTitleNum = 0
            threeTitleNum = 0
            fourTitleNum = 0
            afterFixList.append(titleLevel[0] + " " + str(oneTitleNum) + ". " + line)
        elif (spaceCount == 1):
            twoTitleNum += 1
            threeTitleNum = 0
            fourTitleNum = 0
            afterFixList.append(
                titleLevel[1] + " " + str(oneTitleNum) + "." + str(twoTitleNum) + " " + line)
        elif (spaceCount == 2):
            threeTitleNum += 1
            fourTitleNum = 0
            afterFixList.append(titleLevel[2] + " " + str(oneTitleNum) + "." +
                                str(twoTitleNum) + "." + str(threeTitleNum) + " " + line)
        elif (spaceCount == 4):
            fourTitleNum += 1
            # afterFixList.append(titleLevel[3]+" "+str(oneTitleNum)+"." + \
            #     str(twoTitleNum)+"."+str(threeTitleNum)+"."+str(fourTitleNum)+" "+line)
            afterFixList.append("- " + line)

    # 将修改之后内容的写到文件中
    with open(filename + "_toc.md", 'w', encoding='UTF-8') as f:
        for line in afterFixList:
            f.write(line + "\n")


# print(afterFixList)
if __name__ == '__main__':
    filename = sys.argv[1]
    print("开始处理文件: " + filename)
    detectHeadLines(filename)
    print("处理完成")
