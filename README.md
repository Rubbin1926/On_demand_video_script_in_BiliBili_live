#Bilibili直播间点播视频脚本 / On_demand_video_script_in_BiliBili_live
能够读取指定B站直播间的弹幕，并且做出反应，实现视频点播 / Be able to read the barrage in the designated live broadcasting room of station B and respond to it to realize video on demand

## **实现效果 / Effect achieved**
 1. 当观众发送普通弹幕，print发送人id和弹幕内容 / When the audience sends ordinary danmaku, print sender ID and danmaku content
 2. 当观众发送“播放 avxxxxx”或“播放 BVxxxxx”时（注意av和BV的大小写和“点播后的空格”），存储到order_list.json中 / When the audience sends "播放 avxxxxx" or "播放 BVxxxxx" (note the capitalization of av and BV and the space after "播放"), it is stored in order_list.json
 3. 当没有点播视频时，自动播放default_list.json中的视频内容（目前是我本人挑选的一些视频） / Automatically play content from default_list.json when there is no on-demand video (currently some of the videos I have selected)
 4. 当观众发送“切”或者播放的视频结束时，切换下一个视频（下一个视频取决于order_list.json中是否还有需要播放的视频）/ When the audience sends a "切" or the video ends playing, switch to the next video (the next video depends on whether there is still a video to play in order_list.json)
 5. 当在播放默认视频时，如果一位观众点播了视频，马上切换到点播视频（可以关闭此功能） / When playing the default video, if an audience orders a video, immediately switch to the on-demand video (This function can be turned off)

## **需要的python包 / Required Python site-packages**

 - bilibili_api
 - asyncio
 - webbrowser
 - time
 - pyautogui
 - win32gui
 - win32con
 - json
 - random
 - os

  
## **最重要的基础设置 / The most important basic setting**
打开main.bat文件，找到如下字符（有两段相同字符） / Open the main.bat file and find the following characters (there are two identical characters)

    D:\anaconda\python.exe

**将其修改为你的python程序的路径 / Change it to the path of your Python program**

## **修改直播间和默认列表 / Modify the live room id and default list**
### 修改直播间 / Modify the live room id
打开receive_danmaku.py文件，在第7行找到如下代码 / Open receive_danmaku.py file, find the following code on the seventh line

    room = live.LiveDanmaku(22725544)

将"22725544"修改成需要使用自动脚本的直播间 / Modify '22725544' to a live streaming room that requires the use of automatic scripts


----------


###修改默认列表 / Modify default list
打开default_list.json文件，按照原文件里的格式对视频列表进行修改 / Open default_list.json file, modify the video list according to the format in the original file
例如修改为 / For example, modify to

    ["BV1mV411L7F2","BV1254y187SE"]
    
## **关闭&打开“是否在播放播放默认视频时，马上切换播放新出现的点播视频”的功能 / Turn off & Turn on the function of 'whether to immediately switch to playing new on-demand videos when playing the default video'**
打开play_video.py文件，找到如下代码 / Open play_video.py file, find the following code

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

如果要关闭此功能（即只有“切”才切换视频），将"if temp1:"取消注释，注释"if temp1 or (temp2 ^ is_list):"。效果如下 / If you want to turn off this feature (i.e. only switch videos with '切'), uncomment 'if temp1:' and annotate 'if temp1 or (temp2 ^ is_list):'. The effect is as follows

    if temp1:
    # if temp1 or (temp2 ^ is_list):
    
如果要打开此功能，就将上述操作反向操作一次即可（即和Github上代码保持一致） / If you want to turn on this feature, simply reverse the above operation once (i.e. keep it consistent with the code on Github)

## **作者无聊的bb / The author's boring remarks**
随缘更新，有一些问题我还是不满意，比如关闭视频是模拟键盘"Alt+F4"来实现。一直开关浏览器会影响性能。
这个程序是自己在看一位up主的直播间时，突发奇想做来练手的。
欢迎在b站关注作者（作者目前是个大一的小菜逼），会随缘分享一点自己的生活，可能会直播一些无聊的游戏。
[###作者的b站主页链接###][1]


  祝您生活愉快！
  
I may update randomly XD. There are some issues that I am still not satisfied with, such as closing the video by simulating the keyboard with "Alt+F4". Keeping the browser on and off can affect performance.
This program was developed by myself when I was watching a live broadcast room of an bilibili up and had a sudden idea to practice my skills.
Welcome to follow the author on Bilibili (the author is currently a freshman), who will share some of my own life and may live some boring games.
[###Author's homepage link on Bilibili###][2]


  [1]: https://space.bilibili.com/259101880
  [2]: https://space.bilibili.com/259101880
  
Wishing you a happy day!
