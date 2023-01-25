import os


class GlobalVars:
    videoPath = ""
    ear = None
    explore = False
    dating = False
    mainWindow = None
    communicator = None
    player = None

    rootPath = os.getcwd()

    myPort = 5000

    ip = ""
    port = None

    earState = "EXPLORE"
    mouseState = "DISCONNECTED"

    loadState = "NO"
    opLoadState = "NO"

    checkState = "NO"
    opCheckState = "NO"

    opFileMD5 = ""
