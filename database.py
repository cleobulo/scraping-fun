from sqlmodel import SQLModel, Field, create_engine, Session, select
from datetime import datetime

# ============================= Database Setup
sql_file_name = 'database.db'
sqlite_url = f'sqlite:///{sql_file_name}'
connect_args = {'check_same_thread': False}
engine = create_engine(sqlite_url, connect_args=connect_args)
# ============================= Database Setup - End
# ============================= Models
class Page(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str = Field(index=True, unique=True)
    title: str = Field(default=None)
    content: str = Field(default=None)
    scraped_at: datetime = Field(default=None)
# ============================= Models - End
# ============================= Functions
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def insert_page(session: Session, url: str, title: str, content: str, scraped_at: datetime = None):
    page = Page(url=url, title=title, content=content, scraped_at=scraped_at)
    session.add(page)
    session.commit()
    session.refresh(page)
    return page
# ============================= Functions - End
