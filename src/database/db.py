import contextlib

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection, async_sessionmaker,create_async_engine


from src.config.config import config



class DatabaseSesssionManager:
    def __init__(self, url: str) -> None:
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker = async_sessionmaker(autoflush=False, 
                                                      autocommit=False, 
                                                      bind=self._engine)
        

@contextlib.asynccontextmanager
async def session(self):
    if self._session_maker is None:
        raise Exception('Sesion is not initialized')
    session = self._session_maker()
    try:
        yield session
    except Exception as err:
        print(err)
        await session.rollback()
    finally:
        await session.close()


sessionmanager = DatabaseSesssionManager(config.DB_URL)

async def get_db():
    with sessionmanager.session() as session:
        yield session