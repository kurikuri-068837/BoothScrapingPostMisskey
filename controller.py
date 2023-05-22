from scraping import Scraping
from misskey_post_note import PostNote
import threading
#from gui import AppGUI
import time
import pandas as pd

class AppController():
    
    def __init__(self) -> None:
        #self.mainloop = threading.Thread(target=lambda : AppGUI(self),)
        #self.mainloop.start()
        self.load_data()
        self.ProcessingFrag = False
        self.StopProcessFrag = False
        self.cycle_time = 60
        self.sp = Scraping(self.processed_id_list)
        self.scraping_thread = threading.Thread(target=self.sp.process)
        self.pn = PostNote()
        self.postnote_thread = threading.Thread(target=self.pn.post)
        
        
    def start_processing(self):
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
            
    def save_data(self):
        processed_id_list = self.sp.get_processed_id_list()
        processed_id_list_df = pd.DataFrame(processed_id_list)
        processed_id_list_df.to_csv("processed_id_list.csv",index=False)
        
    def scraping_process(self):
        while self.ProcessingFrag:
            self.scraping_thread.start()
            
            (f"PF:{self.ProcessingFrag},SPF:{self.StopProcessFrag}")
            time.sleep(self.cycle_time)
            
            scheduled_posts = self.scraping_thread.join()
            print(f"scheduled_posts:{scheduled_posts}")
            
        self.StopProcessFrag = True
        
        
        
        
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


