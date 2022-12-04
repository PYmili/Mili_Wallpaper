# Mili_Wallpaper

![Mili_Wallpaper](https://www.kuko.icu/static/MiliWallpaper/Mili_Wallpaper_Version/img/mili_wallpaper.ico) 

<font color=blue>Mili_Wallpaper 使用 Python 和 tkinter-gui库开发制作的桌面动态壁纸程序</font>

[![OSCS Status](https://www.oscs1024.com/platform/badge/PYmili/Mili_Wallpaper.svg?size=small)](https://www.oscs1024.com/project/PYmili/Mili_Wallpaper?ref=badge_small)

# 作者 PYmili
![PYmili](https://profile-avatar.csdnimg.cn/414f7b0a2036498bab4e37580fca6377_qq_53280175.jpg!1)

 <font color=yellow>官网网址：</font>[kuko.icu](https://www.kuko.icu/Mili_Wallpaper) 个人博客：[mpen](https://blog.csdn.net/qq_53280175?spm=1000.2115.3001.5343)
---

# 重大更新

- 2.8

  此次更新修复了当ffmpeg视频窗口播放视频时，点击 <font color=red>Windows 任务视窗</font> 出现壁纸显示问题。
更改了<font color=red>Windows_setting.py</font>文件中壁纸实现方法。旧版本都是将视频窗口，设置为PM窗口的子窗口实现壁纸。
这次更改实现方法，将视频窗口设置到<font color=red>WorkerW</font>下的子<font color=red>WorkerW</font>窗口中。

## 非常感谢 !!!
- [FFmpeg](https://github.com/FFmpeg/FFmpeg)
### 程序的播放器实现基于 FFmpeg
---

## <font color=yellow>联系方式
- QQ:2097632843
- QQ群：706128290

如有新增bug请截屏发群。
程序下载地址：</font>[Mili Wallpaper Version](https://www.kuko.icu/API/MiliWallpaper/)
---

# 使用环境
### 已支持环境
- <font color=#008000>Window 10 x64 / x86</font>
- <font color=#008000>Window 11 x64 / x86</font>

<font color=red>X86位exe包及程序兼容x64位。</font>

程序可选择本地视频路径作为壁纸，也可填写完整的url链接作为壁纸

请使用管理员权限运行程序！！！以免发生"未解之谜"
___

# 文件介绍
- <font color=yellow>Mili_Wallpaper\Log\GetBilibili.json</font> 此文件将存储您输入的b站主页链接及其cookie值
  ```json
  {
      "referer": "", # b站主页链接
      "cookie": "" # cookie值
  }
  ```
  清除程序缓存后会自动清空数据并还原原貌

- <font color=yellow>Mili_Wallpaper\Log\journal.log</font> 此文件将用于存储程序产生的日志，可供查看错误

  清除程序缓存后会自动清空数据并还原原貌

- <font color=yellow>Mili_Wallpaper\Log\log.log</font> 此文件将用于存储上次用户选择的视频文件路径(仅本地视频)

  清除程序缓存后会自动清空数据并还原原貌

- <font color=yellow>Mili_Wallpaper\Log\Mili_Starting.wll</font> 此文件将存储程序开启自启动程序开关
  ```
  开启开机自启动;false # true为打开，false为关闭
  ```
  清除程序缓存后会自动清空数据并还原原貌

- <font color=yellow>Mili_Wallpaper\Log\PlayerSettings.json</font> 此文件将存储播放器的基本设置

  ```json
  {
    "delay_local": 0.01, # 播放器本地播放视频默认加载时间
    "delay_network": 3 # 播放器网络播放视频默认加载时间
  }
  ```
  如果出现播放错误的问题可以尝试将默认加载时间设置3以上, 清除程序缓存后不会自动清空数据并还原原貌

- <font color=yellow>Mili_Wallpaper\Log\SelfStartingPlayConfig.wll</font> 此文件将存储程序自启动壁纸缓存文件

  清除程序缓存后会自动清空数据并还原原貌

- <font color=yellow>Mili_Wallpaper\Log\UIDLOG.log</font> 此文件将存储程序获取到播放器窗口句柄

  清除程序缓存后会自动清空数据并还原原貌

- <font color=yellow>Mili_Wallpaper\Log\Version.wll</font> 此文件将存储程序的版本信息

  清除程序缓存后不会自动清空数据并还原原貌

- <font color=yellow>Mili_Wallpaper\Log\VideoConfig.log</font> 此文件将存储用户启动壁纸的播放设置并记录

  清除程序缓存后会自动清空数据并还原原貌

- <font color=yellow>Mili_Wallpaper\Log\Window_configuration.json</font> 此文件将控制程序的主题
  ```json
  {
    "Window transparency": 1, # 窗口透明度
    "Window theme": "light", # 窗口主题
    "Window background": "/image/bg.png" # 窗口背景图
  }
  ```
  清除程序缓存后不会自动清空数据并还原原貌

- <font color=yellow>Mili_Wallpaper\Log\BilibiliLogVideo</font> 此文件夹将存储从b站上抓取到的视频

  清除程序缓存后会自动清空数据并还原原貌

___
# 功能

- 1.播放本地视频

  程序可以选择本地视频播放视频

  根据本地视频画质绝对占用内存量, 壁纸将视频的原像素播放

---

- 2.播放网络视频

  程序可以播放网络视频，根据网络网速及目标方网速决定视频流畅度


---

- 3.静态壁纸

  程序可以选择静态图片作为静态壁纸

---

- b站视频抓取

  程序可以通过脚本抓取到指定b站视频链接中的mp4视频

  需要用户填写个人主页链接及cookie值(程序会自动保存，清除缓存后清空)

---
