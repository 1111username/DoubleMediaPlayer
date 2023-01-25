from tkinter import NORMAL, DISABLED

from globalvar.globalvars import GlobalVars


def set_button_status(
        load: bool, verify: bool, play: bool,
        close: bool, sync: bool, jump: bool,
        save: bool, setting: bool):
    def convert(status: bool):
        if status:
            return NORMAL
        else:
            return DISABLED

    GlobalVars.mainWindow.bt_load['state'] = convert(load)
    GlobalVars.mainWindow.bt_verify['state'] = convert(verify)
    GlobalVars.mainWindow.bt_play['state'] = convert(play)
    GlobalVars.mainWindow.bt_close['state'] = convert(close)
    GlobalVars.mainWindow.bt_sync['state'] = convert(sync)
    GlobalVars.mainWindow.bt_jump['state'] = convert(jump)
    GlobalVars.mainWindow.bt_save['state'] = convert(save)
    GlobalVars.mainWindow.bt_setting['state'] = convert(setting)


def config_status():
    set_button_status(
        load=False, verify=False, play=False,
        close=False, sync=False, jump=False,
        save=False, setting=True
    )


def load_status():
    set_button_status(
        load=True, verify=False, play=False,
        close=False, sync=False, jump=False,
        save=False, setting=True
    )


def check_status():
    set_button_status(
        load=False, verify=True, play=False,
        close=False, sync=False, jump=False,
        save=False, setting=False
    )


def play_status():
    set_button_status(
        load=False, verify=False, play=True,
        close=True, sync=True, jump=True,
        save=True, setting=False
    )
