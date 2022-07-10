"""Gui"""
import random

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
import json
import cv2
import sys

"""pywin32"""
import time
import win32gui
from win32.lib import win32con
import requests
import winreg
from threading import Thread

"""自定义库"""
import Window_settings
import ProgramLog
import GetBilibiliVideo

Log = ProgramLog.Logging(os.path.split(__file__)[0]+"/Log/journal.log")

try:
    __Version__ = open(f"{os.path.split(__file__)[0]}/Log/Version.wll", "r", encoding="utf-8").read()
except:
    with open(f"{os.path.split(__file__)[0]}/Log/Version.wll", "r", encoding="utf-8") as fp:
        fp.write("1.8")
    __Version__ = open(f"{os.path.split(__file__)[0]}/Log/Version.wll", "r", encoding="utf-8").read()

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

"""本地视频播放"""
def PathPlay(Play_Video, width, height, audio):
    global _IF_PLAY_
    if audio == True:
        os.popen(
            f"cd {os.path.split(__file__)[0]}/ && ffplay -x {width} -y {height} -i {Play_Video} -loop 0 -threads 20 -noborder -window_title FFPlay：{Play_Video}")
    else:
        os.popen(
            f"cd {os.path.split(__file__)[0]}/ && ffplay -x {width} -y {height} -i {Play_Video} -an -loop 0 -threads 10 -noborder -window_title FFPlay：{Play_Video}")
    Log.record("正常运行", f"ffmpeg Play -->> {Play_Video}")
    _IF_PLAY_ = True

"""本地视频播放线程"""
def ThreadPlay(Play_Video, width, height, audio, kill, sleeptime):
    Th = Thread(target=PathPlay, args=(Play_Video, width, height, audio))
    Th.start()
    Th.join()
    time.sleep(sleeptime)
    while True:
        try:
            Window_settings.main(f"FFPlay：{Play_Video}")
            UIDLOG(Window_settings._id_)
            Log.record("正常运行", "Settings：True")
            break
        except:
            continue


"""网络视频播放"""
def UrlPlay(VideoUrl, VideoWidth, VideoHeight, Audio_Var):
    Get = requests.get(VideoUrl)
    if Get.status_code == 200:
        if Audio_Var == 1:
            os.popen(
                f"cd {os.path.split(__file__)[0]}/ && ffplay -threads 20 -loop 0 -noborder -x {VideoWidth} -y {VideoHeight} -window_title FFPlay：URL -i {VideoUrl}")
        else:
            os.popen(
                f"cd {os.path.split(__file__)[0]}/ && ffplay -threads 20 -loop 0 -noborder -x {VideoWidth} -y {VideoHeight} -window_title FFPlay：URL -an -i {VideoUrl}")
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
    while True:
        try:
            Window_settings.main(f"FFPlay：URL")
            UIDLOG(Window_settings._id_)
            Log.record("正常运行", "Settings：True")
            break
        except:
            continue

def PlayVideoLabel(cap, Labels):
    try:
        _, frame = cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        frame_image = Image.fromarray(cv2image).resize((960, 540))
        frame_image = ImageTk.PhotoImage(frame_image)
        Labels.config(image=frame_image)
        Labels.image = frame_image
        Labels.after(1, lambda: PlayVideoLabel(cap, Labels))
    except:
        Labels.close()
        return

def ImageWallpaper(Image=False, Images=False, SleepTime=False, Random=False):
    if Image:
        os.popen(f"cd {os.path.split(__file__)[0]}/PictureWallpaper && PictureWallpaper.exe --Image={Image}")
        print(f"cd {os.path.split(__file__)[0]}/PictureWallpaper && PictureWallpaper.exe --Image={Image}")
    elif Images:
        InitImages = ",".join(Images)
        os.popen(f"cd {os.path.split(__file__)[0]}/PictureWallpaper && PictureWallpaper.exe --Images={InitImages} --SleepTime={SleepTime} --Random=={Random}")
        print(f"cd {os.path.split(__file__)[0]}/PictureWallpaper && PictureWallpaper.exe --Images={InitImages} --SleepTime={SleepTime} --Random=={Random}")

def ImageWallpaperThread(Image=False, Images=False, SleepTime=False, Random=False):
    Wall = Thread(target=ImageWallpaper, args=(Image, Images, SleepTime, Random))
    Wall.start()
    Wall.join()


