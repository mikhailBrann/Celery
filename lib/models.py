from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship

from lib.settings import Base


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(120), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    reg_time = Column(DateTime, server_default=func.now())
    is_authorized = Column(Boolean, unique=False, default=False)
    adv = relationship('AdvertisementModel')


class AdvertisementModel(Base):
    __tablename__ = 'advertisement'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    create_time = Column(DateTime, server_default=func.now())
    owner = Column(Integer, ForeignKey('users.id'))