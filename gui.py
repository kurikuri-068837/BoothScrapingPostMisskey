import time
import tkinter as tk
import pickle
import threading
from scraping import Scraping
from misskey_post_note import PostNote

def start_processing():
    global is_processing, start_button_state, pause_button_state, resume_button_state, stop_button_state
    if not start_button_state and not is_processing:
        is_processing = True
        start_button_state  = True
        pause_button_state  = True
        resume_button_state = False
        stop_button_state   = False
        
        log_entry("status:start")
        # 処理スレッドの開始
        processing_thread = threading.Thread(target=running_process)
        processing_thread.start()
        # ボタンの状態を更新
        start_button.config(state=tk.DISABLED)
        pause_button.config(state=tk.NORMAL)
        resume_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        exit_button.config(state=tk.DISABLED)


def pause_processing():
    global pause_button_state, resume_button_state
    if is_processing and pause_button_state and not resume_button_state:
        pause_button_state = False
        resume_button_state = True
        log_entry("status:pause")
        # ボタンの状態を更新
        pause_button.config(state=tk.DISABLED)
        resume_button.config(state=tk.NORMAL)

def resume_processing():
    global pause_button_state, resume_button_state
    if is_processing and not pause_button_state and resume_button_state:
        pause_button_state = True
        resume_button_state = False
        log_entry("status:resume")
        # ボタンの状態を更新
        pause_button.config(state=tk.NORMAL)
        resume_button.config(state=tk.DISABLED)

def stop_processing():
    global is_processing, start_button_state, pause_button_state, resume_button_state, stop_button_state
    if is_processing:
        is_processing = False
        start_button_state = False
        pause_button_state = False
        resume_button_state = False
        stop_button_state = True
        log_entry("status:stop")
        # ボタンの状態を更新
        start_button.config(state=tk.NORMAL)
        pause_button.config(state=tk.DISABLED)
        resume_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.DISABLED)
        # 正常終了ボタンの状態を更新
        exit_button.config(state=tk.NORMAL)
        save_data()

def normaltarmination_processing():
    global is_processing, start_button_state, pause_button_state, resume_button_state, stop_button_state, update_status
    if not is_processing:
        is_processing = False
        start_button_state = False
        pause_button_state = False
        resume_button_state = False
        stop_button_state = True
        log_entry("request termination process")
        # ボタンの状態を更新
        start_button.config(state=tk.DISABLED)
        pause_button.config(state=tk.DISABLED)
        resume_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.DISABLED)
        # 正常終了ボタンの状態を更新
        exit_button.config(state=tk.DISABLED)
        update_status = False
        log_entry("ok")
        time.sleep(1)
        # プログラムを終了
        window.destroy()

def log_entry(entry):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    log_text = f"{current_time}: {entry}\n"
    log.insert(tk.END, log_text)
    log.see(tk.END)

def save_data():
    id_list_before = sp.get_processed_item_list()
    with open("id_list_before.txt", "w") as f:
        pickle.dump(id_list_before, f)

def load_data():
    global id_list_before
    try:
        with open("id_list_before.txt", "rb") as f:
            id_list_before = pickle.load(f)
    except FileNotFoundError:
        id_list_before = []

def scraping_and_post():
    global sp, pn
    scheduled_posts_dict = sp.process()
    #pn.post(scheduled_posts_dict)

def running_process():
    global sp, pn
    while is_processing:
        
        # ここに処理を記述する #
        
        sap = threading.Thread(target=scraping_and_post)
        sap.start()
        time.sleep(60)
        sap.join()
        
        ###################### 
        

def update_gui():
    global update_status
    while update_status:
        window.update()
        time.sleep(0.1)

# GUIの作成
window = tk.Tk()
window.title("Processing Program")

# ボタンとテキストボックスの配置
button_frame = tk.Frame(window)
button_frame.pack()

start_button_state = False
start_button = tk.Button(button_frame, text="Start", command=start_processing)
start_button.pack(side=tk.LEFT)

pause_button_state = False
pause_button = tk.Button(button_frame, text="Pause", command=pause_processing, state=tk.DISABLED)
pause_button.pack(side=tk.LEFT)

resume_button_state = False
resume_button = tk.Button(button_frame, text="Resume", command=resume_processing, state=tk.DISABLED)
resume_button.pack(side=tk.LEFT)

stop_button_state = False
stop_button = tk.Button(button_frame, text="Stop", command=stop_processing, state=tk.DISABLED)
stop_button.pack(side=tk.LEFT)

exit_button = tk.Button(button_frame, text="正常終了", command=normaltarmination_processing, state=tk.DISABLED)
exit_button.pack(side=tk.LEFT)

log = tk.Text(window, width=50, height=20)
log.pack()

# 初期化とデータの読み込み
is_processing = False
id_list_before = []
load_data()
sp = Scraping(id_list_before)
pn = PostNote()

# メインスレッドの開始
gui_thread = threading.Thread(target=update_gui)

gui_thread.start()

# メインループ
window.mainloop()

# スレッドの終了待ち
gui_thread.join()
