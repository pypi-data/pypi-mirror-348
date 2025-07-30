import sys
import os
import time
import subprocess

try:
    import pyperclip
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "pyperclip"])
    import pyperclip

def read_and_print(command):
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, "data", f"{command}.txt")

    if not os.path.isfile(data_path):
        print(f"未知命令或缺少数据文件：{command}")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        content = f.read()
        print(content)
        time.sleep(2)

        # 清屏（Windows & Unix 兼容）
        os.system('cls' if os.name == 'nt' else 'clear')

        time.sleep(1)

        # 复制到剪贴板
        pyperclip.copy(content)

def main():
    if len(sys.argv) < 2:
        print("Usage: cuit_alore_duoyuan <command>")
        return

    command = sys.argv[1]
    read_and_print(command)

if __name__ == "__main__":
    main()
