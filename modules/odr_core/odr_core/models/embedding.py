# odr_core/models/embedding.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON,
    Enum,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from odr_core.models.base import Base
import enum
from pgvector.sqlalchemy import Vector


class EmbeddingEngineType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    VOICE = "voice"
    MUSIC = "music"
    TEXT = "text"


class EmbeddingEngine(Base):
    __tablename__ = "embedding_engines"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(EmbeddingEngineType))
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    version = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    supported = Column(Boolean, default=False)

    # Relationships
    content_embeddings = relationship(
        "ContentEmbedding", back_populates="embedding_engine"
    )
    annotation_embeddings = relationship(
        "AnnotationEmbedding", back_populates="embedding_engine"
    )

    def __repr__(self):
        return f"<EmbeddingEngine(id={self.id}, name='{self.name}', version='{self.version}')>"


class ContentEmbedding(Base):
    __tablename__ = "content_embeddings"
    __table_args__ = (
        UniqueConstraint(
            "content_id", "embedding_engine_id", name="ic_content_embedding_engine"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"))
    embedding = Column(Vector(512))
    embedding_engine_id = Column(Integer, ForeignKey("embedding_engines.id"))
    from_user_id = Column(Integer, ForeignKey("users.id"))
    from_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    content = relationship("Content", back_populates="embeddings")
    embedding_engine = relationship(
        "EmbeddingEngine", back_populates="content_embeddings"
    )
    from_user = relationship("User", back_populates="content_embeddings")
    from_team = relationship("Team", back_populates="content_embeddings")


class AnnotationEmbedding(Base):
    __tablename__ = "annotation_embeddings"
    __table_args__ = (
        UniqueConstraint(
            "annotation_id",
            "embedding_engine_id",
            name="ic_annotation_embedding_engine",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    annotation_id = Column(Integer, ForeignKey("annotations.id"))
    embedding = Column(Vector(384))
    embedding_engine_id = Column(Integer, ForeignKey("embedding_engines.id"))
    from_user_id = Column(Integer, ForeignKey("users.id"))
    from_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    annotation = relationship("Annotation", back_populates="embeddings")
    embedding_engine = relationship(
        "EmbeddingEngine", back_populates="annotation_embeddings"
    )
    from_user = relationship("User", back_populates="annotation_embeddings")
    from_team = relationship("Team", back_populates="annotation_embeddings")
