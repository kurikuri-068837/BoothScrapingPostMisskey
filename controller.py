from scraping import Scraping
from misskey_post_note import PostNote
import pandas as pd

class AppController():
    
    def __init__(self) -> None:
        self.load_data()
        
        
    def start_processing(self):
        self.scraping_process()
        
        
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
        
        print("start scraping process")
        scheduled_posts = self.sp.process()
        if scheduled_posts != {}:
            print("start post process")
            pn.post(scheduled_posts)
            print("end posted process")
            self.sp.update_save_data()
        else:
            print("nothing postnote")
