import json
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class Base(DeclarativeBase):
    pass


class BaseDo(Base):
    __abstract__ = True

    def model_dump(self):
        """
        将当前实例转换为字典的方法
        """
        mapper = sa.inspect(self.__class__)
        columns = mapper.columns
        result_dict = {}
        for column in columns:
            column_name = column.name
            value = getattr(self, column_name)
            if not column_name.startswith('_'):
                if isinstance(column.type, sa.DateTime):
                    if value:
                        # 将datetime类型的值转换为指定格式的字符串
                        value = value.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        value = None
                result_dict[column_name] = value
        return result_dict

    def model_dump_json(self) -> str:
        """将实例转成json字符串"""
        result_dict = self.model_dump()
        return json.dumps(result_dict)


def get_db(user,password,host,port,database,pool_size: int = 10, max_overflow: int = 5, pool_recycle: int = 3600):
    engine = create_async_engine(
        f'mysql+aiomysql://{user}:{password}@{host}:{port}/{database}',
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_recycle=pool_recycle
    )
    return engine


async def init_db():
    # 创建异步引擎，和你代码中的函数类似
    engine = async_engine
    async with engine.begin() as conn:
        # 关键在这里，调用create_all创建所有表
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

def init_database(user,password,host,port,database):
    async_engine = get_db(user=user,password=password,host=host,port=port,database=database)

    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    return async_engine, Session

