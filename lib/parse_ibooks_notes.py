import sys
import email
import re
import os
from email.header import decode_header
from email.utils import parsedate_to_datetime
from collections import OrderedDict


class Note:
    def __init__(self, title: str, underlined_sentences_dict: OrderedDict):
        """
        title: 标题
        underlined_sentences: 划线句(key:划线句 value: 注释)
        """
        self.title = title
        self.underlined_sentences_dict = underlined_sentences_dict


def write_body_to_file(body: str):
    with open("temp_body.txt", "w") as file:
        file.write(body)


def parse_eml(eml_fp, attr_dir):
    """
    eml文件解析
    :params eml_fp: eml文件路径
    :params attr_dir: 附件保存目录
    """
    if not os.path.exists(attr_dir):
        os.makedirs(attr_dir)

    # 读取eml文件
    with open(eml_fp, "r") as file:
        eml_content = file.read()
    # 转为email对象
    msg = email.message_from_string(eml_content)

    # 邮件主题
    subject_bytes, subject_encode = decode_header(msg["Subject"])[0]
    if subject_encode:
        subject = subject_bytes.decode(subject_encode)
    else:
        subject = subject_bytes
    print("主题：", subject)

    # 邮件发件人
    from_ip = re.search("<(.*)>", msg["from"]).group(1)
    print("发件人邮箱：", from_ip)
    from_name = decode_header(msg["from"].split("<")[0].strip())
    if from_name:
        if from_name[0] and from_name[0][1]:
            from_n = from_name[0][0].decode(from_name[0][1])
        else:
            from_n = from_name[0][0]
    print("发件人名称：", from_n)

    # 邮件时间
    received_date = parsedate_to_datetime(msg["date"])
    print("接收时间：", received_date)

    # 邮件正文及附件
    for par in msg.walk():
        if not par.is_multipart():  # 判断是否为multipart，里面的数据不需要
            name = par.get_param("name")  # 获取附件的文件名
            if name:
                # 附件
                fname = decode_header(name)[0]
                if fname[1]:
                    attr_name = fname[0].decode(fname[1])
                else:
                    attr_name = fname[0]
                print("附件名:", attr_name)
                # 解码附件内容
                attr_data = par.get_payload(decode=True)
                attr_fp = os.path.join(attr_dir, attr_name)
                with open(attr_fp, 'wb') as f_write:
                    f_write.write(attr_data)
            else:
                # 正文
                text_char = par.get_content_charset()
                if "text/plain" in par["content-type"]:  # 文本正文
                    body = par.get_payload(decode=True).decode(text_char)
                    print("邮件正文：", body)
                    write_body_to_file(body)
                else:
                    # html格式正文
                    # html_body = par.get_payload(decode=True).decode(text_char)
                    # print("HTML正文：", html_body)
                    # 这部分我不需要
                    pass
            print("-" * 60)


def modeling_data():
    underlined_sentences_dict = OrderedDict()
    note = Note("", underlined_sentences_dict)

    with open("temp_body.txt", "r") as file:
        lines = file.readlines()
        index = 0
        length = len(lines)
        while index < length:
            line = lines[index]
            if str(line).strip() == "":
                index += 1
                continue
            if line.startswith("笔记摘自"):
                # 标题
                has_value_index = find_next_has_value_line(lines, index)
                if has_value_index != -1:
                    title = lines[has_value_index].strip()
                    # print("标题:" + title)
                    note.title = title
                    index = has_value_index + 1
                    continue
            elif is_date_at_start(line):
                # 划线句
                has_value_index = find_next_has_value_line(lines, index)
                if has_value_index != -1:
                    underlined_sentences = lines[has_value_index].strip()
                    underlined_sentences_dict[underlined_sentences] = []
                    # print("划线句:" + underlined_sentences)
                    # 找到 关于划线句的注释
                    next_date_at_start_index = find_next_date_at_start(lines, has_value_index)
                    if next_date_at_start_index != -1 and next_date_at_start_index < length and next_date_at_start_index != (
                            has_value_index + 1):
                        # 取出has_value_index到next_date_at_start_index的所有行
                        underlined_sentences_comment = lines[has_value_index + 1:next_date_at_start_index]
                        # 找到注释
                        for e in underlined_sentences_comment:
                            if e.strip() != "":
                                # print("注释:" + e)
                                underlined_sentences_dict[underlined_sentences].append(e)
                        index = next_date_at_start_index
                        continue
                    elif next_date_at_start_index == -1:
                        end_index = find_end(lines, has_value_index)
                        if end_index != -1:
                            # 取出has_value_index到end_index的所有行
                            underlined_sentences_comment = lines[has_value_index + 1:end_index]
                            # 找到注释
                            for e in underlined_sentences_comment:
                                if e.strip() != "":
                                    # print("注释:" + e)
                                    underlined_sentences_dict[underlined_sentences].append(e)
                            index = end_index
                            continue

            index += 1
    return note


def find_next_date_at_start(lines, index):
    """
    寻找下一个日期开始的line的index
    """
    index = index + 1
    while index < len(lines):
        line = lines[index]
        if is_date_at_start(line):
            return index
        index += 1
    return -1


def find_end(lines, index):
    """
    寻找结束的line的index
    """
    index = index + 1
    while index < len(lines):
        line = lines[index]
        if str(line).strip() == "":
            index += 1
            continue
        if line.startswith("所有摘录来自"):
            return index
        index += 1
    return -1


def is_date_at_start(string):
    """
    匹配日期的开始
    """
    # 正则表达式匹配 YYYY年M月D日
    # \d 表示数字，{4}表示重复4次，{1,2}表示重复1到2次
    # ^ 表示匹配字符串开头
    pattern = r'^\d{4}年\d{1,2}月\d{1,2}日'

    # 使用re.match来检查字符串开头是否匹配正则表达式
    if re.match(pattern, string):
        return True
    return False


def find_next_has_value_line(lines, index):
    """
    寻找下一个有值的行
    """
    index = index + 1
    while index < len(lines):
        line = lines[index]
        if str(line).strip() == "":
            index += 1
            continue
        if len(line) > 0:
            return index
        index += 1
    return -1


def generate_note(note: Note):
    """
    生成笔记
    """
    # 生成note.title的markdown文件
    file_path = note.title + "_笔记.md"
    content = ""
    for key, value in note.underlined_sentences_dict.items():
        content += "- " + key
        if not key.__contains__("\n"):
            content += "\n"
        for v in value:
            content += "> "
            if len(value) > 1:
                content += "- "
            content += v
            if not v.__contains__("\n"):
                content += "\n"

    # 打开文件，模式"w"表示写入模式，如果文件已存在则会被覆盖
    with open(file_path, "w") as file:
        # 将内容写入文件
        file.write(content)

    pass


if __name__ == '__main__':
    eml_path = sys.argv[1]
    print("开始处理文件: " + eml_path)
    parse_eml(eml_path, "./")
    print("处理完成,开始建模")
    note = modeling_data()
    print("开始生成笔记")
    generate_note(note)
    os.remove("temp_body.txt")
    print("处理完成")
