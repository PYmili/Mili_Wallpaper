import requests
import re
import json
import os
from time import sleep
import fileid

"""发送请求"""
def get_requese(url, referer, cookie):
    headers = {
        "referer":referer, # 自己B站主页的防盗链
        "cookie":cookie, # 自己cookie
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.44"
    }
    return requests.get(url=url, headers=headers)

"""回去数据链接"""
def get_playinfo(url, req):
    title = re.search('''<title data-vue-meta="true">(.*?)</title>''', req.text, re.S).group(1)
    search = re.findall("<script>window.__playinfo__=(.*?)</script>", req.text)[0]
    data = json.loads(search)
    audio = data['data']['dash']['audio'][0]['baseUrl']
    video = data['data']['dash']['video'][0]['baseUrl']
    return [audio, video, title]

"""保存文件"""
def save(audio, video, title, loging, referer, cookie):
    title = fileid.fileid.Newid(5).newfileid()
    loging.record("正常运行", f"生成随机文件名{title}")
    with open(fr".\test.mp3", "wb") as faudio:
        faudio.write(get_requese(audio, referer, cookie).content)
        loging.record("正常运行", f"保存text.mp3文件")
    with open(fr".\test.mp4", "wb") as fvideo:
        fvideo.write(get_requese(video, referer, cookie).content)
        loging.record("正常运行", f"保存text.mp4文件")
    PATH = os.path.split(__file__)[0]
    os.popen(
        fr"cd {PATH}/and_ffmpeg/bin && ffmpeg -i {PATH}/test.mp4 -i {PATH}/test.mp3 -c:v copy -c:a copy -bsf:a aac_adtstoasc {PATH}/Log/BilibiliLogVideo/{title}.mp4"
    )
    loging.record("正常运行", f"合成目标文件...")

    while True:
        if os.path.exists(f"{PATH}\Log\BilibiliLogVideo\{title}.mp4"):
            sleep(3)
            os.remove(f"./test.mp4")
            loging.record("正常运行", f"删除text.mp4文件")
            os.remove(f"./test.mp3")
            loging.record("正常运行", f"删除text.mp3文件")
            break
        else:
            continue
        sleep(1)
    return f"{PATH}\Log\BilibiliLogVideo\{title}.mp4"

def main(BilibiliUrl, referer, cookie, loging):
    urllist = get_playinfo(BilibiliUrl, get_requese(BilibiliUrl, referer, cookie))
    return save(urllist[0], urllist[1], urllist[-1], loging, referer, cookie)

# main(
#     "https://www.bilibili.com/video/BV1PB4y127F2?spm_id_from=333.851.b_7265636f6d6d656e64.4&vd_source=38ed22feb13e188519d677588b4ab6e5",
#     "https://space.bilibili.com/483109517?spm_id_from=333.1007.0.0",
#     "buvid3=D2256BF8-443F-889F-FAD8-F675DDA1621920615infoc; i-wanna-go-back=-1; _uuid=5E10759F3-7387-B267-ED10A-A875B949D9B823175infoc; rpdid=|(u))|YlmJmk0J'uYRk)RJYJJ; buvid_fp_plain=undefined; CURRENT_BLACKGAP=0; blackside_state=0; buvid4=B8C8B889-4EB6-FF44-FD98-6D174F4C5B5199175-022012415-boF00P1fYfgMZnjWURx6hg%3D%3D; DedeUserID=483109517; DedeUserID__ckMd5=16e796c2407276bb; b_ut=5; LIVE_BUVID=AUTO4816463852172581; fingerprint3=2f927b785a462738d887b272a256c63a; nostalgia_conf=-1; go_old_video=1; is-2022-channel=1; hit-dyn-v2=1; CURRENT_QUALITY=112; fingerprint=2c514c19705e4de16f63d732224cdec0; buvid_fp=2c514c19705e4de16f63d732224cdec0; SESSDATA=d2c5f6b6%2C1672150659%2C2cafa%2A61; bili_jct=68d2ec4bc48c248b8fefdcb1226751dc; sid=bkf0sd7v; bp_video_offset_483109517=677540462619263000; CURRENT_FNVAL=80; PVID=2; innersign=0; b_lsid=744441036_181BE17CDE8; b_timer=%7B%22ffp%22%3A%7B%22333.1007.fp.risk_D2256BF8%22%3A%22181BE17D29B%22%2C%22333.999.fp.risk_D2256BF8%22%3A%22181BE17DFA6%22%7D%7D",
#     Log
# )