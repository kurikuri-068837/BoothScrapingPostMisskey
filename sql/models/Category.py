from sqlalchemy import Column, Integer, String, DateTime,Boolean
from sql.setting.setting import Engine,Base

class Category(Base):
    __tablename__="category"
    __table_args__={
        "comment":""
    }
    
    category_no=Column("category_no",Integer,nullable=False)
    category_name=Column("category_name",String(13),nullable=False)

Base.metadata.create_all(bind=Engine)