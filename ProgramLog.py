import os
import time

class Logging:
    def __init__(self, FilePath):
        self.time = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime(time.time()))
        self.File = FilePath
        if os.path.exists(os.path.split(FilePath)[0]):
            with open(FilePath, "w+", encoding="utf-8") as fp:
                fp.write(f"{self.time}|{FilePath}|新建日志\n")
        else:
            raise TypeError(f"参数错误！{FilePath}路径不存在！")

    def record(self, Type, Data):
        with open(self.File, "r+", encoding="utf-8") as fp:
            fp.write(f"{self.time}|{Type}|{Data}\n")
            print(f"{self.time}|{Type}|{Data}")