from sqlalchemy import Column

from feng_tools.orm.sqlalchemy.base_models import Model


class FileResource(Model, table=True):
    __tablename__ = 'file_resource'
    file_id = Column(comment='文件id', unique=True, nullable=False)
    save_path = Column(comment='保存路径')
    file_url = Column(comment='访问url', unique=True, nullable=False)