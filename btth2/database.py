from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_URL = 'mysql+pymysql://root:tiennamz@localhost:3306/plan_db'

engine = create_engine(DB_URL)

LocalSession = sessionmaker(
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

def get_db():
    db = LocalSession()
    try:
        yield db

    finally:
        db.close()
        
        
