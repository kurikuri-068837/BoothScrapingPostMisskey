import time
import tkinter as tk
import pandas as pd
import threading
from scraping import Scraping
from misskey_post_note import PostNote


class AppGUI():
    def __init__(self,controller):
        # GUIの作成
        window = tk.Tk()
        self.window = window
        self.window.title("Processing Program")

        # ボタンとテキストボックスの配置
        button_frame = tk.Frame(self.window)
        button_frame.pack()

        self.start_button_state = False
        start_button = tk.Button(button_frame, text="Start", command=self.start_processing)
        start_button.pack(side=tk.LEFT)

        self.pause_button_state = False
        pause_button = tk.Button(button_frame, text="Pause", command=self.pause_processing, state=tk.DISABLED)
        pause_button.pack(side=tk.LEFT)

        self.resume_button_state = False
        resume_button = tk.Button(button_frame, text="Resume", command=self.resume_processing, state=tk.DISABLED)
        resume_button.pack(side=tk.LEFT)

        self.stop_button_state = False
        stop_button = tk.Button(button_frame, text="Stop", command=self.stop_processing, state=tk.DISABLED)
        stop_button.pack(side=tk.LEFT)

        #exit_button = tk.Button(button_frame, text="正常終了", command=self.normaltarmination_processing, state=tk.DISABLED)
        #exit_button.pack(side=tk.LEFT)

        log = tk.Text(self.window, width=50, height=20)
        log.pack()
        self.log = log
        
        self.start_button = start_button
        self.pause_button = pause_button
        self.resume_button = resume_button
        self.stop_button = stop_button
        #self.exit_button = exit_button

        # 初期化とデータの読み込み
        self.is_processing = False
        self.ProcessStopFrag = False
        self.update_status = True
        self.id_list_before = []
        # self.load_data()
        
        
        self.controller = controller
        self.window.mainloop()
        
    def start_processing(self):
        if not self.start_button_state and not self.is_processing and not self.ProcessStopFrag:
            self.is_processing = True
            self.ProcessStopFrag = False
            self.start_button_state  = True
            self.pause_button_state  = True
            self.resume_button_state = False
            self.stop_button_state   = False
            
            self.log_entry("status:start")
            
            
            # ボタンの状態を更新
            self.start_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            #self.exit_button.config(state=tk.DISABLED)
            
            self.controller.start_processing()
            
    def stop_processing(self):
        if self.is_processing:
            self.is_processing = False
            self.start_button_state = False
            self.pause_button_state = False
            self.resume_button_state = False
            self.stop_button_state = True
            self.log_entry("status:stop")
            # ボタンの状態を更新
            
            self.pause_button.config(state=tk.DISABLED)
            self.resume_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            
            # リスタートのボタンの状態を更新
            self.start_button.config(state=tk.NORMAL)
            # 正常終了ボタンの状態を更新
            #self.exit_button.config(state=tk.NORMAL)
            
            self.controller.stop_processing()
            
    def pause_processing(self):
        if self.is_processing and self.pause_button_state and not self.resume_button_state:
            self.pause_button_state = False
            self.resume_button_state = True
            # ボタンの状態を更新
            self.pause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)
            
            self.log_entry("status:pause")
            self.stop_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.NORMAL)
            
            self.controller.pause_processing()
            
    def resume_processing(self):
        if self.is_processing and not self.pause_button_state and self.resume_button_state:
            self.pause_button_state = True
            self.resume_button_state = False
            self.log_entry("status:resume")
            # ボタンの状態を更新
            self.pause_button.config(state=tk.NORMAL)
            self.resume_button.config(state=tk.DISABLED)
            
            self.controller.resume_processing()
            
            
            
    def log_entry(self,entry):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        log_text = f"{current_time}: {entry}\n"
        self.log.insert(tk.END, log_text)
        self.log.see(tk.END)
        self.window.update()
        
        
# ここまで再構築完了


"""
def normaltarmination_processing():
    global is_processing, start_button_state, pause_button_state, resume_button_state, stop_button_state, update_status, ProcessStopFrag
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
        log_entry("prease wait for little time(1~60sec)")
        
        
        
        # 正常終了ボタンの状態を更新
        exit_button.config(state=tk.DISABLED)
        update_status = False
        log_entry("ok")
        time.sleep(1)
        # プログラムを終了
        window.destroy()





def save_data():
    id_list_before = sp.get_processed_item_list()
    id_list_before_df = pd.DataFrame(id_list_before)
    id_list_before_df.to_csv("id_list_before.csv",index=False)
        
        

def load_data():
    global id_list_before
    try:
        id_list_before = pd.read_csv("id_list_before.csv")["data"].to_list()
        
    except FileNotFoundError:
        id_list_before = []
    
    except KeyError:
        id_list_before = []
        
def scraping_log():
    for i in range(4):
        time.sleep(5)
        log_entry(sp.watch_now_processing_url())

def scraping_and_post():
    global sp, pn
    scheduled_posts_dict = sp.process()
    #pn.post(scheduled_posts_dict)

        

def update_gui():
    while update_status:
        
        time.sleep(0.1)

"""
