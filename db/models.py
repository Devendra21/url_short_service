from sqlalchemy import Column, Integer, String, DateTime
import datetime
# from sqlalchemy.orm import relationship

from .database import Base


class UrlModel(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String(255), nullable=False, index=True)
    shortcode = Column(String(7), unique=True, index=True, nullable=False)
    redirectCount = Column(Integer, nullable=False, default=0)
    created = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    lastRedirect = Column(DateTime, onupdate=datetime.datetime.now(datetime.timezone.utc))
