"""
Database models for the VishwaGuru application.

This module defines SQLAlchemy ORM models for storing civic issues
and related information in the database.
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from database import Base
import datetime


class Issue(Base):
    """
    Represents a civic issue reported by users.
    
    This model stores information about reported civic issues such as potholes,
    garbage, vandalism, flooding, and infrastructure problems. Issues can be
    reported via web interface or Telegram bot.
    
    Attributes:
        id: Unique identifier for the issue (primary key)
        description: Detailed description of the issue
        category: Type of issue (e.g., 'pothole', 'garbage', 'vandalism')
        image_path: File path to uploaded evidence image
        source: Origin of the report ('telegram' or 'web')
        status: Current status of the issue (default: 'open')
        created_at: Timestamp when the issue was reported
        user_email: Email address of the reporter (optional)
        upvotes: Number of upvotes from community members
        latitude: Geographic latitude coordinate (optional)
        longitude: Geographic longitude coordinate (optional)
        location: Human-readable location description (optional)
        action_plan: JSON string containing AI-generated action plan (optional)
    """
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    category = Column(String, index=True)
    image_path = Column(String)
    source = Column(String)
    status = Column(String, default="open", index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    user_email = Column(String, nullable=True)
    upvotes = Column(Integer, default=0, index=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    action_plan = Column(Text, nullable=True)
