from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import backref, relationship
from .meta import Base


class Line(Base):
    __tablename__ = 'lines'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    direction1 = Column(String, nullable=False)
    direction2 = Column(String, nullable=False)
    # Relationship should be defined on the parent only:
    # see https://stackoverflow.com/questions/5033547/sqlalchemy-cascade-delete
    # "Stop" class not being defined yet => string "Stop" allowed here:
    stops = relationship("Stop", cascade="all,delete-orphan", backref="line", passive_deletes=True)

    def to_json(self):
        to_serialize = ['id', 'name', 'direction1', 'direction2']
        d = {}
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d


class Stop(Base):
    __tablename__ = 'stops'
    id = Column('id', Integer, primary_key=True)
    stac_id = Column('stac_id', Integer)
    logical_id = Column('logical_id', Integer)
    # means when a line is deleted, stops belonging to the line also are:
    line_id = Column('line_id', Integer, ForeignKey('lines.id', ondelete='CASCADE'))
    name = Column('name', String, nullable=False)
    order = Column('order', Integer, nullable=False)

    def to_json(self):
        to_serialize = ['logical_id', 'line_id', 'name', 'order']
        d = {
            'id': getattr(self, 'stac_id')
        }
        for attr_name in to_serialize:
            d[attr_name] = getattr(self, attr_name)
        return d
