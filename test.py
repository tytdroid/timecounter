import tkinter as tk
from tkinter import messagebox
import time
import winsound  # Windows用

# --------------------
# 設定値
# --------------------
MAX_SECONDS = 60 * 60  # 60分
BEEP_FREQ = 1000
BEEP_DURATION = 200  # ms

# --------------------
# グローバル状態
# --------------------
interval_seconds = None
start_time = None
count = 1
running = False

# --------------------
# 周期設定
# --------------------
def set_interval():
    global interval_seconds

    try:
        minutes = int(minutes_spinbox.get())
        seconds = float(seconds_spinbox.get())
    except ValueError:
        messagebox.showerror("エラー", "数値を入力してください")
        return

    if minutes < 0 or seconds < 0:
        messagebox.showerror("エラー", "負の値は設定できません")
        return

    value = minutes * 60 + seconds

    if value <= 0:
        messagebox.showerror("エラー", "0より大きい値を入力してください")
        return

    if value > MAX_SECONDS:
        messagebox.showerror("エラー", "最大60分まで設定可能です")
        return

    interval_seconds = value
    status_label.config(text=f"周期設定済み：{interval_seconds:.1f} 秒")

# --------------------
# 計測開始
# --------------------
def start_timer():
    global start_time, count, running

    if interval_seconds is None:
        messagebox.showerror("エラー", "周期を先に設定してください")
        return

    start_time = time.perf_counter()
    count = 1
    running = True

    status_label.config(text="計測中...")
    check_time()

# --------------------
# 時間監視ループ
# --------------------
def check_time():
    global count

    if not running or interval_seconds is None or start_time is None:
        return

    now = time.perf_counter()
    target = start_time + interval_seconds * count

    if now >= target:
        winsound.Beep(BEEP_FREQ, BEEP_DURATION)
        count += 1

    root.after(10, check_time)  # 10ms周期

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

tk.Button(root, text="OK（周期設定）", command=set_interval).pack(pady=5)
tk.Button(root, text="Start", command=start_timer).pack(pady=5)

status_label = tk.Label(root, text="周期未設定")
status_label.pack(pady=10)

root.mainloop()
