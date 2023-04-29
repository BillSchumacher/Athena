from sqlalchemy import BigInteger, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from athena.db import Base


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    base_url = Column(String, nullable=False)

    endpoints = relationship("Endpoint", back_populates="model")


class Endpoint(Base):
    __tablename__ = "endpoints"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    path = Column(String, nullable=False)

    model_id = Column(Integer, ForeignKey("models.id"))
    model = relationship("Model", back_populates="endpoints")

    costs = relationship("Cost", back_populates="endpoint")
    rate_limits = relationship("RateLimit", back_populates="endpoint")


class Cost(Base):
    __tablename__ = "costs"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cost_per_use = Column(Float, nullable=False)

    endpoint_id = Column(Integer, ForeignKey("endpoints.id"))
    endpoint = relationship("Endpoint", back_populates="costs")


class RateLimit(Base):
    __tablename__ = "rate_limits"

    id = Column(Integer, primary_key=True)
    rate_limit = Column(Integer, nullable=False)
    time_interval = Column(Integer, nullable=False)  # In seconds

    endpoint_id = Column(Integer, ForeignKey("endpoints.id"))
    endpoint = relationship("Endpoint", back_populates="rate_limits")


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    prompt = Column(String, nullable=False)


class Completion(Base):
    __tablename__ = "completions"

    id = Column(BigInteger, primary_key=True)
    timestamp = Column(BigInteger, nullable=False)
    completion = Column(String, nullable=False)
    prompt_id = Column(BigInteger, ForeignKey("prompts.id"))
    prompt = relationship("Prompt", back_populates="completions")
    endpoint_id = Column(Integer, ForeignKey("endpoints.id"))
    endpoint = relationship("Endpoint", back_populates="completions")


class Context(Base):
    __tablename__ = "contexts"

    id = Column(BigInteger, primary_key=True)
    role = Column(String, nullable=True)
    context = Column(String, nullable=False)
    completion_id = Column(BigInteger, ForeignKey("completions.id"))
    completion = relationship("Completion", back_populates="contexts")
