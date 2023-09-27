from scraping import Scraping
from misskey_post_note import PostNote
import threading
import time
import pandas as pd

class AppController():
    
    def __init__(self) -> None:
        self.ProcessingFrag = False
        self.load_data()
        
        
    def start_processing(self):
        self.ProcessingFrag = True
        other_process_thread = threading.Thread(target=self.scraping_process)
        other_process_thread.start()
        
        
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
        self.sp = Scraping(self.processed_id_list)
        pn = PostNote()
        while self.ProcessingFrag:
            
            print("start scraping process")
            scheduled_posts = self.sp.process()
            
            if scheduled_posts != {}:
                print("start post process")
                postnote_thread = threading.Thread(target=pn.post,args=(scheduled_posts,))
                postnote_thread.start()
            
            
            if not self.ProcessingFrag:
                if scheduled_posts != {}:
                    postnote_thread.join()
                    print("Change ProcessingFrag")
            
            if scheduled_posts != {}:
                postnote_thread.join()
            print("end posted process")
        
