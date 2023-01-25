import tkinter.filedialog

import filetype

from chat.action import Notice
from globalvar.globalvars import GlobalVars
from window.status import check_status


class Load:
    def __init__(self):
        self.log = GlobalVars.mainWindow.log
        self.path = tkinter.filedialog.askopenfilename()
        self.check_is_video()

    def check_is_video(self):
        videoKinds = ('mp4', 'm4v', 'mkv', 'webm', 'mov', 'avi', 'wmv', 'mpg', 'flv', 'rmvb')
        if self.path == "":
            self.log("ERROR", "未打开文件")
        else:
            kind = filetype.guess(self.path)
            if kind.extension in videoKinds:
                self.log("INFO", "成功装载视频目录")
                if GlobalVars.player:
                    GlobalVars.player.close()
                GlobalVars.videoPath = self.path
                Notice.ok_selected_file()
                Notice.check_file_md5()
                GlobalVars.loadState = "YES"
                if GlobalVars.opLoadState == "YES":
                    check_status()
            else:
                self.log("ERROR", "选择的不是视频文件")
