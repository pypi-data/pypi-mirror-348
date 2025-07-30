import sys
import os

def read_and_print(command):
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, "data", f"{command}.txt")

    if not os.path.isfile(data_path):
        print(f"未知命令或缺少数据文件：{command}")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        print(f.read())

def main():
    if len(sys.argv) < 2:
        print("Usage: cuit_alore_duoyuan <command>")
        return

    command = sys.argv[1]
    read_and_print(command)

if __name__ == "__main__":
    main()
