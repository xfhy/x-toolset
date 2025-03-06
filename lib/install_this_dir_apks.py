import os
import subprocess
import sys


def install_apks():
    # 获取当前目录下所有apk文件
    apk_files = [f for f in os.listdir('.') if f.lower().endswith('.apk')]

    if not apk_files:
        print("❌ 当前目录未找到APK文件")
        sys.exit(1)

    # 检查设备连接
    try:
        devices = subprocess.check_output(['adb', 'devices'], text=True)
        if 'device' not in devices:
            print("❌ 未检测到已连接的Android设备")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("❌ ADB命令执行失败，请检查ADB安装")
        sys.exit(1)

    # 安装所有APK
    total = len(apk_files)
    success = []
    failures = []

    for idx, apk in enumerate(apk_files, 1):
        print(f"\n📦 正在安装 ({idx}/{total}): {apk}")
        try:
            subprocess.check_call(['adb', 'install', '-r', apk])
            success.append(apk)
        except subprocess.CalledProcessError:
            failures.append(apk)

    # 输出结果
    print("\n" + "=" * 40)
    print(f"✅ 成功安装: {len(success)} 个")
    print(f"❌ 安装失败: {len(failures)} 个")

    if failures:
        print("\n失败列表:")
        for f in failures:
            print(f"• {f}")


if __name__ == "__main__":
    install_apks()