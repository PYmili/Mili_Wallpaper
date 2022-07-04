# Mili_Wallpaper

![Mili_Wallpaper](./image/mili_wallpaper.ico) Mili_Wallpaper 使用 Python 和 tkinter-gui库开发制作的桌面动态壁纸程序

[Mili_Wallpaper](https://www.kuko.icu/Mili_Wallpaper)

# 作者 PYmili
![PYmili](./image/PYmili_400x400.jpg)
### 官网网址：[kuko.icu](https://www.kuko.icu) 个人博客：[mpen](http://mpen.natapp1.cc)

# 非常感谢 !!!
### https://github.com/mpv-player/mpv Mpv
### https://github.com/FFmpeg/FFmpeg FFmpeg
### 程序的播放器现支持 FFmpeg 与 Mpv 播放
# 此地址仓库没有上传ffmpeg及mpv请到这里下载：https://gitcode.net/qq_53280175/mili_wallpaper

后期会相应更新其他播放器，欢迎投稿!

# 联系方式
### QQ:2097632843
### QQ群：706128290

如有新增bug请截屏发群。
程序下载地址：https://www.kuko.icu/API/MiliWallpaper/Mili_Wallpaper_Version/

# 使用环境
### 此程序只对于windows10进行维护与开发，并不支持windows7,8,11 或许能够正常运行但是会出现部分"未解之谜"
程序可选择本地视频路径作为壁纸，也可填写完整的url链接作为壁纸

请使用管理员权限运行程序！！！以免发生"未解之谜"

建议将程序安装到C盘以外的文件夹

___

# 文件介绍
## Mili_Wallpaper\Log\GetBilibili.json
此文件将存储您输入的b站主页链接及其cookie值
```
{
    "referer": "", # b站主页链接
    "cookie": "" # cookie值
}
```

清除程序缓存后会自动清空数据并还原原貌

---

## Mili_Wallpaper\Log\journal.log
此文件将用于存储程序产生的日志，可供查看错误

清除程序缓存后会自动清空数据并还原原貌

---

## Mili_Wallpaper\Log\log.log
此文件将用于存储上次用户选择的视频文件路径(仅本地视频)

清除程序缓存后会自动清空数据并还原原貌

---

## Mili_Wallpaper\Log\Mili_Starting.wll
此文件将存储程序开启自启动程序开关
```
开启开机自启动;false # true为打开，false为关闭
```

清除程序缓存后会自动清空数据并还原原貌

---

## Mili_Wallpaper\Log\PlayerSettings.json
此文件将存储播放器的基本设置

```
{
  "Player": [
    "ffmpeg",
    "mpv"
  ], # 播放器列表
  "use": "ffmpeg", # 默认播放器
  "delay_local": 3, # 播放器本地播放视频默认加载时间
  "delay_network": 3 # 播放器网络播放视频默认加载时间
}
```

如果出现播放错误的问题可以尝试将默认加载时间设置3以上

清除程序缓存后不会自动清空数据并还原原貌

---

## Mili_Wallpaper\Log\SelfStartingPlayConfig.wll
此文件将存储程序自启动壁纸缓存文件

清除程序缓存后会自动清空数据并还原原貌

---

## Mili_Wallpaper\Log\UIDLOG.log
此文件将存储程序获取到播放器窗口句柄

清除程序缓存后会自动清空数据并还原原貌

---

## Mili_Wallpaper\Log\Version.wll
此文件将存储程序的版本信息

清除程序缓存后不会自动清空数据并还原原貌

---

## Mili_Wallpaper\Log\VideoConfig.log
此文件将存储用户启动壁纸的播放设置并记录

清除程序缓存后会自动清空数据并还原原貌

---

## Mili_Wallpaper\Log\Window_configuration.json
此文件将控制程序的主题

```
{
  "Window transparency": 1, # 窗口透明度
  "Window theme": "light", # 窗口主题
  "Window background": "/image/bg.png" # 窗口背景图
}
```

清除程序缓存后不会自动清空数据并还原原貌

---

## Mili_Wallpaper\Log\BilibiliLogVideo
此文件夹将存储从b站上抓取到的视频

清除程序缓存后会自动清空数据并还原原貌

___
# 功能

### 1.播放本地视频

程序可以选择本地视频播放视频 可自行选择播放器 (ffmpeg/mpv)

根据本地视频画质绝对占用内存量, 壁纸将视频的原像素播放

ffmpeg可以选择播放视频的尺寸，mpv将强制全屏

---

### 2.播放网络视频

程序可以播放网络视频，根据网络网速及目标方网速决定视频流畅度

ffmpeg可以选择播放视频的尺寸，mpv将强制全屏

---

### b站视频抓取

程序可以通过脚本抓取到指定b站视频链接中的mp4视频

需要用户填写个人主页链接及cookie值(程序会自动保存，清除缓存后清空)

---
