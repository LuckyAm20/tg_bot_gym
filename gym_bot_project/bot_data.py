import os

import telebot

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///gym_helper.db')
# Base = declarative_base()
# Session = sessionmaker(bind=engine)

bot = telebot.TeleBot(os.getenv('TELEGRAM_API_TOKEN'))

Base = declarative_base()
engine = create_engine(os.getenv('DATABASE_URL'))
Session = sessionmaker(bind=engine)
