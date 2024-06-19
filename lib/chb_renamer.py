"""
批量重命名,移除名称里面的不需要部分
"""

import os
import glob

dont_need_list = [
    "【需要去除的字符串】",
]

path = "这里填路径"


def rename(file_name):
    for dont_need in dont_need_list:
        file_name = file_name.replace(dont_need, "")
    return file_name


def list_files(path):
    """
    遍历指定路径下的所有文件。

    :param path: 要遍历的目录路径
    """
    for root, dirs, files in os.walk(path):
        for file in files:
            # 构建完整的文件路径
            old_file_path = os.path.join(root, file)
            new_file_path = os.path.join(root, rename(file))
            os.rename(old_file_path, new_file_path)


if __name__ == '__main__':
    # 遍历path下的所有文件
    list_files(path)
    pass