"""
主窗口类
"""
class Mili_Wallpaper:

    def __init__(self):
        self.Play_Video = open_log_json()
        self.window_config = json.loads(open(f"{os.path.split(__file__)[0]}/Log/Window_configuration.json", "r+", encoding="utf-8").read())
        self.PlayerJson = json.loads(
            open(f"{os.path.split(__file__)[0]}/Log/PlayerSettings.json", "r+", encoding="utf-8").read()
        )
        self.GetBilibiliJson = json.loads(open(f"{os.path.split(__file__)[0]}/Log/GetBilibili.json", "r+", encoding="utf-8").read())

    """主窗口"""
    def main(self):
        self.tk = tkinter.Tk()
        swidth = self.tk.winfo_screenwidth()
        sheight = self.tk.winfo_screenheight()
        self.tk.geometry(f"1000x600+{int((swidth - 1000) / 2)}+{int((sheight - 600) / 2)}")
        self.tk.attributes('-alpha', self.window_config['Window transparency'])
        sv_ttk.set_theme(self.window_config['Window theme'])
        #sv_ttk.set_theme("dark")
        #sv_ttk.toggle_theme()
        PATH = os.path.split(__file__)[0]
        self.tk.title("Mili Wallpaper")
        self.tk.resizable(False, False)
        self.tk.iconbitmap(f"{PATH}/image/mili_wallpaper.ico")
        #self.tk.attributes('-alpha', 0.8)
        # self.tk.attributes('-toolwindow', 1)
        self.tk.protocol("WM_DELETE_WINDOW", self.destroy_all_gui)

        Bg = tkinter.Canvas(self.tk, width=1000, height=600)
        if self.window_config['Window background'] == "/image/heis.jpg":
            BgPngPath = f"{os.path.split(__file__)[0]}{self.window_config['Window background']}"
        else:
            BgPngPath = self.window_config['Window background']
        BgPng = ImageTk.PhotoImage(Image.open(BgPngPath).resize((1000, 600)))
        Bg.create_image(500, 300, image=BgPng)
        Bg.pack()

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
        xMenu.add_command(label="更改软件背景(ctrl+shift+b)", command=self.ChangeBackgroundPicture)
        xMenu.add_command(label="选择图片文件(ctrl+shift+i)", command=self.ImageWallpaper)
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
                self.Mili_Starting()
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
        self.tk.bind("<Control-I>", self.ImageWallpaper)

        Label(self.tk, text="右键菜单", bg="black", fg="white").place(x=1, y=1)
        Button(self.tk, text="选择视频文件", bg="black", fg="white", command=self.Select_file).place(x=40, y=550)
        Button(self.tk, text="关闭动态壁纸", bg="black", fg="white", command=self.kill).place(x=150, y=550)
        Button(self.tk, text="启动动态壁纸", bg="black", fg="white", command=self.Play).place(x=260, y=550)
        Button(self.tk, text="通过VideoList视频id获取壁纸", command=self.VideoList).place(x=415, y=550)
        Label(self.tk, text="抓取Bilibili视频：", bg="black", fg="white").place(x=650, y=550)
        self.BilibiliUrl = Text(self.tk, width=25, height=2)
        self.BilibiliUrl.place(x=750, y=550)
        Button(self.tk, text="抓取", command=self.GetBilibiliVideo).place(x=950, y=550)

        self.Self_starting()
        self.Mili_Starting()
        self.tk.mainloop()

    def destroy_all_gui(self, event=False):
        sys.exit(0)
        self.tk.destory()

    """PictureWallpaper"""
    def ImageWallpaper(self, event=False):
        PATH = os.path.split(__file__)[0]
        self.ImagePath = False
        self.ImagesPath = []

        ImgWall = Toplevel()
        ImgWall.resizable(False, False)
        ImgWall.geometry("960x540")
        ImgWall.iconbitmap(f"{PATH}/image/mili_wallpaper.ico")

        BgImage = Canvas(ImgWall, width=960, height=540)
        BgImage.pack()

        def FileOPen():
            global Bg
            OpenFile = tkinter.filedialog.askopenfilename(title="选择壁纸")
            if os.path.exists(OpenFile):
                self.ImagePath = OpenFile
                Bg = ImageTk.PhotoImage(Image.open(self.ImagePath).resize((960, 540)))
                BgImage.create_image(int(960 / 2), int(540 / 2), image=Bg)
            else:
                tkinter.messagebox.showinfo("错误！", "文件不存在！")
        Button(ImgWall, text="选择单文件壁纸", bg="black", fg="white", command=FileOPen).place(x=0, y=0)
        def FilesOpen():
            global Bg
            OpenFile = tkinter.filedialog.askopenfilenames(title="选择多个壁纸")
            for file in OpenFile:
                if os.path.exists(file):
                    self.ImagesPath.append(file)
                    Bg = ImageTk.PhotoImage(Image.open(file).resize((960, 540)))
                    BgImage.create_image(int(960 / 2), int(540 / 2), image=Bg)
                    ImgWall.update()
                else:
                    continue
        Button(ImgWall, text="选择多文件壁纸", bg="black", fg="white", command=FilesOpen).place(x=120, y=0)

        """是否随机"""
        Label(ImgWall, text="是否随机", bg="black", fg="white").place(x=250, y=0)
        self.Random_Var = IntVar(value=1)
        Random = Checkbutton(ImgWall, variable=self.Random_Var)
        Random.place(x=310, y=1)

        Label(ImgWall, text="设置切换壁纸间隔：", bg="black", fg="white").place(x=350, y=0)
        self.SleepTimeText = Text(ImgWall, height=1, width=10)
        self.SleepTimeText.insert("end", 10)
        self.SleepTimeText.place(x=474, y=0)

        def SetWall():
            print(self.ImagePath, self.ImagesPath, self.Random_Var.get(), self.SleepTimeText.get("1.0", "end").strip())
            if self.ImagePath:
                ImageWallpaperThread(Image=self.ImagePath)
                self.ImagesPath = False
            elif len(self.ImagesPath) != 0:
                if self.Random_Var.get() == 1:
                    ImageWallpaperThread(Images=self.ImagesPath, Random=True, SleepTime=self.SleepTimeText.get("1.0", "end").strip())
                else:
                    ImageWallpaperThread(Images=self.ImagesPath, Random=False, SleepTime=self.SleepTimeText.get("1.0", "end").strip())
            else:
                tkinter.messagebox.showinfo("错误", "未知错误！")
        Button(ImgWall, text="确定", bg="black", fg="white", command=SetWall).place(x=555, y=0)

        def KillImageWallpaper():
            UID = open(f"{PATH}/PictureWallpaper/Log/ImageWallpaper.log", "r", encoding="utf-8").read()
            while True:
                try:
                    win32gui.PostMessage(UID, win32con.WM_CLOSE, 0, 0)
                except:
                    break
        Button(ImgWall, text="关闭", bg="black", fg="white", command=KillImageWallpaper).place(x=600, y=0)

        ImgWall.mainloop()

    """判断是否有参数"""
    def GetBiliIF(self):
        self.biliif = Toplevel()
        PATH = os.path.split(__file__)[0]
        self.GetBilibiliJson = json.loads(open(f"{PATH}/Log/GetBilibili.json", "r", encoding="utf-8").read())
        Label(self.biliif, text="请输入您的bilibili主页链接", bg="black", fg="white").pack()
        self.bilibililink = Text(self.biliif, width=22, height=5)
        self.bilibililink.insert("end", self.GetBilibiliJson['referer'])
        self.bilibililink.pack()

        Label(self.biliif, text="请输入您的bilibili主页cookie", bg="black", fg="white").pack()
        self.bilibilicookie = Text(self.biliif, width=23, height=5)
        self.bilibilicookie.insert("end", self.GetBilibiliJson['cookie'])
        self.bilibilicookie.pack()

        def OK():
            self.GetBilibiliJson['referer'] = self.bilibililink.get("1.0", "end").strip()
            self.GetBilibiliJson['cookie'] = self.bilibilicookie.get("1.0", "end").strip()
            with open(f"{os.path.split(__file__)[0]}/Log/GetBilibili.json", "r+", encoding="utf-8") as fp:
                fp.write(json.dumps(self.GetBilibiliJson))
            self.biliif.destroy()
        Button(self.biliif, text="确定", bg="black", fg="white", command=OK).pack()
        self.biliif.mainloop()

    """VideoList"""
    def VideoList(self, event=False):
        Get = requests.get("https://www.kuko.icu/Mili_Wallpaper/")
        if Get.status_code == 200:
            videlist = Toplevel()
            videlist.title("VideoList")
            videlist.geometry("960x540")
            videlist.iconbitmap(f"{os.path.split(__file__)[0]}/image/mili_wallpaper.ico")
            videlist.resizable(False, False)

            videolistbg = Label(videlist)
            videolistbg.pack()

            Label(videlist, text="请输入图片id：", bg="black", fg="white").place(x=10, y=12)
            id = Text(videlist, width=10, height=2)
            id.place(x=100, y=10)

            def getvideo():
                global Bgjpg
                path = os.path.split(__file__)[0]
                ID = id.get("1.0", "end").strip()
                Get = requests.get("https://www.kuko.icu/Mili_Wallpaper/API.json")
                if Get.status_code == 200:
                    try:
                        URL = "https://www.kuko.icu/Mili_Wallpaper/img/" + Get.json()[ID].split('.')[0] + ".jpg"
                        print(URL)
                        GetImage = requests.get(URL)
                        if GetImage.status_code == 200:
                            open(f"{path}/Log/VideoList/log.jpg", "wb").write(GetImage.content)
                            Bgjpg = ImageTk.PhotoImage(Image.open(f"{path}/Log/VideoList/log.jpg").resize((960, 540)))
                            videolistbg['image'] = Bgjpg
                            print(f"https://www.kuko.icu/Mili_Wallpaper/video/{Get.json()[ID]}")
                            GetVideo = requests.get(f"https://www.kuko.icu/Mili_Wallpaper/video/{Get.json()[ID]}")
                            if GetVideo.status_code == 200:
                                open(f"{path}/Log/VideoList/log.mp4", "wb").write(GetVideo.content)
                                tkinter.messagebox.showinfo("获取成功！", "获取成功！")
                            else:
                                tkinter.messagebox.showinfo("错误！", "未知错误！")
                        else:
                            tkinter.messagebox.showinfo("错误！", "未知错误！")
                    except KeyError:
                        tkinter.messagebox.showinfo("未找到", "未找到相应壁纸,请检查id是否错误！")
                else:
                    tkinter.messagebox.showinfo("服务器错误", "服务器错误，请等待管理员维护！")

            def SetPlay(Self=self):
                if os.path.exists(f"{os.path.split(__file__)[0]}/Log/VideoList/log.mp4"):
                    videlist.quit()
                    videlist.destroy()
                    Self.Play_Video = f"{os.path.split(__file__)[0]}/Log/VideoList/log.mp4"
                    write_log_json(f"{os.path.split(__file__)[0]}/Log/VideoList/log.mp4")
                    Self.Play()
                else:
                    tkinter.messagebox.showinfo("请获取", "请先获取到资源！")

            Button(videlist, text="获取", bg="black", fg="white", command=getvideo).place(x=180, y=10)
            Button(videlist, text="设置此壁纸", bg="black", fg="white", command=SetPlay).place(x=250, y=10)

            videlist.mainloop()
        else:
            tkinter.messagebox.showinfo("服务器错误", "服务器发生错误，请等待管理员维护！")


    """软件背景 Change background picture"""
    def ChangeBackgroundPicture(self, event=False):
        file = tkinter.Tk()
        file.withdraw()
        FilePath = tkinter.filedialog.askopenfilename(title="选择背景图片")
        if os.path.exists(FilePath):
            self.window_config['Window background'] = FilePath
            with open(f"{os.path.split(__file__)[0]}/Log/Window_configuration.json", "w+", encoding="utf-8") as fp:
                fp.write(json.dumps(self.window_config))

            tkinter.messagebox.showinfo("成功", "设置成功重启程序即可更换")
        else:
            pass

    """GetBilibiliVideo 获取b站视频"""
    def GetBilibiliVideo(self):
        if self.BilibiliUrl.get("1.0", "end").strip():
            if self.GetBilibiliJson['referer'].strip() != "None":
                if self.GetBilibiliJson["cookie"].strip() != "None":
                    Log.record(
                        "正常运行",
                        f'Data -->> 视频链接：{self.GetBilibiliJson["referer"]} 主页链接：{self.BilibiliUrl.get("1.0", "end").strip()} 主页cookie：{self.GetBilibiliJson["cookie"]}'
                    )
                    try:
                        self.Play_Video = GetBilibiliVideo.main(
                            self.BilibiliUrl.get("1.0", "end").strip(),
                            self.GetBilibiliJson["referer"],
                            self.GetBilibiliJson["cookie"],
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
                    self.GetBiliIF()
            else:
                tkinter.messagebox.showinfo("Link", "请输入您在b站主页的链接")
                self.GetBiliIF()
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
                    ThreadPlay(
                        Play_Video=self.Play_Video,
                        width=config[1],
                        height=config[0],
                        audio=config[-1],
                        kill=self.kill,
                        sleeptime=self.PlayerJson["delay_local"]
                        )
                else:
                    with open(f"{os.path.split(__file__)[0]}/Log/VideoConfig.log", "w+", encoding="utf-8") as fp:
                        fp.write(f"1080;1920;True")
            else:
                Log.record("警告", "未找到视频文件！")
        else:
            Log.record("警告", f"自启动壁纸:{self.SelfStartingPlay}")


    """调用ffplay 播放视频函数"""
    def Play(self, event=False):
        self.width = str(self.tk.winfo_screenwidth())
        self.height = str(self.tk.winfo_screenheight())
        self.kill()
        if os.path.exists(self.Play_Video):
            Play = tkinter.Toplevel()
            Play.title("Playback Settings")
            Play.geometry("960x540")
            Play.iconbitmap(f"{os.path.split(__file__)[0]}/image/mili_wallpaper.ico")
            Play.resizable(False, False)

            SleepTime = self.PlayerJson["delay_local"]
            def play():
                Log.record("正常运行", "Width"+self.width)
                Log.record("正常运行", "Height"+self.height)
                Log.record("正常运行", f"Audio{self.audio}")
                with open(f"{os.path.split(__file__)[0]}/Log/VideoConfig.log", "w+", encoding="utf-8") as fp:
                    fp.write(f"{self.height};{self.width};{self.audio}")
                ThreadPlay(self.Play_Video, self.width, self.height, self.audio, self.kill, SleepTime)
                Play.destroy()

            bgvideo = Label(Play)
            bgvideo.pack()
            cap = cv2.VideoCapture(self.Play_Video)
            PlayVideoLabel(cap, bgvideo)

            """是否播放音乐"""
            Label(Play, text="是否播放音乐：", font=("", 10), bg="black", fg="white").place(x=1, y=2)
            Audio_Var = IntVar(value=1)
            Audio = Checkbutton(Play, variable=Audio_Var)
            Audio.place(x=100, y=1)

            def And_Play_Bottun():
                if Audio_Var.get() == 1:
                    self.audio = True
                else:
                    self.audio = False
                play()

            Button(Play, text="确定", command=And_Play_Bottun, bg="black", fg="white").place(x=150, y=1)

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
        Label(Play_Url, text="网页视频链接", font=("", 10), bg="black", fg="white").place(x=1, y=1)
        VideoUrl = Text(Play_Url, width=20, height=2)
        VideoUrl.place(x=0, y=20)

        """是否播放音乐"""
        Label(Play_Url, text="是否播放音乐：", font=("", 10)).place(x=20, y=150)
        Audio_Var = IntVar(value=1)
        Audio = Checkbutton(Play_Url, variable=Audio_Var)
        Audio.place(x=100, y=150)

        SleepTime = self.PlayerJson["delay_network"]
        def Play():
            TreadUrlPlay(VideoUrl.get('0.0', 'end').strip(), self.width, self.height, Audio_Var.get(), self.kill, SleepTime)
            Play_Url.destroy()
        Button(Play_Url, text="确定", font=("", 20), command=Play, bg="black", fg="white").place(x=250, y=130)

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
                    fp.write(f"start {os.path.split(__file__)[0]}/Mili_Wallpaper.exe")
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
            # win32gui.PostMessage(Window_settings.get_hwnd_from_name(f"{self.Play_Video} 预览"), win32con.WM_CLOSE, 0, 0)
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
            "referer":"None",
            "cookie":"None"
        }
        open(f"{os.path.split(__file__)[0]}/Log/GetBilibili.json", "w+", encoding="utf-8").write(json.dumps(getbilbilijson))
        for paths, dirs, files in os.walk(f"{os.path.split(__file__)[0]}/Log/BilibiliLogVideo"):
            if files:
                for file in files:
                    try:
                        os.remove(paths+"/"+file)
                        print(f"删除文件 -->> {paths}/{file}")
                    except:
                        continue

        windowsconfig = {
            "Window transparency": 1,
            "Window theme": "light",
            "Window background":"/image/heis.jpg"
        }
        open(f"{os.path.split(__file__)[0]}/Log/Window_configuration.json", "w+", encoding="utf-8").write(json.dumps(windowsconfig))

        while True:
            try:
                if os.path.exists(f"{os.path.split(__file__)[0]}/Log/VideoList/log.mp4"):
                    os.remove(f"{os.path.split(__file__)[0]}/Log/VideoList/log.mp4")
                    os.remove(f"{os.path.split(__file__)[0]}/Log/VideoList/log.jpg")
                else:
                    break
            except:
                pass

        self.Play_Video = "None"
        tkinter.messagebox.showinfo("清除缓存", "已清除程序所有缓存！")

if __name__ in "__main__":
    Mili_Wallpaper().main()