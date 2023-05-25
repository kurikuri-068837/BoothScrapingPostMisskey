from scraping import Scraping
from misskey_post_note import PostNote
import threading
#from gui import AppGUI
import time
import pandas as pd
import logging

class AppController():
    
    def __init__(self) -> None:
        #self.mainloop = threading.Thread(target=lambda : AppGUI(self),)
        #self.mainloop.start()
        self.ProcessingFrag = False
        self.StopProcessFrag = False
        self.cycle_time = 600
        
        
        
        
    def start_processing(self):
        self.load_data()
        self.ProcessingFrag = True
        self.StopProcessFrag = False
        #TODO:ここにスクレイピング等の処理
        other_process_thread = threading.Thread(target=self.scraping_process)
        other_process_thread.start()
        
        
        
        
    
    def stop_processing(self):
        self.ProcessingFrag = False
        timer_start = time.time()
        print("prease wait...")
        while self.StopProcessFrag:
            time.sleep(2)
            print(time.time()-timer_start)
        #TODO:スクレイピング、misskeyのポスト終了処理、処理済みリストの保存処理
        self.save_data()
        print("save ok")       
    
    def pause_processing(self):
        self.ProcessingFrag = False
        
        #TODO:スクレイピング、misskeyのポストの中断処理
        pass
    
    def resume_processing(self,):
        self.ProcessingFrag = True
        self.StopProcessFrag = False
        self.scraping_process()
        pass
    
    def normarmination_processing(self):
        
        
        print("Close GUI")
        
        pass
    
    def load_data(self):
        try:
            self.processed_id_list = list(pd.read_csv("processed_id_list.csv").values[:,0])
                
        except:
            self.processed_id_list = []
        logging.log
            
    def save_data(self):
        processed_id_list = self.sp.get_processed_id_list()
        processed_id_list_df = pd.DataFrame(processed_id_list)
        processed_id_list_df.to_csv("processed_id_list.csv",index=False)
        
    def scraping_process(self):
        sp = Scraping(self.processed_id_list)
        pn = PostNote()
        while self.ProcessingFrag:
            if self.check_process_time():
                print("enter")
                scheduled_posts = sp.process()
                
                if scheduled_posts != {}:
                    print("post process")
                    postnote_thread = threading.Thread(target=pn.post,args=(scheduled_posts,))
                    postnote_thread.start()
                    print("post end")
            
            (f"PF:{self.ProcessingFrag},SPF:{self.StopProcessFrag}")
            print(f"scheduled_posts:{scheduled_posts}")
            
            if self.judge_weekday_daytime(): # 日中の昼間だった場合は実行スパンを30分おきにする
                time.sleep(self.cycle_time*3)
            else:
                time.sleep(self.cycle_time)
            
        self.StopProcessFrag = True
        
    def judge_weekday_daytime(self):
        current_time = time.localtime()
        day_of_week = current_time.tm_wday  # 0: 月曜日, 1: 火曜日, ... , 6: 日曜日
        hour = current_time.tm_hour
        minute = current_time.tm_min

        if 0 <= day_of_week <= 4:
            # 月曜日から金曜日までの場合
            if (9 <= hour < 11) or (13 <= hour < 17) or (hour == 11 and minute <= 20 ):
                # 9時から12時、13時から17時までの間は日中のスパンを延長する
                return True
        return False
        
        
    def CUI_Controller(self):
        while True:
            command = input("process - start/stop: ")
            if command == "stop":
                self.stop_processing()
                break
            # 特定のコマンドに対する処理を記述する
            if command == "start":
                # 別のプロセスを実行
                self.start_processing()
            else:
                print("無効なコマンドです。")
                
        input("プログラムを終了します。(please Enter)")


    def check_process_time(self):
        current_time = time.localtime()
        hour = current_time.tm_hour
        minute = current_time.tm_min
        
        if 23 <= hour or 0 <= hour < 6 or (hour == 6 and minute <= 30 ):
            
            print("夜間のため、プロセスを実行しません(停止時間:23時~6時半まで)")
            if hour == 23:
                wait_sec = 7*3600
                time.sleep(wait_sec)
            return False
        return True

    
    
    
