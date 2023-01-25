import tools.tools as tool
from globalvar.globalvars import GlobalVars
from player.control import Player
from window.status import load_status, check_status, play_status


class Notice:
    @staticmethod
    def ok_selected_file():
        dataDict = {
            "type": "selected",
        }
        GlobalVars.communicator.say(
            message=tool.dict_to_json_bytes(dataDict)
        )
        GlobalVars.mainWindow.log("INFO", "已告知对方选择好了视频")

    @staticmethod
    def check_file_md5():
        dataDict = {
            "type": "check",
            "filemd5": tool.get_file_md5(GlobalVars.videoPath)
        }
        GlobalVars.communicator.say(
            message=tool.dict_to_json_bytes(dataDict)
        )
        GlobalVars.mainWindow.log("INFO", "已告知对方视频的摘要")

    @staticmethod
    def ok_check():
        dataDict = {
            "type": "ok_check"
        }
        GlobalVars.communicator.say(
            message=tool.dict_to_json_bytes(dataDict)
        )
        GlobalVars.mainWindow.log("INFO", "已告知对方验证成功")

    @staticmethod
    def no_check():
        dataDict = {
            "type": "no_check"
        }
        GlobalVars.communicator.say(
            message=tool.dict_to_json_bytes(dataDict)
        )
        GlobalVars.mainWindow.log("INFO", "已告知对方验证失败")

    @staticmethod
    def start_play():
        dataDict = {
            "type": "play"
        }
        GlobalVars.communicator.say(
            message=tool.dict_to_json_bytes(dataDict)
        )
        GlobalVars.mainWindow.log("INFO", "已经告知对方开始播放")
        pass

    @staticmethod
    def turn_video_state():
        dataDict = {
            "type": "pause"
        }
        GlobalVars.communicator.say(
            message=tool.dict_to_json_bytes(dataDict)
        )
        GlobalVars.mainWindow.log("INFO", "已告知对方切换视频状态")
        pass

    @staticmethod
    def close_video():
        dataDict = {
            "type": "close"
        }
        GlobalVars.communicator.say(
            message=tool.dict_to_json_bytes(dataDict)
        )
        GlobalVars.mainWindow.log("INFO", "已告知对方关闭视频")
        pass

    @staticmethod
    def sync_video(videoTime: int):
        dataDict = {
            "type": "sync",
            "time": videoTime
        }
        GlobalVars.communicator.say(
            message=tool.dict_to_json_bytes(dataDict)
        )
        GlobalVars.mainWindow.log("INFO", "已告知对方同步视频")
        pass

    @staticmethod
    def jump_video(videoTime: int):
        dataDict = {
            "type": "jump",
            "time": videoTime
        }
        GlobalVars.communicator.say(
            message=tool.dict_to_json_bytes(dataDict)
        )
        GlobalVars.mainWindow.log("INFO", "已告知对方跳转视频")
        pass


class Receive:
    @staticmethod
    def analyze(message: bytes):
        dataDict = tool.json_bytes_to_dict(message)
        noticeType = dataDict['type']

        match noticeType:
            case 'selected':
                GlobalVars.mainWindow.log("INFO", "对方已经选择好了视频，等待校验")
                GlobalVars.opLoadState = "YES"
                if GlobalVars.loadState == "YES":
                    check_status()
            case 'check':
                GlobalVars.mainWindow.log("INFO", "对方已经发送来了视频的摘要")
                GlobalVars.opFileMD5 = dataDict['filemd5']
            case 'ok_check':
                GlobalVars.mainWindow.log("INFO", "经对方验证成功，视频相同")
                GlobalVars.opCheckState = "YES"
                if GlobalVars.checkState == "YES":
                    play_status()
                    GlobalVars.player = Player()
                    GlobalVars.player.set_uri(GlobalVars.videoPath)
            case 'no_check':
                GlobalVars.mainWindow.log("ERROR", "经对方验证失败，请重新加载")
                GlobalVars.opLoadState = "NO"
                GlobalVars.loadState = "NO"
                GlobalVars.checkState = "NO"
                GlobalVars.opCheckState = "NO"
                load_status()
            case 'play':
                GlobalVars.mainWindow.log("INFO", "对方发送来视频开始播放的消息")
                GlobalVars.mainWindow.active_play()
            case 'pause':
                GlobalVars.mainWindow.log("INFO", "对方发送来切换视频状态的消息")
                GlobalVars.mainWindow.active_play()
            case 'close':
                GlobalVars.mainWindow.log("INFO", "对方发送来关闭视频的消息")
                GlobalVars.mainWindow.active_close()
                load_status()
            case 'sync':
                GlobalVars.mainWindow.log("INFO", "对方发送来同步视频的消息")
                GlobalVars.mainWindow.log("INFO", f"对方视频在{dataDict['time']}ms，跳转")
                GlobalVars.player.set_time(dataDict['time'])
            case 'jump':
                GlobalVars.mainWindow.log("INFO", f"对方发来跳转视频的消息，跳转到{dataDict['time']}ms")
                GlobalVars.player.set_time(dataDict['time'])
            case _:
                GlobalVars.mainWindow.log("ERROR", "收到消息，但解析失败")
