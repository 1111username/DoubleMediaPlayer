import threading
from socket import *

from globalvar.globalvars import GlobalVars
from window.status import config_status, load_status


class Communicator:
    def __init__(self, recPort: int, log):
        self.recPort = recPort
        self.log = log
        self.mouse = None
        self.earThread = None
        GlobalVars.ear = self.create_server(self.recPort)

    def hear(self, handle):
        self.earThread = threading.Thread(target=self.accept, args=(handle, self.log))
        self.earThread.daemon = True
        self.earThread.start()
        self.log("INFO", "接收器开始监听连接")

    def die(self):
        GlobalVars.explore = False
        GlobalVars.dating = False
        GlobalVars.ear.close()

    def conn(self, oppositeAdd: str, oppositePort: int):
        self.mouse = socket(AF_INET, SOCK_STREAM)
        try:
            self.mouse.settimeout(3.0)
            self.mouse.connect((oppositeAdd, oppositePort))
            self.log("INFO", "连接成功")
            GlobalVars.mouseState = "CONNECTED"
            if GlobalVars.earState == "LISTEN":
                load_status()
        except:
            self.log("ERROR", "连接失败")

    def say(self, message: bytes):
        try:
            self.mouse.send(message)
        except:
            self.log("ERROR", "发送失败")

    def leave(self):
        self.mouse.close()
        GlobalVars.mouseState = "DISCONNECTED"
        config_status()

    @staticmethod
    def create_server(recPort: int) -> socket:
        server = socket(AF_INET, SOCK_STREAM)
        server.bind(('0.0.0.0', recPort))
        server.listen(1)
        return server

    @staticmethod
    def accept(handle, log):
        GlobalVars.explore = True
        GlobalVars.dating = True
        while GlobalVars.explore:
            connect, address = GlobalVars.ear.accept()
            log("INFO", f"远端{address}已同你连接")
            GlobalVars.earState = "LISTEN"
            if GlobalVars.mouseState == "CONNECTED":
                print(1)
                load_status()
            while GlobalVars.dating:
                data = connect.recv(1024)
                if len(data) == 0:
                    log("INFO", f"远端{address}已同你断开连接")
                    GlobalVars.earState = "EXPLORE"
                    config_status()
                    break
                handle(data)
