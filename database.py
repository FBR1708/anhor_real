from sqlalchemy import create_engine, Column, Integer, String, LargeBinary, DateTime, func
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("postgresql://postgres:1@localhost:5432/menu")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Menu(Base):
    __tablename__ = 'menu_taom'

    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    callback_data = Column(String(300))
    price = Column(String(300))
    food_id = Column(Integer, nullable=True)



class MainMenu(Base):
    __tablename__ = 'main_menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    food_picture = Column(LargeBinary, nullable=True)
    price = Column(String(300), nullable=True)



