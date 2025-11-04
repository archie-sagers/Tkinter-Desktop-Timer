import datetime
import time
import threading
import tkinter as tk
from tkinter import messagebox

def show_fullscreen_alert():
    """Display a fullscreen popup alarm window."""
    alert = tk.Toplevel(root)
    alert.attributes("-fullscreen", True)
    alert.configure(bg="black")

    alert.lift()
    alert.focus_force()
    alert.attributes("-topmost", True)

    label = tk.Label(
        alert,
        text="Timer Finished",
        fg="white",
        bg="black",
        font=("Arial", 80, "bold")
    )
    label.pack(expand=True)

    dismiss_btn = tk.Button(
        alert,
        text="Dismiss Alarm",
        command=alert.destroy,
        bg="red",
        fg="white",
        font=("Arial", 24, "bold"),
        padx=30, pady=15
    )
    dismiss_btn.pack(pady=50)

def update_countdown(target_time):
    """Continuously update countdown label until alarm triggers."""
    while True:
        now = datetime.datetime.now()
        remaining = target_time - now
        if remaining.total_seconds() <= 0:
            countdown_var.set("00:00")
            break
        hrs, rem = divmod(int(remaining.total_seconds()), 3600)
        mins, secs = divmod(rem, 60)
        if hrs > 0:
            countdown_var.set(f"{hrs:02d}:{mins:02d}:{secs:02d}")
        else:
            countdown_var.set(f"{mins:02d}:{secs:02d}")
        time.sleep(1)

def alarm_at_specific_time(alarm_time):
    """Wait until a specific HH:MM:SS time."""
    target = datetime.datetime.combine(datetime.date.today(), datetime.time.fromisoformat(alarm_time))
    if target < datetime.datetime.now():
        target += datetime.timedelta(days=1)  # next day if time already passed

    threading.Thread(target=update_countdown, args=(target,), daemon=True).start()

    while True:
        if datetime.datetime.now() >= target:
            show_fullscreen_alert()
            break
        time.sleep(0.5)

def alarm_in_minutes(minutes_from_now):
    """Wait for a given number of (possibly fractional) minutes."""
    target_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes_from_now)
    threading.Thread(target=update_countdown, args=(target_time,), daemon=True).start()

    while True:
        if datetime.datetime.now() >= target_time:
            show_fullscreen_alert()
            break
        time.sleep(0.5)

# GUI

def toggle_inputs():
    """Show/hide inputs based on selected mode."""
    if mode_var.get() == "time":
        time_frame.pack(pady=(10, 0))
        minutes_frame.forget()
    else:
        minutes_frame.pack(pady=(10, 0))
        time_frame.forget()

def set_alarm(event=None):
    """Handle user input and start alarm in a thread (supports Enter key)."""
    mode = mode_var.get()
    countdown_var.set("")  # clear countdown display

    if mode == "time":
        alarm_time = time_entry.get().strip()
        if not alarm_time:
            messagebox.showwarning("Warning", "Please enter a time in HH:MM:SS format.")
            return
        messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")
        threading.Thread(target=alarm_at_specific_time, args=(alarm_time,), daemon=True).start()
    else:
        try:
            minutes = float(minutes_entry.get().strip())
            if minutes <= 0:
                raise ValueError
            messagebox.showinfo("Alarm Set", f"Alarm set for {minutes} minute(s) from now.")
            threading.Thread(target=alarm_in_minutes, args=(minutes,), daemon=True).start()
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid positive number of minutes.")

# Build interface

root = tk.Tk()
root.title("Alarm Clock")
root.geometry("380x330")
root.resizable(True, True)

tk.Label(root, text="Select Alarm Type:", font=("Arial", 12)).pack(pady=10)

mode_var = tk.StringVar(value="time")
tk.Radiobutton(root, text="Specific Time (HH:MM:SS)", variable=mode_var, value="time", command=toggle_inputs).pack()
tk.Radiobutton(root, text="Minutes from now", variable=mode_var, value="minutes", command=toggle_inputs).pack()

# Frames for time/minutes inputs
time_frame = tk.Frame(root)
tk.Label(time_frame, text="Enter time (HH:MM:SS):").pack()
time_entry = tk.Entry(time_frame, justify='center')
time_entry.pack()

minutes_frame = tk.Frame(root)
tk.Label(minutes_frame, text="Enter minutes (decimal allowed, e.g. 0.5 = 30 sec):").pack()
minutes_entry = tk.Entry(minutes_frame, justify='center')
minutes_entry.pack()

# Start with "time" visible
time_frame.pack(pady=(10, 0))

# Set button
set_button = tk.Button(
    root, text="Set Alarm", command=set_alarm,
    bg="white", fg="black",
    font=("Arial", 11, "bold"),
    relief="raised", padx=10, pady=5
)
set_button.pack(pady=15)

# Countdown display
countdown_var = tk.StringVar()
countdown_label = tk.Label(root, textvariable=countdown_var, font=("Courier", 20, "bold"), fg="blue")
countdown_label.pack(pady=5)

# Bind Enter key
root.bind('<Return>', set_alarm)

root.mainloop()