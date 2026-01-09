import tkinter as tk
from tkinter import messagebox
import timer

# --------------------
# GUI コールバック
# --------------------
def on_set_interval():
    """周期設定ボタンが押されたときの処理"""
    try:
        minutes = int(minutes_spinbox.get())
        seconds = float(seconds_spinbox.get())
    except ValueError:
        messagebox.showerror("エラー", "数値を入力してください")
        return

    success, message = timer.set_interval(minutes, seconds)
    if success:
        status_label.config(text=message)
    else:
        messagebox.showerror("エラー", message)


def on_start_timer():
    """開始ボタンが押されたときの処理"""
    success, message = timer.start_timer_func()
    if success:
        status_label.config(text=message)
        check_time_loop()
    else:
        messagebox.showerror("エラー", message)


def check_time_loop():
    """時間監視ループ"""
    if timer.check_time():
        root.after(10, check_time_loop)  # 10ms周期
    else:
        timer.stop_timer()

# --------------------
# GUI構築
# --------------------
root = tk.Tk()
root.title("時間感覚トレーニングタイマー")
root.geometry("300x280")

tk.Label(root, text="周期入力（分:秒）").pack(pady=5)

# 分のスピンボックス
frame_minutes = tk.Frame(root)
frame_minutes.pack(pady=5)
tk.Label(frame_minutes, text="分：").pack(side=tk.LEFT)
minutes_spinbox = tk.Spinbox(frame_minutes, from_=0, to=60, width=5)
minutes_spinbox.delete(0, tk.END)
minutes_spinbox.insert(0, "0")
minutes_spinbox.pack(side=tk.LEFT)

# 秒のスピンボックス
frame_seconds = tk.Frame(root)
frame_seconds.pack(pady=5)
tk.Label(frame_seconds, text="秒：").pack(side=tk.LEFT)
seconds_spinbox = tk.Spinbox(frame_seconds, from_=0, to=59.9, width=5, format="%.1f")
seconds_spinbox.delete(0, tk.END)
seconds_spinbox.insert(0, "0")
seconds_spinbox.pack(side=tk.LEFT)

tk.Button(root, text="OK（周期設定）", command=on_set_interval).pack(pady=5)
tk.Button(root, text="Start", command=on_start_timer).pack(pady=5)

status_label = tk.Label(root, text="周期未設定")
status_label.pack(pady=10)

root.mainloop()
