import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)
# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "sqlite:///./test.db"  # default for local/testing
# )
# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"check_same_thread": False}
#     if DATABASE_URL.startswith("sqlite")
#     else {}
# )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
