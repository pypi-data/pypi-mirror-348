from typing import Any, Generator

from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session

from feng_tools.orm.sqlalchemy.sqlalchemy_settings import DbSessionSettings


class SqlalchemySessionTool:
    """Session类"""

    def __init__(self, engine: Engine, session_settings:DbSessionSettings=None):
        self.engine = engine
        if session_settings is None:
            session_settings=DbSessionSettings()
        self.session_settings=session_settings
        self._create_session_maker()

    def _create_session_maker(self):
        """Session创建者"""
        self.session_maker = sessionmaker(bind=self.engine,
                                          autocommit=self.session_settings.auto_commit,
                                          autoflush=self.session_settings.auto_flush,
                                          expire_on_commit=self.session_settings.expire_on_commit)

    def create_session(self) -> Session:
        """获取Session"""
        return self.session_maker()

    def get_session_context(self) -> Generator[Session, Any, None]:
        """获取Session上下文"""
        with self.session_maker() as session:
            yield session



