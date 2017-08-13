from sqlalchemy import Column, Text, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class FormSubmission(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, server_default=func.current_timestamp())
    # Even though the SZ ID is a "number" it's not ordinal or cardinal. It is safe to
    # treat it as text.
    sz_id = Column(Text)
    form_name = Column(Text)
    responses = Column(Text)
