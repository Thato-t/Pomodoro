import tkinter as tk
from tkinter import simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import font as tkfont
import winsound
import requests
import threading
import ctypes
from ctypes import windll
import pyautogui
import os
from filelock import FileLock, Timeout
import pygetwindow as gw
import sys
import keyboard


lock = FileLock('pomodoro.lock')

try:
    lock.acquire(timeout=0.1)
except Timeout:
    print('App is already running')
    sys.exit(0)
# Initialize window
root = ttk.Window(themename="superhero")
root.title('Pomodoro')
root.attributes('-topmost', True)

# Position in corner
window_width = 120
window_height = 80
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = screen_width - window_width - 5
y = screen_height - window_height - 719
root.geometry(f'{window_width}x{window_height}+{x}+{y}')

# Remove title bar and buttons
# root.overrideredirect(True)

# Ensure correct path
font_path = os.path.abspath('fonts/Poppins-Regular.ttf')

# Load font using windows API
FR_PRIVATE = 0x10
FR_NOT_ENUM = 0x20

if windll.gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0):
    print('Poppins font loaded successfully')
else:
    print('Failed to load font')
# Fonts and state
custom_fonts = tkfont.Font(family="Poppins", size=18)
paused = False
is_work = True
session = 1
remaining_seconds = 0
remaining_job = None

# Ask for time input
start_minutes = simpledialog.askinteger('Pomodoro Timer', 'Enter number of minutes for timer:', minvalue=1, maxvalue=120)
if not start_minutes:
    exit()
break_minutes = simpledialog.askinteger('Pomodoro Timer', 'Enter number of minutes for break:', minvalue=1, maxvalue=120)
long_break_minutes = simpledialog.askinteger('Pomodoro Timer', 'Enter number of minutes for long break:', minvalue=1, maxvalue=120)
session_length = simpledialog.askinteger('Pomodoro Timer', 'Enter number of sessions before long break:', minvalue=1, maxvalue=60)

# Frame and Label
frame = ttk.Frame(root)
frame.pack(expand=True, fill='both')
# Configure the grid inside the frame
frame.grid_rowconfigure(0, weight=1)  # Top empty row
frame.grid_rowconfigure(2, weight=1)  # Bottom empty row
frame.grid_columnconfigure(0, weight=1)  # Single column with weight

label = ttk.Label(frame, text=f'{start_minutes:02d}:00', font=custom_fonts, foreground='#000')
label.grid(row=1, column=0)

# Buttons
pause_btn = ttk.Button(frame, text="⏸", bootstyle="warning", command=lambda: pause_timer())
resume_btn = ttk.Button(frame, text="▶", bootstyle="success", command=lambda: resume_timer())


frame.grid_rowconfigure(4, weight=1)

def bring_to_front():
    windows = gw.getWindowsWithTitle('Pomodoro')
    print(windows)
    if windows:
        win = windows[0]
        win.restore()
        win.activate()

# Countdown logic
def update_timer_display():
    mins = remaining_seconds // 60
    secs = remaining_seconds % 60
    color = "#000" if is_work else "#E74C3C"
    label.config(text=f"{mins:02d}:{secs:02d}", foreground=color)

def countdown():
    global remaining_seconds, remaining_job, session
    if paused:
        return
    update_timer_display()
    if remaining_seconds > 0:
        remaining_seconds -= 1
        remaining_job = root.after(1000, countdown)
    else:
        switch_mode()

def start_timer(minutes):
    global remaining_seconds, paused, session
    remaining_seconds = minutes * 60
    paused = False
    show_pause()
    countdown()

def pause_timer():
    global paused
    paused = True
    if remaining_job:
        root.after_cancel(remaining_job)
    pause_btn.grid_forget()
    resume_btn.grid(row=3, column=0)

def resume_timer():
    global paused
    paused = False
    resume_btn.grid_forget()
    pause_btn.grid(row=3, column=0)
    countdown()

def show_pause():
    resume_btn.grid_forget()
    pause_btn.grid(row=3, column=0)

def switch_mode():
    global session, is_work
    is_work = not is_work
    if session == session_length:
        winsound.Beep(500, 1400)
        start_timer(long_break_minutes)
        session = 0
    elif is_work:
        winsound.Beep(440, 1000)
        start_timer(start_minutes)
        session += 1
    else:
        winsound.Beep(440, 500)
        start_timer(break_minutes)

# Start first session
start_timer(start_minutes)
root.bind('<Delete>', lambda e: root.destroy())
root.bind('<space>', lambda e: root.iconify())
keyboard.add_hotkey('Escape', bring_to_front)
# TODO make certain keyboards keys to minimize and restore

print("All systems running")
root.mainloop()
