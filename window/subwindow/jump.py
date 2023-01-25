from tkinter import Label, Button, Entry

from chat.action import Notice
from globalvar.globalvars import GlobalVars


class Jump:
    def __init__(self):
        self.mainWindow = GlobalVars.mainWindow
        self.root = self.mainWindow.create_sub_window(
            width=200,
            height=120,
            title='跳转到'
        )
        self.frameEntry = None
        self.jumpButtion = None
        self._set_elements()
        self._set_bt_jump()

    def _set_elements(self):
        Label(
            master=self.root,
            text="ms"
        ).place(x=15, y=22, width=50, height=30)
        self.frameEntry = Entry(
            master=self.root
        )
        self.frameEntry.place(x=65, y=20, width=120, height=35)
        self.jumpButtion = Button(
            master=self.root,
            text="跳转"
        )
        self.jumpButtion.place(x=40, y=70, width=120, height=30)

    def _set_bt_jump(self):

        def jump():
            ttime = self.frameEntry.get()
            if ttime == "" or int(ttime) > GlobalVars.player.get_length():
                pass
            else:
                GlobalVars.player.set_time(int(ttime))
                Notice.jump_video(int(ttime))

        self.jumpButtion.configure(command=jump)
