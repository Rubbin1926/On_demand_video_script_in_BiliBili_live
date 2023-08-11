from bilibili_api import live, sync
import json
"""BV1X8411m7HQ"""
"""播放 BV1WV4y167Uz"""
"""BV15z4y147hQ"""

room = live.LiveDanmaku(22725544)
"""咸鱼直播间:9447550"""


@room.on('DANMU_MSG')
async def on_danmaku(event):

    # 收到弹幕
    danmu = event
    # print(danmu)

    # 弹幕发送人
    danmu_person = danmu["data"]["info"][2][1]

    # 弹幕信息
    danmu_info = danmu["data"]["info"][1]

    # 打印弹幕
    print(f"""{danmu_person}:{danmu_info}""")

    # 如果弹幕为“切”则将switch_video.json内容改为[1]
    if danmu_info == "切":
        is_switch = [1]
        with open('switch_video.json', 'w') as f:
            json.dump(is_switch, f)

    if danmu_info.startswith("播放 "):
        danmu_info_ = danmu_info[3:]
        # 打印av或BV号
        # print(danmu_info_)

        if danmu_info_.startswith("av") or danmu_info_.startswith("BV"):
            # 导入视频列表
            with open('order_list.json', 'r') as f:
                video_list = json.load(f)

            video_list.append(danmu_info_)
            print(f"""播放列表：{video_list}""")
            with open('order_list.json', 'w') as f:
                json.dump(video_list, f)

        else:
            print("视频格式错误，请检查")


sync(room.connect())
