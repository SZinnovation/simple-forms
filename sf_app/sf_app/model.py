from sqlalchemy import Column, Text, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class FormSubmission(Base):
    __tablename__ = 'responses'

    # The expectation is that we just let the DB set these (or perhaps pretend
    # in the case of sqlite3)
    id = Column(Integer, primary_key=True)
    time = Column(DateTime, server_default=func.current_timestamp())

    # These need to be set explicitly
    session = Column(Text)
    sz_id = Column(Text)
    form_name = Column(Text)
    # Even though the SZ ID is a "number" it's not ordinal or cardinal. It is safe to
    # treat it as text.
    responses = Column(Text)
