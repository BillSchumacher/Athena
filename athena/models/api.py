from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from athena.db import Base


class Model(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    endpoints = relationship('Endpoint', back_populates='model')


class Endpoint(Base):
    __tablename__ = 'endpoints'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    model_id = Column(Integer, ForeignKey('models.id'))
    model = relationship('Model', back_populates='endpoints')

    costs = relationship('Cost', back_populates='endpoint')
    rate_limits = relationship('RateLimit', back_populates='endpoint')


class Cost(Base):
    __tablename__ = 'costs'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cost_per_use = Column(Float, nullable=False)

    endpoint_id = Column(Integer, ForeignKey('endpoints.id'))
    endpoint = relationship('Endpoint', back_populates='costs')


class RateLimit(Base):
    __tablename__ = 'rate_limits'

    id = Column(Integer, primary_key=True)
    rate_limit = Column(Integer, nullable=False)
    time_interval = Column(Integer, nullable=False)  # In seconds

    endpoint_id = Column(Integer, ForeignKey('endpoints.id'))
    endpoint = relationship('Endpoint', back_populates='rate_limits')
