from data.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


engine = create_async_engine(url=settings.DB_URI)

SESSION_MAKER = async_sessionmaker(bind=engine)
