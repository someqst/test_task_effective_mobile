from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from data.config import settings


engine = create_async_engine(url=settings.DB_URI)

SESSION_MAKER = async_sessionmaker(bind=engine)
