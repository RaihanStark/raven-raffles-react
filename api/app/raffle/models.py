from app import db
from sqlalchemy import Binary, Column, Integer, String, Date

class Shoes(db.Model):
    __tablename__ = 'Shoes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(String)
    img = Column(String)
    price = Column(String)
    sizes = Column(String)
    sites = Column(String)
    link = Column(String)

    def __repr__(self):
        return str(self.name)