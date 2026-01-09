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
        value = float(interval_entry.get())
    except ValueError:
        messagebox.showerror("エラー", "数値を入力してください")
        return

    if value <= 0:
        messagebox.showerror("エラー", "正の値を入力してください")
        return

    if unit.get() == "min":
        value *= 60

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
root.geometry("300x230")

tk.Label(root, text="周期入力").pack(pady=5)

interval_entry = tk.Entry(root, justify="center")
interval_entry.pack()

unit = tk.StringVar(value="sec")
tk.Radiobutton(root, text="秒", variable=unit, value="sec").pack()
tk.Radiobutton(root, text="分", variable=unit, value="min").pack()

tk.Button(root, text="OK（周期設定）", command=set_interval).pack(pady=5)
tk.Button(root, text="Start", command=start_timer).pack(pady=5)

status_label = tk.Label(root, text="周期未設定")
status_label.pack(pady=10)

root.mainloop()
