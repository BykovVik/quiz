from sqlalchemy import Column, String, DateTime, Integer, MetaData
from db import Base

class Question(Base):
    __tablename__ = 'Question'
    MetaData
    id = Column(Integer, primary_key=True)
    question_text = Column(String)
    answer_text = Column(String)
    created = Column(DateTime)