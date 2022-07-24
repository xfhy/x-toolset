# coding=UTF-8
import sys
import os


headline_dic = {'#': 0, '##': 1, '###': 2, '####': 3, '#####': 4, '######': 5}
suojin = {0: -1, 1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1}

# 准备拿来加序号的,暂时没用到
header_number_array = [0, 0, 0, 0, 0, 0]


def writefile(fp, str=None):
    with open(fp, 'w') as f:
        f.write(str)


def detectHeadLines(f,realName):
    '''detact headline and return inserted string.
    params:
        f: Markdown file
    '''
    f.seek(0)

    insert_str = ""
    org_str = ""

    last_status = -1
    c_status = -1

    headline_counter = 0
    iscode = False

    # 处理目录内容
    for line in f.readlines():
        # 如果是代码块
        if(line[:3] == '```'):
            iscode = not iscode

        # fix code indent bug and fix other indentation bug. 2020/7/3  缩进问题
        if not iscode:
            temp_line = line.strip(' ')
        ls = temp_line.split(' ')
        # '## 标题' -> ls[0]:'##' ls[1]:'标题'
        if len(ls) > 1 and ls[0] in headline_dic.keys() and not iscode:
            headline_counter += 1
            c_status = headline_dic[ls[0]]
            #header_number_array[c_status] = header_number_array[c_status] + 1
            # find first rank headline
            if last_status == -1 or c_status == 0 or suojin[c_status] == 0:
                # init suojin
                for key in suojin.keys():
                    suojin[key] = -1
                suojin[c_status] = 0
            elif c_status > last_status:
                suojin[c_status] = suojin[last_status]+1

            # update headline text
            headtext = (' '.join(ls[1:-1]))
            spaceText = '' if headtext == '' else ' '
            if ls[-1][-1] == '\n':
                headtext += (spaceText+ls[-1][:-1])
            else:
                headtext += (spaceText+ls[-1])

            if headtext.find('资料') != -1:
                continue

            headid = '{}{}'.format('head', headline_counter)
            headline = ls[0] + \
                ' <span id=\"{}\"'.format(headid)+'>' + headtext+'</span>'+'\n'
            org_str += headline

            jump_str = '- [{}](#{}{})'.format(headtext,
                                              'head', headline_counter)
            insert_str += ('\t'*suojin[c_status]+jump_str+'\n')

            last_status = c_status
        else:
            org_str += line

    # 前缀
    prefix = ''
    prefix += realName
    prefix += '\n'
    prefix += '---'
    prefix += '\r\n'
    prefix += '#### 目录'
    prefix += '\n'

    # 后缀
    afterFix = ''
    afterFix += '\n'
    afterFix += '---'
    afterFix += '\r\n'

    insert_str = prefix + insert_str + afterFix

    return insert_str + org_str


def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position+1)
        if position == -1:
            return last_position
        last_position = position


if __name__ == '__main__':

    filename = sys.argv[1]
    fullName = os.path.basename(filename)
    realName = fullName[:find_last(fullName, ".")]
    print(realName)
    f = open(filename, 'r', encoding='utf-8')
    insert_str = detectHeadLines(f,realName)
    f.close()
    with open('{}_with_toc.md'.format(realName), 'w', encoding='utf-8') as f:
        f.write(insert_str)
