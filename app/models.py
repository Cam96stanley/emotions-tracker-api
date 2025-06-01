from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy
from datetime import date as DateType
from sqlalchemy import Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


user_moods_feelings = Table(
  "user_moods_feelings",
  Base.metadata,
  db.Column("user_mood_id", db.Integer, db.ForeignKey("user_moods.id"), primary_key=True),
  db.Column("feeling_id", db.Integer, db.ForeignKey("feelings.id"), primary_key=True)
)


class User(db.Model):
  __tablename__ = "users"
  
  id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
  name: Mapped[str] = mapped_column(db.String(150), nullable=False)
  email: Mapped[str] = mapped_column(db.String(150), nullable=False, unique=True)
  password: Mapped[str] = mapped_column(db.String(100), nullable=False)
  is_admin: Mapped[Optional[bool]] = mapped_column(db.Boolean, default=False)
  image: Mapped[Optional[str]] = mapped_column(db.String(150), nullable=False, default="uploads/default_user.png")
  
  user_moods: Mapped[List["UserMood"]] = db.relationship(back_populates="user")


class Mood(db.Model):
  __tablename__ = "moods"
  
  id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
  mood_type: Mapped[str] = mapped_column(db.String(50), nullable=False)
  
  related_user_moods: Mapped[List["UserMood"]] = db.relationship("UserMood", back_populates="mood")


class Feeling(db.Model):
  __tablename__ = "feelings"

  id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
  feeling_name: Mapped[int] = mapped_column(db.String(50), nullable=False)
  user_moods: Mapped[List["UserMood"]] = db.relationship("UserMood", secondary=user_moods_feelings, back_populates="feelings")


class UserMood(db.Model):
  __tablename__ = "user_moods"
  
  id: Mapped[int] = mapped_column(db.Integer(), primary_key=True)
  user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"))
  mood_id: Mapped[int] = mapped_column(db.ForeignKey("moods.id"))
  diary_entry: Mapped[Optional[str]] = mapped_column(db.String(1000))
  sleep_time: Mapped[int] = mapped_column(db.Integer(), nullable=False)
  date: Mapped[DateType] = mapped_column(db.Date, default=lambda: DateType.today())
  
  mood: Mapped["Mood"] = db.relationship("Mood", back_populates="related_user_moods")
  user: Mapped["User"] = db.relationship("User", back_populates="user_moods")
  feelings: Mapped[List["Feeling"]] = db.relationship("Feeling", secondary=user_moods_feelings, back_populates="user_moods")