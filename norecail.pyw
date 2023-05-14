from ctypes import windll, c_long, c_ulong, Structure, Union, c_int, POINTER, sizeof, CDLL
from os import path
import win32api
import time
import threading
import keyboard
import tkinter as tk
from win32gui import SetWindowLong, GetWindowLong, SetLayeredWindowAttributes
from win32con import WS_EX_LAYERED, WS_EX_TRANSPARENT, GWL_EXSTYLE



dlldir = path.join('./bypass.dll')
speed = 3
onoff = "OFF"



LONG = c_long
DWORD = c_ulong
ULONG_PTR = POINTER(DWORD)
gm = CDLL(dlldir)
gmok = gm.mouse_open()


class MOUSEINPUT(Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))


class _INPUTunion(Union):
    _fields_ = (('mi', MOUSEINPUT), ('mi', MOUSEINPUT))


class INPUT(Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))


def SendInput(*inputs):
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = c_int(sizeof(INPUT))
    return windll.user32.SendInput(nInputs, pInputs, cbSize)


def Input(structure):
    return INPUT(0, _INPUTunion(mi=structure))


def MouseInput(flags, x, y, data):
    return MOUSEINPUT(x, y, data, flags, 0, None)


def Mouse(flags, x=0, y=0, data=0):
    return Input(MouseInput(flags, x, y, data))


def mouse_xy(x, y): 
    if gmok:
        return gm.moveR(x, y)
    return SendInput(Mouse(0x0001, x, y))


def mouse_down(key = 1):  
    if gmok:
        return gm.press(key)
    if key == 1:
        return SendInput(Mouse(0x0002))
    elif key == 2:
        return SendInput(Mouse(0x0008))


def mouse_up(key = 1): 
    if gmok:
        return gm.release()
    if key == 1:
        return SendInput(Mouse(0x0004))
    elif key == 2:
        return SendInput(Mouse(0x0010))


def mouse_close(): 
    if gmok:
        return gm.mouse_close()
    

def mouse_move(rel_x,rel_y):
    mouse_xy(round(rel_x), round(rel_y))


def set_clickthrough(hwnd):
    try:
        styles = GetWindowLong(hwnd, GWL_EXSTYLE)
        styles = WS_EX_LAYERED | WS_EX_TRANSPARENT
        SetWindowLong(hwnd, GWL_EXSTYLE, styles)
        SetLayeredWindowAttributes(hwnd, 0, 255, 0x00000001)
    except Exception as e:
        print(e)


def onoff_event(event):
    global onoff
    if event.name == 'caps lock':
        if onoff == "OFF":
            onoff = "ON"

        elif onoff == "ON":
            onoff = "OFF"



def updown_event(event):
    global speed
    if event.name == '+':
        if speed < 11:
            speed = speed + 1
    elif event.name == "-":
        if speed > 1:
            speed = speed - 1




def main():



    while 1:
        if win32api.GetKeyState(0x01) < 0 and onoff == "ON":
            mouse_move(0, speed)
            time.sleep(0.014)
        if win32api.GetKeyState(0x2D) < 0:
            root.destroy()
            exit()



def update_label_text():
    global onoff
    label.config(text=f"PUBG NO Recoil Macro\nNo recoil : {onoff}\nSpeed : {speed}")
    root.after(1, update_label_text)  


keyboard.on_release(onoff_event)
keyboard.on_release(updown_event)

root = tk.Tk()
root.geometry('1920x1080')
root.overrideredirect(True)
root.config(bg='#000000')
root.attributes("-alpha", 1)
root.wm_attributes("-topmost", 1)
root.attributes('-transparentcolor', '#000000', '-topmost', 1)
root.resizable(False, False)
set_clickthrough(root.winfo_id())

label = tk.Label(root, text="PUBG NO Recoil Macro\nNo recoil : ON\nSpeed : 3", bg="black", fg="#FFFFFF", font=("Arial", 15), bd=0, justify='left')
label.place(x=0, y=0)
update_label_text()

threading.Thread(target=main, daemon=True).start()
root.mainloop()
