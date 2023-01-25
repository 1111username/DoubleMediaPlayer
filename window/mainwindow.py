import os.path
import tkinter as tk
from tkinter import *

from chat.action import Receive, Notice
from chat.communicate import Communicator
from globalvar.globalvars import GlobalVars
from player.control import Player
from tools.tools import get_file_md5, have_file, create_json_file, write_json_file, read_json_file
from window.status import config_status, load_status, play_status
from window.subwindow.jump import Jump
from window.subwindow.load import Load
from window.subwindow.setting import Setting


class BaseWindow:

    def __init__(self):
        self.root = tk.Tk()
        self.screenWidth = self.root.winfo_screenwidth()
        self.screenHeight = self.root.winfo_screenheight()
        self.console = tk.Text(master=self.root)
        self.bt_load = tk.Button(master=self.root, text='加载')
        self.bt_verify = tk.Button(master=self.root, text='验证')
        self.bt_play = tk.Button(master=self.root, text='播放/暂停')
        self.bt_close = tk.Button(master=self.root, text='关闭视频')
        self.bt_sync = tk.Button(master=self.root, text='同步')
        self.bt_jump = tk.Button(master=self.root, text='跳转')
        self.bt_save = tk.Button(master=self.root, text='保存')
        self.bt_setting = tk.Button(master=self.root, text='设置')

        GlobalVars.mainWindow = self
        GlobalVars.communicator = Communicator(
            recPort=GlobalVars.myPort,
            log=self.log
        )
        GlobalVars.communicator.hear(handle=Receive.analyze)

        self._set_main_window()
        self._set_element_in_main_window()
        self._set_console()
        self._set_load()
        self._set_verify()
        self._set_play()
        self._set_close()
        self._set_sync()
        self._set_jump()
        self._set_save()
        self._set_setting()
        config_status()

    def quit_window(self):
        try:
            GlobalVars.communicator.leave()
        except:
            pass
        try:
            GlobalVars.communicator.die()
        except:
            pass
        self.root.destroy()

    def _set_main_window(self):
        self.root.title("双人播放器")
        self.root.resizable(False, False)
        left = (self.screenWidth - 280) // 2
        top = (self.screenHeight - 440) // 2
        self.root.geometry(f"280x440+{left}+{top}")
        self.root.protocol('WN_DELETE_WINDOW', self.quit_window)

    def _set_element_in_main_window(self):
        self.console.place(x=20, y=20, width=240, height=70)
        self.bt_load.place(x=20, y=100, width=110, height=60)
        self.bt_verify.place(x=150, y=100, width=110, height=60)
        self.bt_play.place(x=20, y=170, width=110, height=60)
        self.bt_close.place(x=150, y=170, width=110, height=60)
        self.bt_sync.place(x=20, y=240, width=110, height=60)
        self.bt_jump.place(x=150, y=240, width=110, height=60)
        self.bt_save.place(x=20, y=310, width=110, height=60)
        self.bt_setting.place(x=150, y=310, width=110, height=60)

    def _set_console(self):
        self.console.config(state=DISABLED)
        pass

    def _set_load(self):
        self.bt_load.configure(command=Load)

    def _set_verify(self):

        def verfiy():
            if get_file_md5(GlobalVars.videoPath) == GlobalVars.opFileMD5:
                GlobalVars.checkState = "YES"
                self.log("INFO", "验证成功")
                Notice.ok_check()
                if GlobalVars.opCheckState == "YES":
                    play_status()
                    GlobalVars.player = Player()
                    GlobalVars.player.set_uri(GlobalVars.videoPath)
            else:
                self.log("ERROR", "验证失败")
                GlobalVars.checkState = "NO"
                GlobalVars.opLoadState = "NO"
                GlobalVars.loadState = "NO"
                GlobalVars.opLoadState = "NO"
                load_status()

        self.bt_verify.configure(command=verfiy)

    def active_play(self):

        match GlobalVars.player.get_status():
            case 1:
                GlobalVars.player.pause()
            case 0:
                GlobalVars.player.pause()
            case -1:
                GlobalVars.player.play()
            case _:
                pass

    def _set_play(self):

        def trun():
            match GlobalVars.player.get_status():
                case 1:
                    GlobalVars.player.pause()
                    Notice.turn_video_state()
                case 0:
                    GlobalVars.player.pause()
                    Notice.turn_video_state()
                case -1:
                    GlobalVars.player.play()
                    Notice.start_play()
                case _:
                    pass
        self.bt_play.configure(
            command=trun
        )

    def active_close(self):
        GlobalVars.player.close()
        self._set_play()

    def _set_close(self):

        def close():
            GlobalVars.player.close()
            Notice.close_video()
            self._set_play()
            GlobalVars.loadState = "NO"
            GlobalVars.opLoadState = "NO"
            GlobalVars.checkState = "NO"
            GlobalVars.opCheckState = "NO"
            load_status()

        self.bt_close.configure(
            command=close
        )

    def _set_sync(self):

        def sync():
            Notice.sync_video(
                videoTime=GlobalVars.player.get_time()
            )
            self.log("INFO", "已经向对方发布当前时间，以同步")

        self.bt_sync.configure(command=sync)

    def _set_save(self):

        def save():
            filePath = os.path.join(
                GlobalVars.rootPath,
                'history.json'
            )
            if not have_file(filePath):
                create_json_file(GlobalVars.rootPath, 'history.json')
                write_json_file(filePath, {"history": []})
            dataDict = read_json_file(filePath)
            dataDict['history'].append({
                "filePath": GlobalVars.videoPath,
                "process": GlobalVars.player.get_time()
            })
            write_json_file(filePath, dataDict)
            self.log("INFO", "已经保存当前进度")
            pass

        self.bt_save.configure(command=save)

    def _set_jump(self):
        self.bt_jump.configure(command=Jump)

    def _set_setting(self):
        self.bt_setting.configure(command=Setting)

    def log(self, tag: str, message: str):
        self.console.config(state=NORMAL)
        self.console.insert(END, f"{tag}-{message}\n")
        self.console.config(state=DISABLED)
        self.console.see(END)

    def start(self):
        self.root.mainloop()

    def create_sub_window(self, width, height, title) -> Toplevel:
        subWindow = tk.Toplevel(master=self.root)
        subWindow.title(title)
        left = (self.screenWidth - width) // 2
        top = (self.screenHeight - height) // 2
        subWindow.geometry(f"{width}x{height}+{left}+{top}")
        subWindow.resizable(False, False)
        return subWindow
