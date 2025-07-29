import sqlalchemy as sa
from sqlalchemy import Update, inspect, Result
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .base_do import BaseDo, get_db
from .._logger import logger
from typing import List

class BaseDAO:
    def __init__(self):
        # 创建异步引擎
        async_engine = get_db(pool_size=2, max_overflow=1)
        # 使用更明确的名称表示这是一个会话工厂
        self.session_factory = sessionmaker(
            bind=async_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def insert(self, instance: List[BaseDo] | BaseDo):
        """
        插入新数据
        :param instance:
        :return:
        """
        # 通过会话工厂创建一个新的会话对象
        async with self.session_factory() as session:
            async with session.begin():
                try:
                    if isinstance(instance, list):
                        session.add_all(instance)
                    else:
                        session.add(instance)
                    await session.commit()
                    return True
                except Exception as e:
                    logger.error(f"Insert operation failed: {e}")
                    await session.rollback()
                    return False

    async def update(self, instance: BaseDo, fields_to_update: List[str] = None):
        # 通过会话工厂创建一个新的会话对象
        async with self.session_factory() as session:
            async with session.begin():
                try:
                    if fields_to_update:
                        update_values = {
                            field: getattr(instance, field) for field in fields_to_update if hasattr(instance, field)
                        }
                        primary_key = inspect(instance.__class__).primary_key[0].name
                        stmt = (
                            Update(instance.__class__)
                            .where(getattr(instance.__class__, primary_key) == getattr(instance, primary_key))
                            .values(**update_values)
                        )
                        await session.execute(stmt)
                        return True
                    else:
                        update_values = {
                            col.name: getattr(instance, col.name)
                            for col in instance.__table__.columns
                            if not col.primary_key
                        }
                        primary_key = inspect(instance.__class__).primary_key[0].name
                        stmt = (
                            Update(instance.__class__)
                            .where(getattr(instance.__class__, primary_key) == getattr(instance, primary_key))
                            .values(**update_values)
                        )
                        await session.execute(stmt)
                        return True
                except Exception as e:
                    logger.error(f"Update operation failed: {e}")
                    await session.rollback()
                    return False

    async def update_by_dict(self, instance: BaseDo, update_data: dict = None):
        # 通过会话工厂创建一个新的会话对象
        async with self.session_factory() as session:
            async with session.begin():
                try:
                    if update_data:
                        # 构建更新语句的 values 部分
                        update_values = update_data.copy()
                        primary_key = sa.inspect(instance.__class__).primary_key[0].name
                        # 确保主键不在更新字段中（一般主键不用于更新操作，除非特殊情况）
                        if primary_key in update_values:
                            del update_values[primary_key]

                        stmt = (
                            sa.Update(instance.__class__)
                            .where(getattr(instance.__class__, primary_key) == getattr(instance, primary_key))
                            .values(**update_values)
                        )
                        await session.execute(stmt)
                        return True
                    else:
                        update_values = {
                            col.name: getattr(instance, col.name)
                            for col in instance.__table__.columns
                            if not col.primary_key
                        }
                        primary_key = sa.inspect(instance.__class__).primary_key[0].name
                        stmt = (
                            sa.Update(instance.__class__)
                            .where(getattr(instance.__class__, primary_key) == getattr(instance, primary_key))
                            .values(**update_values)
                        )
                        await session.execute(stmt)
                        return True
                except Exception as e:
                    logger.error(f"Update by dict operation failed: {e}")
                    await session.rollback()
                    raise

    async def scalar(self, query):
        # 通过会话工厂创建一个新的会话对象
        async with self.session_factory() as session:
            try:
                result = await session.scalar(query)
                return result
            except Exception as e:
                logger.error(f"Scalar operation failed: {e}")
                raise

    async def execute(self, query) -> Result | None:
        """
        执行操作
        :param query:
        :return:
        """
        # 通过会话工厂创建一个新的会话对象
        async with self.session_factory() as session:
            async with session.begin():
                try:
                    result = await session.execute(query)
                    return result
                except Exception as e:
                    logger.error(f"Execute operation failed: {e}")
                    await session.rollback()
                    return None