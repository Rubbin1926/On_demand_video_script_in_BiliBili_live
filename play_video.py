from bilibili_api import live, sync, video
import asyncio
import webbrowser
import time
import pyautogui
import win32gui
import win32con
import json
import random
import os
"""BV1X8411m7HQ"""
"""BV1WV4y167Uz"""
"""BV15z4y147hQ"""

room = live.LiveDanmaku(22725544)
# 咸鱼直播间:9447550

# def open_and_close_browser(url, t):
#     # 在当前页面打开新窗口
#     webbrowser.open(url)
#     hwnd = win32gui.FindWindow(None, "Microsoft Edge")
#     win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
#
#     # 等待视频播放完成
#     time.sleep(t)
#
#     # 关闭当前页面（通过模拟按下alt+F4快捷键）
#     pyautogui.hotkey('alt', 'f4')


def if_switch_video():
    """返回 True 或 False，判断是否切换视频"""
    with open('switch_video.json', 'r') as f:
        is_switch = json.load(f)

    if is_switch == [1]:
        return True
    else:
        return False


def any_video_in_list():
    """返回 True 或 False，判断是否出现点播视频"""
    with open('order_list.json', 'r') as f:
        temp_video_list = json.load(f)
    return bool(temp_video_list)


def open_and_close_browser(url, t, is_list):
    # 在当前页面打开新窗口
    webbrowser.open(url)
    hwnd = win32gui.FindWindow(None, "Microsoft Edge")
    win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

    # 等待视频播放完成或检测到外部变量为True
    start_time = time.time()
    while time.time() - start_time < t:
        temp1, temp2 = if_switch_video(), any_video_in_list()

        # 第一个if:只有“切”才切换视频
        # 第二个if:输入”切“或者在播放默认列表时出现点播视频都直接“切”

        # if temp1:
        if temp1 or (temp2 ^ is_list):
            print("有新任务力")

            # 把“切”改为否
            is_switch = [0]
            with open('switch_video.json', 'w') as f:
                json.dump(is_switch, f)

            # 判断是否为点播列表中，是则删除第一个视频
            if is_list:
                with open('order_list.json', 'r') as f:
                    video_list = json.load(f)
                del video_list[0]
                print(f"""播放列表：{video_list}""")
                with open('order_list.json', 'w') as f:
                    json.dump(video_list, f)
            pyautogui.hotkey('alt', 'f4')
            return
        time.sleep(0.5)

    # 判断是否为点播列表中，是则删除第一个视频
    if is_list:
        with open('order_list.json', 'r') as f:
            video_list = json.load(f)
        del video_list[0]
        print(f"""播放列表：{video_list}""")
        with open('order_list.json', 'w') as f:
            json.dump(video_list, f)
    pyautogui.hotkey('alt', 'f4')


async def main():
    while True:
        print("___________")
        await asyncio.sleep(1.5)
        with open('order_list.json', 'r') as f:
            video_list = json.load(f)
        if not video_list:
            # 自动播放功能
            print("列表为空QAQ 播放默认视频")

            # 读取默认播放列表
            with open('default_list.json', 'r') as f:
                default_list = json.load(f)

                # 随机选取默认列表视频
                default_list_length = len(default_list)
                seed = int.from_bytes(os.urandom(4), byteorder='little')
                random.seed(seed)
                random_number = random.randint(0, default_list_length-1)

                v = video.Video(bvid=default_list[random_number])
                v_info = await v.get_info()
                v_time = v_info["duration"]
                print(f"""视频时长：{v_time}s""")

                # 打开网页播放视频
                url = f"""https://www.bilibili.com/video/{default_list[random_number]}"""
                open_and_close_browser(url, v_time+6, False)

        else:
            # 获取列表第一个视频
            v1 = video_list[0]
            if v1.startswith("av"):

                # 获取视频信息（时长）
                v_ = v1[2:]
                v = video.Video(aid=int(v_))
                v_info = await v.get_info()
                v_time = v_info["duration"]
                print(f"""视频时长：{v_time}s""")

                # 打开网页播放视频
                url = f"""https://www.bilibili.com/video/{v1}"""
                open_and_close_browser(url, v_time+6, True)

                # 播放完毕删除视频
                # del video_list[0]
                # with open('order_list.json', 'w') as f:
                #     json.dump(video_list, f)

            if v1.startswith("BV"):

                # 获取视频信息（时长）
                v = video.Video(bvid=v1)
                v_info = await v.get_info()
                v_time = v_info["duration"]
                print(f"""视频时长：{v_time}s""")

                # 打开网页播放视频
                url = f"""https://www.bilibili.com/video/{v1}"""
                open_and_close_browser(url, v_time+6, True)

                # 播放完毕删除视频
                # del video_list[0]
                # with open('order_list.json', 'w') as f:
                #     json.dump(video_list, f)

asyncio.run(main())


# @room.on('DANMU_MSG')
# async def on_danmaku(event):
#
#     # 收到弹幕
#     danmu = event
#     #print(danmu)
#
#     #弹幕发送人
#     danmu_person = danmu["data"]["info"][2][1]
#
#     #弹幕信息
#     danmu_info = danmu["data"]["info"][1]
#
#     #打印弹幕
#     print(f"""{danmu_person}:{danmu_info}""")
#
#     if danmu_info.startswith("播放 "):
#         danmu_info_ = danmu_info[3:]
#         print(danmu_info_)
#
#         if danmu_info_.startswith("av"):
#
#             # 获取视频信息（时长）
#             v = danmu_info_[2:]
#             v = video.Video(aid=int(v))
#             v_info = await v.get_info()
#             v_time = v_info["duration"]
#             print(f"""视频时长：{v_time}""")
#
#             # 打开网页播放视频
#             url = f"""https://www.bilibili.com/video/{danmu_info_}"""
#             open_and_close_browser(url, v_time+5)
#             hwnd = win32gui.FindWindow(None, "Microsoft Edge")
#             win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
#
#         if danmu_info_.startswith("BV"):
#
#             #获取视频信息（时长）
#             v = video.Video(bvid = danmu["data"]["info"][1][3:])
#             v_info = await v.get_info()
#             v_time = v_info["duration"]
#             print(f"""视频时长：{v_time}""")
#
#             #打开网页播放视频
#             url = f"""https://www.bilibili.com/video/{danmu["data"]["info"][1][3:]}"""
#             open_and_close_browser(url, v_time+5)
#             hwnd = win32gui.FindWindow(None, "Microsoft Edge")
#             win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
#
#         else:
#             print("视频格式错误，请检查")
#
#
# sync(room.connect())
