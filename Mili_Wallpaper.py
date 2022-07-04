import sv_ttk
import tkinter
import tkinter.ttk
from tkinter import *
import tkinter.filedialog
import tkinter.messagebox
from PIL import Image,ImageTk
import imageio
import os
import getpass
import sys
import json

import Window_settings
import time
import win32gui
from win32.lib import win32con
import requests
from threading import Thread

import ProgramLog
import GetBilibiliVideo

Log = ProgramLog.Logging(os.path.split(__file__)[0]+"/Log/journal.log")

try:
    __Version__ = open(f"{os.path.split(__file__)[0]}/Log/Version.wll", "r", encoding="utf-8").read()
except:
    with open(f"{os.path.split(__file__)[0]}/Log/Version.wll", "r", encoding="utf-8") as fp:
        fp.write("1.8")
    __Version__ = open(f"{os.path.split(__file__)[0]}/Log/Version.wll", "r", encoding="utf-8").read()

"""Mpv播放器"""
def MpvPlay(Video, audio):
    if audio:
        os.popen(
            f"""cd {os.path.split(__file__)[0]}/mpv && mpv {Video} -loop --title="MyMpv" --cursor-autohide=no -fs -audio=1"""
        )
        Log.record("正常运行", f"Mpv Play -->> {Video}")
    else:
        os.popen(
            f"""cd {os.path.split(__file__)[0]}/mpv && mpv {Video} -loop --title="MyMpv" --cursor-autohide=no -fs -audio=0"""
        )
        Log.record("正常运行", f"Mpv Play -->> {Video}")


def MpvTread(Video, audio, kill, sleeptime):
    MPV = Thread(target=MpvPlay, args=(Video, audio))
    MPV.start()
    MPV.join()
    time.sleep(sleeptime)
    try:
        Window_settings.main(f"MyMpv")
        UIDLOG(Window_settings._id_)
        Log.record("正常运行", "Settings：True")
    except:
        kill()
        Log.record("正常运行", "Settings：False")
        tkinter.messagebox.showinfo("错误！", "出现了一些非正常错误请重新启动程序尝试！")

"""Mpv Paly Url Video"""
def MpvUrlPlay(VideoUrl, audio):
    if audio:
        os.popen(
            f"""cd {os.path.split(__file__)[0]}/mpv && mpv -fs -audio=1 -loop --title="MyMpv" --cursor-autohide=no {VideoUrl}"""
        )
        Log.record("正常运行", f"Mpv Play -->> {VideoUrl}")
    else:
        os.popen(
            f"""cd {os.path.split(__file__)[0]}/mpv && mpv -fs -audio=0 -loop --title="MyMpv" --cursor-autohide=no {VideoUrl}"""
        )
        Log.record("正常运行", f"Mpv Play -->> {VideoUrl}")

def MpvUrlThread(VideoUrl, audio, kill, sleeptime):
    MPV = Thread(target=MpvUrlPlay, args=(VideoUrl, audio))
    MPV.start()
    MPV.join()
    time.sleep(sleeptime)
    try:
        Window_settings.main(f"MyMpv")
        UIDLOG(Window_settings._id_)
        Log.record("正常运行", "Settings：True")
    except:
        kill()
        Log.record("正常运行", "Settings：False")
        tkinter.messagebox.showinfo("错误！", "出现了一些非正常错误请重新启动程序尝试！")

"""本地视频播放"""
def PathPlay(Play_Video, width, height, audio):
    if audio == True:
        os.popen(
            f"cd {os.path.split(__file__)[0]}/and_ffmpeg/bin && ffplay -i {Play_Video} -loop 0 -threads 20 -x {width} -y {height} -noborder -window_title FFPlay：{Play_Video}")
    else:
        os.popen(
            f"cd {os.path.split(__file__)[0]}/and_ffmpeg/bin && ffplay -i {Play_Video} -an -loop 0 -threads 10 -x {width} -y {height} -noborder -window_title FFPlay：{Play_Video}")
    Log.record("正常运行", f"ffmpeg Play -->> {Play_Video}")

