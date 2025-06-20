import tkinter as tk
from tkinter import simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import font as tkfont
import winsound
import requests

# Initialize window
root = ttk.Window(themename="flatly")
root.title('Pomodoro')
root.attributes('-topmost', True)

# Position in corner
window_width = 120
window_height = 80
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = screen_width - window_width - 10
y = screen_height - window_height - 690
root.geometry(f'{window_width}x{window_height}+{x}+{y}')

# Fonts and state
custom_fonts = tkfont.Font(family="Poppins", size=18)
paused = False
session = 0
is_work = True
remaining_seconds = 0
remaining_job = None

# Ask for time input
start_minutes = simpledialog.askinteger('Pomodoro Timer', 'Enter number of minutes for timer:', minvalue=1, maxvalue=120)
if not start_minutes:
    exit()
break_minutes = simpledialog.askinteger('Pomodoro Timer', 'Enter number of minutes for break:', minvalue=1, maxvalue=120)
long_break_minutes = simpledialog.askinteger('Pomodoro Timer', 'Enter number of minutes for long break:', minvalue=1, maxvalue=120)

# Frame and Label
frame = ttk.Frame(root)
frame.pack()
label = ttk.Label(frame, text=f'{start_minutes:02d}:00', font=custom_fonts, foreground='#000')
label.pack()

# Buttons
pause_btn = ttk.Button(frame, text="⏸", bootstyle="warning", command=lambda: pause_timer())
resume_btn = ttk.Button(frame, text="▶", bootstyle="success", command=lambda: resume_timer())

# Countdown logic
def update_timer_display():
    mins = remaining_seconds // 60
    secs = remaining_seconds % 60
    color = "#000" if is_work else "#E74C3C"
    label.config(text=f"{mins:02d}:{secs:02d}", foreground=color)

def countdown():
    global remaining_seconds, remaining_job
    if paused:
        return
    update_timer_display()
    if remaining_seconds > 0:
        remaining_seconds -= 1
        remaining_job = root.after(1000, countdown)
    else:
        switch_mode()

def start_timer(minutes):
    global remaining_seconds, paused
    remaining_seconds = minutes * 60
    paused = False
    show_pause()
    countdown()

def pause_timer():
    global paused
    paused = True
    if remaining_job:
        root.after_cancel(remaining_job)
    pause_btn.pack_forget()
    resume_btn.pack()

def resume_timer():
    global paused
    paused = False
    resume_btn.pack_forget()
    pause_btn.pack()
    countdown()

def show_pause():
    resume_btn.pack_forget()
    pause_btn.pack()

def switch_mode():
    global session, is_work
    is_work = not is_work
    if session == 1:
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
root.mainloop()
