from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class FormSubmission(Base):
    __tablename__ = 'responses'

    id = Column(Integer, primary_key=True)
    form_name = Column(Text)
    responses = Column(Text)
