from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://ylab_user:qwe123@localhost/ylab_dz"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()


class Menu(Base):
    __tablename__ = 'Menus'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    submenues = relationship('Submenu', cascade='save-update, merge, delete')


class Submenu(Base):
    __tablename__ = 'Submenus'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    menu_id = Column(Integer, ForeignKey('Menus.id'))
    dishes = relationship('Dish', cascade='save-update, merge, delete')


class Dish(Base):
    __tablename__ = 'Dishes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float)
    submenu_id = Column(Integer, ForeignKey('Submenus.id'))


SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()
