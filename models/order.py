from sqlalchemy import Column, Integer, String, ARRAY, Float, DateTime
from sqlalchemy_utils import DateTimeRangeType
from models.base import Base


class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    weight = Column(Float, nullable=False)
    region = Column(Integer, nullable=False)
    delivery_hours = Column(ARRAY(DateTimeRangeType), nullable=False)
    status = Column(String, nullable=False, default='created')
    assign_time = Column(DateTime)
    complete_time = Column(DateTime)
    cour_id = Column(Integer)
