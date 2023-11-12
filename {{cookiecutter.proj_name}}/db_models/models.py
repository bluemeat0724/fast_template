"""
Author: G
Time: 2023 2023/11/2 16:48
File: models.py
"""
from sqlalchemy.orm import declarative_base, registry
from sqlalchemy import UniqueConstraint, Column, Integer, String, BigInteger, FLOAT, DateTime, JSON, Text, Boolean
from datetime import datetime
from db_models.base import ModelBase

