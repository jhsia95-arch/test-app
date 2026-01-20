# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql://appuser:password123@postgres:5432/appdb"
#
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql://dbadmin:V9%21rQ2%23Lx814124@postgres:5432/postgres"
# DATABASE_URL = "postgresql://dbadmin:gqOXTN9QUggtKBTh@tech-assessment-db.ct4kusau6ztk.ap-southeast-1.rds.amazonaws.com:5432/postgresdb"
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./test.db"  # default for local/testing
)
# engine = create_engine(DATABASE_URL)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