"""本地视频播放线程"""
def ThreadPlay(Play_Video, width, height, audio, kill, sleeptime):
    Th = Thread(target=PathPlay, args=(Play_Video, width, height, audio))
    Th.start()
    Th.join()
    time.sleep(sleeptime)
    try:
        Window_settings.main(f"FFPlay：{Play_Video}")
        UIDLOG(Window_settings._id_)
        Log.record("正常运行", "Settings：True")
    except:
        kill()
        Log.record("正常运行", "Settings：False")
        tkinter.messagebox.showinfo("错误！", "出现了一些非正常错误请重新启动程序尝试！")


"""网络视频播放"""
def UrlPlay(VideoUrl, VideoWidth, VideoHeight, Audio_Var):
    Get = requests.get(VideoUrl)
    if Get.status_code == 200:
        if Audio_Var == 1:
            os.popen(
                f"cd {os.path.split(__file__)[0]}/and_ffmpeg/bin && ffplay -threads 20 -loop 0 -noborder -x {VideoWidth} -y {VideoHeight} -window_title FFPlay：URL -i {VideoUrl}")
        else:
            os.popen(
                f"cd {os.path.split(__file__)[0]}/and_ffmpeg/bin && ffplay -threads 20 -loop 0 -noborder -x {VideoWidth} -y {VideoHeight} -window_title FFPlay：URL -an -i {VideoUrl}")
    else:
        tkinter.messagebox.showinfo("错误！", "请检查链接是否存在！")
    Log.record("正常运行", VideoUrl)

"""网络视频播放线程"""
def TreadUrlPlay(VideoUrl, VideoWidth, VideoHeight, Audio_Var, kill, sleeptime):
    Log.record("正常运行", f"{VideoUrl}, {VideoWidth,} {VideoHeight}, {Audio_Var}")
    Th = Thread(target=UrlPlay, args=(VideoUrl, VideoWidth, VideoHeight, Audio_Var))
    Th.start()
    Th.join()
    time.sleep(sleeptime)
    try:
        Window_settings.main(f"FFPlay：URL")
        UIDLOG(Window_settings._id_)
        Log.record("正常运行", "Settings：True")
    except:
        Log.record("正常运行", "Settings：False")
        kill()
        tkinter.messagebox.showinfo("错误！", "出现了一些非正常错误请重新启动程序尝试！")

"""读取指定路径图片的数据并返回为tkinter 可读数据"""
def open_img(img):
    return ImageTk.PhotoImage(Image.open(img))

"""读取缓存文件夹 Log 中的 log.log文件 如果不存在及创建文件"""
def open_log_json():
    Video = None
    """读取"""
    if os.path.exists(f"{os.path.split(__file__)[0]}/Log/log.log"):
        with open(f"{os.path.split(__file__)[0]}/Log/log.log", "r", encoding="utf-8") as f:
            Video = f.read()
    else:
        """创建"""
        with open(f"{os.path.split(__file__)[0]}/Log/log.log", "w+", encoding="utf-8") as f:
            f.write(str(None))
    return Video

"""写入缓存数据log.log文件（用于下次用户打开程序不需要再次选择视频文件）"""
def write_log_json(Path):
    with open(f"{os.path.split(__file__)[0]}/Log/log.log", "w+", encoding="utf-8") as f:
        f.write(Path)

"""uid缓存文件"""
def UIDLOG(UID):
    with open(f"{os.path.split(__file__)[0]}/log/UIDLOG.log", "w+", encoding="utf-8") as f:
        f.write(str(UID))
        return UID

def GetUid():
    with open(f"{os.path.split(__file__)[0]}/log/UIDLOG.log", "r", encoding="utf-8") as f:
        return int(f.read())

