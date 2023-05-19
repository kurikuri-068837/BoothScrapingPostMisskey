from scraping import Scraping
from misskey_post_note import PostNote
import threading
from gui import AppGUI
import time
import pandas as pd

class AppController():
    
    def __init__(self) -> None:
        self.mainloop = threading.Thread(target=lambda : AppGUI(self),)
        self.mainloop.start()
        self.load_data()
        self.ProcessingFrag = False
        self.StopProcessFrag = False
        self.cycle_time = 60
        self.sp = Scraping(self.processed_id_list)
        self.scraping_thread = threading.Thread(target=self.sp.get_info)
        self.pn = PostNote()
        self.postnote_thread = threading.Thread(target=self.pn.post)
        
        
    def start_processing(self,log_entry_func):
        self.ProcessingFrag = True
        self.StopProcessFrag = False
        #TODO:ここにスクレイピング等の処理
        self.scraping_process(log_entry_func)
        
        
        pass
    
    def stop_processing(self):
        self.ProcessingFrag = False
        timer_start = time.time()
        print("prease wait...")
        while self.StopProcessFrag:
            time.sleep(1)
            print(time.time()-timer_start)
        #TODO:スクレイピング、misskeyのポスト終了処理、処理済みリストの保存処理
        self.save_data()
        pass        
    
    def pause_processing(self):
        self.ProcessingFrag = False
        
        #TODO:スクレイピング、misskeyのポストの中断処理
        pass
    
    def resume_processing(self,log_entry_func):
        self.ProcessingFrag = True
        self.StopProcessFrag = False
        self.scraping_process(log_entry_func)
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
        
    def scraping_process(self,log_entry_func):
        while self.ProcessingFrag:
            self.scraping_thread.start()
            
            log_entry_func(f"PF:{self.ProcessingFrag},SPF:{self.StopProcessFrag}")
            time.sleep(self.cycle_time)
            
            scheduled_posts = self.scraping_thread.join()
            
        self.StopProcessFrag = True
    


