import tkinter as tk
from tkinter import simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import font as tkfont
import winsound
import requests


root = ttk.Window()


custom_fonts = tkfont.Font(family="Poppins", size=18)
paused = False
session = 0
phone_ip = '192.168.0.187'
is_work = True
remaining_time = None

start_minutes = simpledialog.askinteger('Pomodoro Timer', 'Enter number of minutes for timer:', minvalue=1, maxvalue=120)
break_minutes = simpledialog.askinteger('Pomodoro Timer', 'Enter number of minutes for break:', minvalue=1, maxvalue=120)
long_break_minutes = simpledialog.askinteger('Pomodoro Timer', 'Enter number of minutes for long break:', minvalue=1, maxvalue=120)



if not start_minutes and break_minutes and long_break_minutes:
    exit()

root = ttk.Window()
root.title('Pomodoro')
root.attributes('-topmost', True)


frame = ttk.Frame(root)
frame.pack()



window_width = 120
window_height = 80
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = screen_width - window_width - 10
y= screen_height - window_height - 690
root.geometry(f'{window_width}x{window_height}+{x}+{y}')

label = ttk.Label(frame, text=f'{start_minutes:02d}:00',
                        font=custom_fonts,
                        foreground='#000')
label.pack()


# def trigger_focus_mode(mode="start"):
#     url = f'http://{phone_ip}:8080/focus?mode={mode}'
#     try:
#         requests.get(url)
#     except Exception as e:
#         print('Error sending focus command:', e)


def start_timer(min):
    total_seconds = min * 60
    countdown(total_seconds)


def focus_break(mins, secs):
    if is_work:
        label.config(text=f'{mins:02d}:{secs:02d}',
                     foreground="#000")
    else:
        label.config(text=f'{mins:02d}:{secs:02d}',
                     foreground="#E74C3C")



def countdown(seconds_left):
    global paused, remaining_time
    if paused:
        return
    mins = seconds_left // 60
    secs = seconds_left % 60
    label.config(focus_break(mins, secs))
    if seconds_left > 0:
        remaining_time = root.after(1000, countdown, seconds_left - 1)
    else:  
        switch_mode()

def pause_timer():
    global paused, remaining_time
    paused = True
    if remaining_time:
        root.after_cancel(remaining_time)

    pause_btn.pack_forget()
    resume_btn.pack(padx=5)

def resume_timer():
    global paused, remaining_time
    paused = False
    resume_btn.pack_forget()
    pause_btn.pack(padx=5)
    countdown(remaining_time) 
    
    pause_btn = tk.Button(root, text="Pause", command=pause_timer)
    pause_btn.pack(padx=5)
    resume_btn = tk.Button(root, text="Resume", command=resume_timer)


def switch_mode():
    global session, is_work
    is_work = not is_work
    
    if session == 3:
        winsound.Beep(500, 1400)
        start_timer(long_break_minutes)
        session = 0
        pause_btn = tk.Button(root, text="Pause", command=pause_timer)
        pause_btn.pack_forget()
        return
    if is_work and session != 3:
        winsound.Beep(440, 1000)
        start_timer(start_minutes)
        pause_btn = tk.Button(root, text="Pause", command=pause_timer)
        pause_btn.pack(padx=5)
        resume_btn = tk.Button(root, text="Resume", command=resume_timer)
        # trigger_focus_mode('start')
        session += 1
    else:
        winsound.Beep(440, 500)
        start_timer(break_minutes)
        pause_btn = tk.Button(root, text="Pause", command=pause_timer)
        pause_btn.pack_forget()
        # trigger_focus_mode('break')
start_timer(start_minutes)

root.mainloop()

