import uuid

from sqlalchemy import Column, String

from app.core.database import Base
from app.utils import GUID


class SampleModel(Base):
    __tablename__ = "sample_table"
    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
