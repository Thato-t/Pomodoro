import tkinter as tk
from tkinter import simpledialog
import winsound

root = tk.Tk()
root.withdraw()

is_work = True
minutes = simpledialog.askinteger('Pomodoro Timer', 'Enter number of minutes:', minvalue=1, maxvalue=120)
if not minutes:
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

label = tk.Label(root, text=f'{minutes:02d}:00',
                       font=('Arial', 15), fg='white',
                       bg='#222')
label.pack(expand=True, fill='both')

def start_timer(min):
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
                     fg='#222',
                     bg='white')


def countdown(seconds_left):
    mins = seconds_left // 60
    secs = seconds_left % 60
    label.config(focus_break(mins, secs))
    if seconds_left > 0:
        root.after(1000, countdown, seconds_left - 1)
    else:  
        switch_mode()

def switch_mode():
    global is_work
    is_work = not is_work
    if is_work:
        winsound.Beep(440, 1000)
        start_timer(minutes)
    else:
        winsound.Beep(440, 500)
        start_timer(5)


start_timer(minutes)

root.mainloop()

