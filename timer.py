import time
import winsound

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


def reset_timer():
    """タイマーをリセット"""
    global interval_seconds, start_time, count, running
    interval_seconds = None
    start_time = None
    count = 1
    running = False


def set_interval(minutes, seconds):
    """周期を設定
    
    Args:
        minutes (int): 分
        seconds (float): 秒
        
    Returns:
        tuple: (成功フラグ, メッセージ)
    """
    global interval_seconds

    if minutes < 0 or seconds < 0:
        return False, "負の値は設定できません"

    value = minutes * 60 + seconds

    if value <= 0:
        return False, "0より大きい値を入力してください"

    if value > MAX_SECONDS:
        return False, "最大60分まで設定可能です"

    interval_seconds = value
    return True, f"周期設定済み：{interval_seconds:.1f} 秒"


def start_timer_func():
    """計測を開始
    
    Returns:
        tuple: (成功フラグ, メッセージ)
    """
    global start_time, count, running

    if interval_seconds is None:
        return False, "周期を先に設定してください"

    start_time = time.perf_counter()
    count = 1
    running = True
    return True, "計測中..."


def check_time():
    """時間を監視
    
    Returns:
        bool: 処理を継続するか
    """
    global count

    if not running or interval_seconds is None or start_time is None:
        return False

    now = time.perf_counter()
    target = start_time + interval_seconds * count

    if now >= target:
        winsound.Beep(BEEP_FREQ, BEEP_DURATION)
        count += 1

    return True


def stop_timer():
    """タイマーを停止"""
    global running
    running = False
