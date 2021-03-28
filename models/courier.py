from sqlalchemy import Column, Integer, String, ARRAY, Float
from sqlalchemy_utils import DateTimeRangeType, IntRangeType
from sqlalchemy.ext.hybrid import hybrid_property
from models.base import Base


class Courier(Base):
    __tablename__ = 'couriers'
    courier_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    courier_type = Column(String, nullable=False)
    regions = Column(ARRAY(Integer), nullable=False)
    working_hours = Column(ARRAY(DateTimeRangeType), nullable=False)

    @hybrid_property
    def weight(self):
        w = {'foot': 10, 'bike': 15, 'car': 50}
        return w[self.courier_type]
