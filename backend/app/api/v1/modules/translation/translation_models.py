from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid
from datetime import datetime

class Translation(Base):
    __tablename__ = "translations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String(255), nullable=False, index=True)
    locale = Column(String(10), nullable=False, index=True)
    value = Column(Text, nullable=False)
    category = Column(String(100), nullable=True, index=True)  # e.g., 'auth', 'dashboard', 'common'
    description = Column(Text, nullable=True)  # Description for translators
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'key': self.key,
            'locale': self.locale,
            'value': self.value,
            'category': self.category,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TranslationSet(Base):
    __tablename__ = "translation_sets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    locale = Column(String(10), nullable=False, index=True)
    translations = Column(JSON, nullable=False)  # Nested JSON structure
    version = Column(String(50), default="1.0.0")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'locale': self.locale,
            'translations': self.translations,
            'version': self.version,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }