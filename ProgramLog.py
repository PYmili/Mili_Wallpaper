import os
import time

class Logging:
    def __init__(self, FilePath):
        self.time = time.strftime("[%Y-%m-%d %H:%M:%S]", time.localtime(time.time()))
        self.File = FilePath
        if os.path.exists(FilePath):
            self.record("正常运行", "启动程序")
        else:
            with open(FilePath, "w+", encoding="utf-8") as fp:
                fp.write(f"{self.time}|{FilePath}|新建日志\n")

    def record(self, Type, Data):
        with open(self.File, "a+", encoding="utf-8") as fp:
            fp.write(f"{self.time}|{Type}|{Data}\n")
            print(f"{self.time}|{Type}|{Data}")