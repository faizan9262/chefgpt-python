from sqlalchemy import Column, String, Integer, TIMESTAMP, text,ForeignKey,ARRAY
from database import Base


class Favorite(Base):
    __tablename__ = "favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False )
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    recipe = Column(ARRAY(String),nullable=False,index=True)
    image = Column(String,nullable=False,index=True)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()')
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()'),
        server_onupdate=text('now()')
    )
