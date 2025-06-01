from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
  __tablename__ = "user"
  
  id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
  name: Mapped[str] = mapped_column(db.String(150), nullable=False)
  email: Mapped[str] = mapped_column(db.String(150), nullable=False, unique=True)
  password: Mapped[str] = mapped_column(db.String(100), nullable=False)
  is_admin: Mapped[bool] = mapped_column(db.Boolean, default=False)
  image: Mapped[Optional[str]] = mapped_column(db.String(150), nullable=False, default="uploads/default_user.png")