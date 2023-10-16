from sqlalchemy import Column, Integer, String, DateTime,Boolean
from sql.setting.setting import Engine,Base

class MisskeyPost(Base):
    __tablename__="misskey_post"
    __table_args__={
        "comment":"item_idをキーとしてmisskeyへ投稿した情報を記録"
    }
    
    item_id=Column("item_id",Integer,primary_key=True)
    note_id=Column("note_id",Integer,primary_key=True)
    poted_id=Column("poted_id",DateTime,nullable=False)
    delete_flag=Column("delete_flag",Boolean,nullable=False)

Base.metadata.create_all(bind=Engine)