# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from API5 import db

Base = declarative_base()
metadata = Base.metadata

Base = db.Model
Column = db.Column
Date = db.Date
DateTime = db.DateTime
ForeignKey = db.ForeignKey
Integer = db.Integer
String = db.String
Text = db.Text
text = db.text
relationship = db.relationship

class Device(Base):
    __tablename__ = 'device'

    device_id = Column(Integer, primary_key=True)
    key = Column(String(127))
    password = Column(String(127))
    type = Column(String(127))
    config = Column(String(512))
    is_claimed = Column(Integer, server_default=text("'0'"))
    in_topic = Column(String(127))

    created = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))




class Home(Base):
    __tablename__ = 'home'

    home_id = Column(Integer, primary_key=True)
    name = Column(String(127))
    latitude = Column(String(127))
    longitude = Column(String(127))
    created = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Room(Base):
    __tablename__ = 'room'

    room_id = Column(Integer, primary_key=True)
    name = Column(String(127))
    type = Column(String(127))
    home_id = Column(ForeignKey(u'home.home_id'), nullable=False, index=True)
    created = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    home = relationship(u'Home')


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), server_default=text("''"))
    password = Column(String(127))
    first_name = Column(String(127))
    last_name = Column(String(127))
    date_of_birth = Column(Date)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class UserHomeLink(Base):
    __tablename__ = 'user_home_link'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey(u'user.user_id'), nullable=False, index=True)
    home_id = Column(ForeignKey(u'home.home_id'), nullable=False, index=True)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    home = relationship(u'Home')
    user = relationship(u'User')


class DeviceRoomLink(Base):
    __tablename__ = 'device_room_link'

    id = Column(Integer, primary_key=True)
    device_id = Column(ForeignKey(u'device.device_id'), nullable=False, index=True)
    room_id = Column(ForeignKey(u'room.room_id'), nullable=False, index=True)
    created = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    device = relationship(u'Device')
    room = relationship(u'Room')
