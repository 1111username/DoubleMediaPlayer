from tkinter import Label, Entry, Button, NORMAL, DISABLED, END

from globalvar.globalvars import GlobalVars


class Setting:
    def __init__(self):
        self.mainWindow = GlobalVars.mainWindow
        self.root = self.mainWindow.create_sub_window(
            width=280,
            height=200,
            title='设置'
        )
        self.ipEntry = None
        self.portEntry = None
        self.tipLable = None
        self.connButtion = None
        self.disconnButtion = None
        self._set_elements()
        self.check_status()
        self.root.mainloop()

    def _set_elements(self):
        Label(
            master=self.root,
            text='对端IP:'
        ).place(x=30, y=30, width=60, height=30)
        Label(
            master=self.root,
            text='对端端口:'
        ).place(x=30, y=70, width=60, height=30)
        self.ipEntry = Entry(
            master=self.root
        )
        self.portEntry = Entry(
            master=self.root
        )
        self.ipEntry.place(x=90, y=30, width=160, height=30)
        self.portEntry.place(x=90, y=70, width=160, height=30)
        self.tipLable = Label(
            master=self.root,
            text="当前状态:未连接"
        )
        self.tipLable.place(x=65, y=110, width=150, height=30)
        self.connButtion = Button(
            master=self.root,
            text="连接"
        )
        self.disconnButtion = Button(
            master=self.root,
            text="断开"
        )
        self.connButtion.place(x=30, y=150, width=90, height=30)
        self.disconnButtion.place(x=160, y=150, width=90, height=30)
        self.connButtion.configure(command=self.connect)
        self.disconnButtion.configure(command=self.disconnect)

    def tip(self, message: str):
        self.tipLable.configure(
            text=f"当前状态:{message}"
        )

    @staticmethod
    def check_ip(ip: str) -> bool:
        ip_list = ip.split('.')
        flag = True
        if 4 != len(ip_list):
            flag = False
            return flag
        for num in ip_list:
            if num.isdigit() and 0 <= int(num) <= 255:
                continue
            else:
                flag = False
                break
        return flag

    @staticmethod
    def check_port(port: str) -> bool:
        try:
            portnum = int(port)
            return 0 <= portnum <= 65535
        except:
            return False

    def check_status(self):
        if GlobalVars.mouseState == "DISCONNECTED":
            self.tip("未连接")
            self.disconnButtion['state'] = DISABLED
            self.ipEntry['state'] = NORMAL
            self.portEntry['state'] = NORMAL
            self.connButtion['state'] = NORMAL
        elif GlobalVars.mouseState == "CONNECTED":
            self.tip("已连接")
            self.ipEntry['state'] = NORMAL
            self.portEntry['state'] = NORMAL
            self.ipEntry.delete(0, END)
            self.portEntry.delete(0, END)
            self.ipEntry.insert(0, GlobalVars.ip)
            self.portEntry.insert(0, GlobalVars.port)
            self.connButtion['state'] = DISABLED
            self.ipEntry['state'] = DISABLED
            self.portEntry['state'] = DISABLED
            self.disconnButtion['state'] = NORMAL

    def connect(self):
        ip = self.ipEntry.get()
        port = self.portEntry.get()
        if self.check_ip(ip) and self.check_port(port):
            GlobalVars.communicator.conn(
                oppositeAdd=ip,
                oppositePort=int(port)
            )
            GlobalVars.ip = ip
            GlobalVars.port = int(port)
        else:
            self.tip("格式有误")
            return
        self.check_status()

    def disconnect(self):
        GlobalVars.communicator.leave()
        self.check_status()
