from gui import *
from scraping import Scraping
from misskey_post_note import PostNote
import threading
from gui import *

pn = PostNote()
post_note_threading = threading.Thread(target=pn)
