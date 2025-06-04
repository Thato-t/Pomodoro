import tkinter as tk
from tkinter import simpledialog
import winsound
import requests

root = tk.Tk()
root.withdraw()

session = 0
phone_ip = '192.168.0.187'
is_work = True
start_minutes = simpledialog.askinteger('Pomodoro Timer', 'Enter number of minutes for timer:', minvalue=1, maxvalue=120)
break_minutes = simpledialog.askinteger('Pomodoro Timer', 'Enter number of minutes for break:', minvalue=1, maxvalue=120)
long_break_minutes = simpledialog.askinteger('Pomodoro Timer', 'Enter number of minutes for long break:', minvalue=1, maxvalue=120)

if not start_minutes and break_minutes and long_break_minutes:
    exit()

root = tk.Tk()
root.title('Pomodoro')
root.attributes('-topmost', True)

window_width = 120
window_height = 60
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = screen_width - window_width - 10
y= screen_height - window_height - 710
root.geometry(f'{window_width}x{window_height}+{x}+{y}')
root.configure(bg='#222')

label = tk.Label(root, text=f'{start_minutes:02d}:00',
                       font=('Arial', 15), fg='white',
                       bg='#222')
label.pack(expand=True, fill='both')

def trigger_focus_mode(mode="start"):
    url = f'http://{phone_ip}:8080/focus?mode={mode}'
    try:
        requests.get(url)
    except Exception as e:
        print('Error sending focus command:', e)

def start_timer(min):
    total_seconds = min * 60
    countdown(total_seconds)

def break_timer(min):
    total_seconds = min * 60
    countdown(total_seconds)

def long_break_timer(min):
    total_seconds = min * 60
    countdown(total_seconds)

def focus_break(mins, secs):
    if is_work:
        time = 'Focus Time!' 
        label.config(text=f'{time}\n{mins:02d}:{secs:02d}',
                     fg='white',
                     bg='#222')
    else:
       
        time = 'Break Time!' 
        label.config(text=f'{time}\n{mins:02d}:{secs:02d}',
                     fg='white',
                     bg='red')


def countdown(seconds_left):
    mins = seconds_left // 60
    secs = seconds_left % 60
    label.config(focus_break(mins, secs))
    if seconds_left > 0:
        root.after(1000, countdown, seconds_left - 1)
    else:  
        switch_mode()

def switch_mode():
    global session
    global is_work
    is_work = not is_work
    
    if session == 3:
        winsound.Beep(500, 1400)
        start_timer(long_break_minutes)
        session = 0
        return
    if is_work and session != 3:
        winsound.Beep(440, 1000)
        start_timer(start_minutes)
        trigger_focus_mode('start')
        session += 1
    else:
        winsound.Beep(440, 500)
        break_timer(break_minutes)
        trigger_focus_mode('break')
start_timer(start_minutes)

root.mainloop()

