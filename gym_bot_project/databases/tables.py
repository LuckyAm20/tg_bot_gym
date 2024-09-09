from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from gym_bot_project.bot_data import Base


class Role(Base):
    __tablename__ = 'roles'
    user_id = Column(Integer, primary_key=True)
    role = Column(String)
    username = Column(String)
    students = relationship("Relation", back_populates="trainer", foreign_keys="[Relation.trainer_id]")
    trainers = relationship("Relation", back_populates="student", foreign_keys="[Relation.student_id]")
    plans = relationship("Plan", back_populates="role")
    videos = relationship("Video", back_populates="role")


class Relation(Base):
    __tablename__ = 'relations'
    student_id = Column(Integer, ForeignKey('roles.user_id'), primary_key=True)
    trainer_id = Column(Integer, ForeignKey('roles.user_id'), primary_key=True)
    student = relationship("Role", back_populates="trainers", foreign_keys=[student_id])
    trainer = relationship("Role", back_populates="students", foreign_keys=[trainer_id])


class Plan(Base):
    __tablename__ = 'plans'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('roles.user_id'))
    plan_type = Column(String, nullable=False)
    plan_date = Column(Date, nullable=False)
    plan = Column(Text)
    role = relationship("Role", back_populates="plans")
    __table_args__ = (UniqueConstraint('user_id', 'plan_type', 'plan_date', name='unique_plan'),)


class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('roles.user_id'))
    video_url = Column(Text)
    upload_date = Column(String)
    role = relationship("Role", back_populates="videos")