"""
主窗口类
self.tk tkinter窗口
self.Play_Video 读取log.log缓存数据
self.width 视频窗口宽度
self.height 视频窗口高度
self.audio 是否播放视频音乐
"""
class Mili_Wallpaper:

    def __init__(self):
        self.Play_Video = open_log_json()
        self.window_config = json.loads(open(f"{os.path.split(__file__)[0]}/Log/Window_configuration.json", "r+", encoding="utf-8").read())
        self.PlayerJson = json.loads(
            open(f"{os.path.split(__file__)[0]}/Log/PlayerSettings.json", "r+", encoding="utf-8").read()
        )

    """主窗口"""
    def main(self):
        self.tk = tkinter.Tk()
        swidth = self.tk.winfo_screenwidth()
        sheight = self.tk.winfo_screenheight()
        self.tk.geometry(f"800x400+{int((swidth - 800) / 2)}+{int((sheight - 400) / 2)}")
        self.tk.attributes('-alpha', self.window_config['窗口透明度'])
        sv_ttk.set_theme(self.window_config['窗口主题'])
        #sv_ttk.set_theme("dark")
        #sv_ttk.toggle_theme()
        PATH = os.path.split(__file__)[0]
        self.tk.title("Mili Wallpaper")
        self.tk.resizable(False, False)
        self.tk.iconbitmap(f"{PATH}/image/mili_wallpaper.ico")
        #self.tk.attributes('-alpha', 0.8)
        # self.tk.attributes('-toolwindow', 1)
        self.tk.protocol("WM_DELETE_WINDOW", self.destroy_all_gui)

        Bg = tkinter.Canvas(self.tk, width=800, height=400)
        BgPng = ImageTk.PhotoImage(Image.open(f"{os.path.split(__file__)[0]}/image/bg.png"))
        Bg.create_image(400, 200, image=BgPng)
        Bg.pack()

        canvas = tkinter.Canvas(self.tk, width=197, height=197)
        img = ImageTk.PhotoImage(Image.open(f"{os.path.split(__file__)[0]}/image/bg.jpg"))
        canvas.create_image(100, 100, image=img)
        canvas.place(x=100, y=100)

        self.width = self.tk.winfo_screenwidth()
        self.height = self.tk.winfo_screenheight()
        self.audio = False
        with open(f"{os.path.split(__file__)[0]}/Log/SelfStartingPlayConfig.wll", "r+", encoding="utf-8") as fp:
            if fp.read().split(";")[-1] == 'True':
                self.SelfStartingPlay = True
            else:
                self.SelfStartingPlay = False

        xMenu = tkinter.Menu(self.tk, tearoff=0, takefocus=False, activebackground='blue', activeforeground='yellow',borderwidth=20, relief=tkinter.RIDGE)
        xMenu.add_command(label='选择视频文件(ctrl+o)', command=self.Select_file)
        xMenu.add_command(label='启动动态壁纸(ctrl+p)', command=self.Play)
        xMenu.add_command(label='网络视频播放(ctrl+shift+p)', command=self.Play_Url_Video)
        xMenu.add_command(label='关闭视频壁纸(ctrl+k)', command=self.kill)
        xMenu.add_command(label='查看最新版(ctrl+v)', command=self.Version_update)
        xMenu.add_command(label='清除程序缓存(ctrl+c)', command=self.Clear_cache)
        xMenu.add_command(label="联系作者(ctrl+l)", command=self.Contact_Me)
        try:
            self.SetText = open(f"{os.path.split(__file__)[0]}/Log/SelfStartingPlayConfig.wll", "r", encoding="utf-8").read().split(';')[0]
        except:
            with open(f"{os.path.split(__file__)[0]}/Log/SelfStartingPlayConfig.wll", "r", encoding="utf-8") as fp:
                fp.write("关闭自启动壁纸;True")
            self.SetText = "关闭自启动壁纸"
        def Set_SelfStartingPlay():
            if self.SetText == "关闭自启动壁纸":
                open(f"{os.path.split(__file__)[0]}/Log/SelfStartingPlayConfig.wll", "w+", encoding="utf-8").write("开启自启动壁纸;False")
                tkinter.messagebox.showinfo("成功！", "重启后生效！")
            else:
                open(f"{os.path.split(__file__)[0]}/Log/SelfStartingPlayConfig.wll", "w+", encoding="utf-8").write("关闭自启动壁纸;True")
                tkinter.messagebox.showinfo("成功！", "重启后生效！")
        xMenu.add_command(label=self.SetText, command=Set_SelfStartingPlay)

        try:
            self.Starting = open(f"{os.path.split(__file__)[0]}/Log/Mili_Starting.wll", "r", encoding="utf-8").read().split(";")[0]
        except:
            with open(f"{os.path.split(__file__)[0]}/Log/Mili_Starting.wll", "r", encoding="utf-8") as fp:
                fp.write("关闭开机自启动;true")
            self.Starting = "关闭开机自启动"
        def add_starting():
            if self.Starting == "开启开机自启动":
                with open(f"{os.path.split(__file__)[0]}/Log/Mili_Starting.wll", "w+", encoding="utf-8") as fp:
                    fp.write("关闭开机自启动;true")
                tkinter.messagebox.showinfo("成功！", "重启后生效！")
            else:
                with open(f"{os.path.split(__file__)[0]}/Log/Mili_Starting.wll", "w+", encoding="utf-8") as fp:
                    fp.write("开启开机自启动;false")
                username = getpass.getuser()
                startup = fr"C:\Users\{username}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
                os.remove(startup + "\Mili_Starting.bat")
                Log.record("删除文件", startup + "\Mili_Starting.bat")
                tkinter.messagebox.showinfo("成功！", "重启后生效！")
        xMenu.add_command(label=self.Starting, command=add_starting)

        def xShowMenu(event):
            xMenu.post(event.x_root, event.y_root)

        self.tk.bind("<Button-3>", xShowMenu)
        self.tk.bind("<Control-Shift-KeyPress-K>", self.kill)
        self.tk.bind("<Control-o>", self.Select_file)
        self.tk.bind("<Control-p>", self.Play)
        self.tk.bind("<Control-P>", self.Play_Url_Video)
        self.tk.bind("<Control-V>", self.Version_update)
        self.tk.bind("<Control-c>", self.Clear_cache)
        self.tk.bind("<Control-l>", self.Contact_Me)
        self.tk.bind("<Control-q>", self.destroy_all_gui)
        self.tk.bind("<Control-s>", add_starting)

        Label(self.tk, text="右键菜单", bg="black", fg="white").place(x=1, y=1)
        Button(self.tk, text="选择视频文件", bg="black", fg="white", command=self.Select_file).place(x=10, y=350)
        Button(self.tk, text="关闭动态壁纸", bg="black", fg="white", command=self.kill).place(x=155, y=350)
        Button(self.tk, text="启动动态壁纸", bg="black", fg="white", command=self.Play).place(x=305, y=350)

        Label(self.tk, text="选择视频播放器：", bg="black", fg="white").place(x=450, y=45)
        self.comstring = StringVar()
        self.combobox = tkinter.ttk.Combobox(self.tk, textvariable=self.comstring, values=self.PlayerJson['Player'])
        self.combobox.current(0)
        self.combobox.place(x=560, y=40)

        Label(self.tk, text="抓取Bilibili视频：", bg="black", fg="white").place(x=450, y=155)
        self.BilibiliUrl = Text(self.tk, width=25, height=2)
        self.BilibiliUrl.place(x=550, y=150)
        Button(self.tk, text="抓取", command=self.GetBilibiliVideo).place(x=750, y=155)


        self.GetBilibiliJson = json.loads(open(f"{PATH}/Log/GetBilibili.json", "r", encoding="utf-8").read())
        Label(self.tk, text="请输入您的bilibili主页链接", bg="black", fg="white").place(x=450, y=250)
        self.bilibililink = Text(self.tk, width=22, height=5)
        self.bilibililink.insert("end", self.GetBilibiliJson['referer'])
        self.bilibililink.place(x=450, y=280)

        Label(self.tk, text="请输入您的bilibili主页cookie", bg="black", fg="white").place(x=630, y=250)
        self.bilibilicookie = Text(self.tk, width=23, height=5)
        self.bilibilicookie.insert("end", self.GetBilibiliJson['cookie'])
        self.bilibilicookie.place(x=630, y=280)

        self.Self_starting()
        self.Mili_Starting()
        self.tk.mainloop()

    def destroy_all_gui(self, event=False):
        sys.exit(0)
        self.tk.destory()

    """GetBilibiliVideo 获取b站视频"""
    def GetBilibiliVideo(self):
        if self.BilibiliUrl.get("1.0", "end").strip():
            if self.bilibililink.get("1.0", "end").strip():
                self.GetBilibiliJson["referer"] = f"{self.bilibililink.get('1.0', 'end').strip()}"
                if self.bilibilicookie.get("1.0", "end").strip():
                    self.GetBilibiliJson["cookie"] = f"{self.bilibilicookie.get('1.0', 'end').strip()}"
                    Log.record(
                        "正常运行",
                        f'Data -->> 视频链接：{self.BilibiliUrl.get("1.0", "end").strip()} 主页链接：{self.bilibililink.get("1.0", "end").strip()} 主页cookie：{self.bilibilicookie.get("1.0", "end").strip()}'
                    )
                    try:
                        self.Play_Video = GetBilibiliVideo.main(
                            self.BilibiliUrl.get("1.0", "end").strip(),
                            self.bilibililink.get("1.0", "end").strip(),
                            self.bilibilicookie.get("1.0", "end").strip(),
                            Log
                        )
                        write_log_json(self.Play_Video)
                        tkinter.messagebox.showinfo("成功!", "爬取成功！请选择启动壁纸")
                    except:
                        tkinter.messagebox.showinfo("失败!", "爬取失败！")
                    with open(f"{os.path.split(__file__)[0]}/Log/GetBilibili.json", "w+", encoding="utf-8") as fp:
                        fp.write(json.dumps(self.GetBilibiliJson))
                else:
                    tkinter.messagebox.showinfo("Cookie", "请输入您在b站主页cookie")
            else:
                tkinter.messagebox.showinfo("Link", "请输入您在b站主页的链接")
        else:
            tkinter.messagebox.showinfo("Video", "请输入您要抓取的视频链接")

    """选择视频文件函数"""
    def Select_file(self, event=False):
        try:
            self.kill()
        except:
            pass
        file = tkinter.Tk()
        file.withdraw()
        FilePath = tkinter.filedialog.askopenfilename(title="选择视频文件")
        write_log_json(FilePath)
        self.Play_Video = FilePath
        # Play_Video.main(FilePath)
        return FilePath

    def Self_starting(self):
        if self.SelfStartingPlay == True:
            if os.path.exists(open_log_json()):
                if os.path.exists(f"{os.path.split(__file__)[0]}/Log/VideoConfig.log"):
                    self.kill()
                    try:
                        with open(f"{os.path.split(__file__)[0]}/Log/VideoConfig.log", "r", encoding="utf-8") as fp:
                            config = fp.read().split(';')
                            Log.record("正常运行", config)
                            if config[-1] == 'True':
                                config[-1] = True
                            else:
                                config[-1] = False
                    except:
                        with open(f"{os.path.split(__file__)[0]}/Log/VideoConfig.log", "w+", encoding="utf-8") as fp:
                            fp.write(f"1080;1920;True")
                        config = [1080, 1920, True]
                    if self.combobox.get().strip() == "ffmpeg":
                        ThreadPlay(
                            Play_Video=self.Play_Video,
                            width=config[1],
                            height=config[0],
                            audio=config[-1],
                            kill=self.kill,
                            sleeptime=self.PlayerJson["delay_local"]
                        )
                    elif self.combobox.get().strip() == "mpv":
                        MpvTread(
                            Video=self.Play_Video,
                            audio=config[-1],
                            kill=self.kill,
                            sleeptime=self.PlayerJson["delay_local"]
                        )
                    else:
                        ThreadPlay(open_log_json(), config[1], config[0], config[-1], self.kill, self.PlayerJson["delay_local"])
                else:
                    with open(f"{os.path.split(__file__)[0]}/Log/VideoConfig.log", "w+", encoding="utf-8") as fp:
                        fp.write(f"1080;1920;True")
            else:
                Log.record("警告", "未找到视频文件！")
        else:
            Log.record("警告", f"自启动壁纸:{self.SelfStartingPlay}")


    """调用ffplay 播放视频函数"""
    def Play(self, event=False):
        self.kill()
        if os.path.exists(self.Play_Video):
            Play = tkinter.Toplevel()
            Play.title("Playback Settings")
            Play.geometry("400x200")
            Play.iconbitmap(f"{os.path.split(__file__)[0]}/image/mili_wallpaper.ico")
            Play.resizable(False, False)

            SleepTime = self.PlayerJson["delay_local"]
            def play():
                Log.record("正常运行", "Width"+self.width)
                Log.record("正常运行", "Height"+self.height)
                Log.record("正常运行", f"Audio{self.audio}")
                with open(f"{os.path.split(__file__)[0]}/Log/VideoConfig.log", "w+", encoding="utf-8") as fp:
                    fp.write(f"{self.height};{self.width};{self.audio}")
                if self.combobox.get().strip() == "ffmpeg":
                    ThreadPlay(self.Play_Video, self.width, self.height, self.audio, self.kill, SleepTime)
                elif self.combobox.get().strip() == "mpv":
                    MpvTread(self.Play_Video, self.audio, self.kill, SleepTime)
                else:
                    tkinter.messagebox.showinfo("请选择", "请选择一个播放器！")
                Play.destroy()

            """视频宽度"""
            Label(Play, text="设置视频宽度：", font=("", 10)).place(x=1, y=1)
            Width = Text(Play, width=10, height=1)
            Width.place(x=90, y=2)
            Width.insert("end", self.width)

            """视频高度"""
            Label(Play, text="设置视频高度：", font=("", 10)).place(x=1, y=25)
            Height = Text(Play, width=10, height=1)
            Height.place(x=90, y=25)
            Height.insert("end", self.height)

            """是否播放音乐"""
            Label(Play, text="是否播放音乐：", font=("", 10)).place(x=20, y=150)
            Audio_Var = IntVar(value=1)
            Audio = Checkbutton(Play, variable=Audio_Var)
            Audio.place(x=100, y=150)

            def And_Play_Bottun():
                self.width = Width.get("1.0", "end").strip()
                self.height = Height.get("1.0", "end").strip()
                if Audio_Var.get() == 1:
                    self.audio = True
                else:
                    self.audio = False
                play()

            Button(Play, text="确定", font=("", 20), command=And_Play_Bottun).place(x=200, y=60)

            Play.mainloop()
        else:
            self.Select_file()

    def Play_Url_Video(self, event=False):
        self.kill()
        Play_Url = tkinter.Toplevel()
        Play_Url.title("Play Url Video")
        Play_Url.geometry("400x200")
        Play_Url.iconbitmap(f"{os.path.split(__file__)[0]}/image/mili_wallpaper.ico")
        Play_Url.resizable(False, False)

        """URL"""
        Label(Play_Url, text="网页视频链接：", font=("", 10)).place(x=1, y=1)
        VideoUrl = Text(Play_Url, width=20, height=2)
        VideoUrl.place(x=90, y=2)

        """视频宽度"""
        Label(Play_Url, text="网页视频宽度：", font=("", 10)).place(x=1, y=40)
        VideoWidth = Text(Play_Url, width=10, height=1)
        VideoWidth.place(x=90, y=40)
        VideoWidth.insert("end", self.width)

        """视频高度"""
        Label(Play_Url, text="网页视频高度：", font=("", 10)).place(x=1, y=60)
        VideoHeight = Text(Play_Url, width=10, height=1)
        VideoHeight.place(x=90, y=60)
        VideoHeight.insert("end", self.height)

        """是否播放音乐"""
        Label(Play_Url, text="是否播放音乐：", font=("", 10)).place(x=20, y=150)
        Audio_Var = IntVar(value=1)
        Audio = Checkbutton(Play_Url, variable=Audio_Var)
        Audio.place(x=100, y=150)

        SleepTime = self.PlayerJson["delay_network"]
        def Play():
            if self.combobox.get() == "ffmpeg":
                TreadUrlPlay(VideoUrl.get('0.0', 'end').strip(), VideoWidth.get('0.0', 'end').strip(), VideoHeight.get('0.0', 'end').strip(), Audio_Var.get(), self.kill, SleepTime)
            elif self.combobox.get() == "mpv":
                MpvUrlThread(VideoUrl.get('0.0', 'end').strip(), Audio_Var.get(), self.kill, SleepTime)
            else:
                tkinter.messagebox.showinfo("请选择", "请选择一个播放器！")

            Play_Url.destroy()
        Button(Play_Url, text="确定", font=("", 20), command=Play).place(x=250, y=130)

    """联系我二维码"""
    def Contact_Me(self, event=False):
        ContactMe = tkinter.Toplevel()
        ContactMe.iconbitmap(f"{os.path.split(__file__)[0]}/image/mili_wallpaper.ico")
        ContactMe.title("联系我")
        ContactMe.geometry("800x800")
        canvas = tkinter.Canvas(ContactMe, width=750, height=800)
        img = ImageTk.PhotoImage(Image.open(f"{os.path.split(__file__)[0]}/image/QQ.jpg"))
        canvas.create_image(380, 480, image=img)
        canvas.pack()
        ContactMe.mainloop()

    def Mili_Starting(self, event=False):
        username = getpass.getuser()
        startup = fr"C:\Users\{username}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
        try:
            startwll = open(f"{os.path.split(__file__)[0]}/Log/Mili_Starting.wll", "r", encoding="utf-8").read().split(";")[-1]
        except:
            open(f"{os.path.split(__file__)[0]}/Log/Mili_Starting.wll", "w+", encoding="utf-8").write("关闭开机自启动;true")
            startwll = "true"
        if startwll == "true":
            if os.path.exists(startup):
                with open(startup+"\Mili_Starting.bat", "w+", encoding="utf-8") as fp:
                    fp.write(f"python {__file__}")
                Log.record("正常运行", "开机自启动已打开")
            else:
                tkinter.messagebox.showinfo("错误！", "无法开启开机自启动")
                Log.record("错误", startup+"不存在")
        else:
            if os.path.exists(startup+"\Mili_Starting.bat"):
                os.remove(startup+"\Mili_Starting.bat")
                Log.record("删除文件", startup+"\Mili_Starting.bat")
            else:
                Log.record("未找到自启动文件", startup+"\Mili_Starting.bat")


    """杀死所有窗口句柄"""
    def kill(self, event=False):
        Log.record("正常运行", self.Play_Video)
        try:
            win32gui.PostMessage(GetUid(), win32con.WM_CLOSE, 0, 0)
            win32gui.PostMessage(Window_settings.get_hwnd_from_name(f"{self.Play_Video} 预览"), win32con.WM_CLOSE, 0, 0)
        except:
            pass

    """版本查询"""
    def Version_update(self, event=False):
        req = requests.get(url="https://www.kuko.icu/API/MiliWallpaper/Updata.json")
        if req.status_code == 200:
            for key, value in req.json().items():
                if __Version__ == key:
                    tkinter.messagebox.showinfo("程序已是最新版本！", f"程序已是最新版本！{key}")
                else:
                    tkinter.messagebox.showinfo("当前程序不是最新版本", f"程序最新下载地址：{value}")
                    os.system(f"start {value}")
        else:
            tkinter.messagebox.showinfo("Error", "服务器可能在维护！")

    """清除程序缓存"""
    def Clear_cache(self, event=False):
        self.kill()
        UIDLOG(None)
        with open(f"{os.path.split(__file__)[0]}/Log/log.log", "w+", encoding="utf-8") as f:
            f.write(str(None))
        open(f"{os.path.split(__file__)[0]}/Log/VideoConfig.log", "w+", encoding="utf-8").write("1080;1920;True")
        open(f"{os.path.split(__file__)[0]}/Log/SelfStartingPlayConfig.wll", "w+", encoding="utf-8").write("关闭自启动壁纸;True")
        open(os.path.split(__file__)[0]+"/Log/journal.log", "w+", encoding="utf-8")
        open(f"{os.path.split(__file__)[0]}/Log/Mili_Starting.wll", "w+", encoding="utf-8").write("开启开机自启动;false")
        getbilbilijson = {
            "referer":"",
            "cookie":""
        }
        open(f"{os.path.split(__file__)[0]}/Log/GetBilibili.json", "w+", encoding="utf-8").write(json.dumps(getbilbilijson))
        for paths, dirs, files in os.walk(f"{os.path.split(__file__)[0]}/Log/BilibiliLogVideo"):
            if files:
                for file in files:
                    os.remove(paths+"/"+file)
                    print(f"删除文件 -->> {paths}/{file}")
        self.Play_Video = "None"
        tkinter.messagebox.showinfo("清除缓存", "已清除程序所有缓存！")

if __name__ in "__main__":
    Mili_Wallpaper().main()