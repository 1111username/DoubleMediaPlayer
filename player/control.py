import os.path
import tkinter

import vlc

from globalvar.globalvars import GlobalVars


class Player:
    def __init__(self, ):
        self.log = GlobalVars.mainWindow.log
        self.mediaPlayer = vlc.MediaPlayer()
        self.add_callback(vlc.EventType.MediaPlayerEndReached, self.check_end)
        self.palyer_window = None
        self.videoCanvas = None

    def play_window_create(self):
        self.palyer_window = GlobalVars.mainWindow.create_sub_window(
            width=500,
            height=500,
            title=os.path.basename(GlobalVars.videoPath)
        )
        self.palyer_window.configure(bg='black')
        self.palyer_window.resizable(True, True)
        self.videoCanvas = tkinter.Canvas(
            master=self.palyer_window,
            bg='black'
        )
        self.videoCanvas.place(x=0, y=0, relwidth=1.0, relheight=1.0)

    def set_uri(self, uri: str):
        self.mediaPlayer.set_mrl(uri)
        self.play_window_create()
        self.mediaPlayer.set_hwnd(self.videoCanvas.winfo_id())
        pass

    def play(self):
        self.log("INFO", "播放")
        self.mediaPlayer.play()

    def pause(self):
        match self.get_status():
            case 1:
                self.log("INFO", "暂停")
            case 0:
                self.log("INFO", "播放")
        self.mediaPlayer.pause()

    def close(self):
        self.mediaPlayer.stop()
        self.mediaPlayer.release()
        self.palyer_window.destroy()
        GlobalVars.player = None
        del self

    def set_time(self, ttime: int):
        self.mediaPlayer.set_time(ttime)

    def get_time(self) -> int:
        return self.mediaPlayer.get_time()

    def get_length(self):
        return self.mediaPlayer.get_length()

    def get_status(self) -> int:
        state = self.mediaPlayer.get_state()
        match state:
            case vlc.State.Playing:
                return 1
            case vlc.State.Paused:
                return 0
            case _:
                return -1

    def add_callback(self, event_type, callback):
        self.mediaPlayer.event_manager().event_attach(event_type, callback)

    def check_end(self, event):
        self.log("INFO", "播放完毕")
        self.close()
