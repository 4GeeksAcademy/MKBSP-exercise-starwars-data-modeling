import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Table, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationship between BlogPost and Tag
blogpost_tag_association = Table(
    'blogpost_tag', Base.metadata,
    Column('blogpost_id', Integer, ForeignKey('blogpost.id')),
    Column('tag_id', Integer, ForeignKey('tag.id'))
)

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    profile_picture = Column(String(250))
    bio = Column(Text)
    linkedin = Column(String(250))
    facebook = Column(String(250))

    user = relationship("User", back_populates="person")
    addresses = relationship("Address", back_populates="person")

class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    street_name = Column(String(150))
    street_number = Column(String(50))
    post_code = Column(String(250))
    country = Column(String(150))
    city = Column(String(250))
    person_id = Column(Integer, ForeignKey('person.id'))

    person = relationship("Person", back_populates="addresses")

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    date_joined = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    person = relationship("Person", back_populates="user")
    favorites = relationship("Favorite", back_populates="user")
    blogposts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="user")
    favorite_blogposts = relationship("FavoriteBlogPost", back_populates="user")

class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(250))
    birth_year = Column(String(20))
    gender = Column(String(20))
    height = Column(String(20))
    movies = Column(String(250))
    comics = Column(String(250))
    books = Column(String(250))

    favorites = relationship("Favorite", back_populates="character")

class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    climate = Column(String(100))
    terrain = Column(String(100))
    population = Column(String(100))
    diameter = Column(String(100))
    movies = Column(String(250))
    comics = Column(String(250))
    books = Column(String(250))

    favorites = relationship("Favorite", back_populates="planet")

class Favorite(Base):
    __tablename__ = 'favorite'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    character_id = Column(Integer, ForeignKey('character.id'), nullable=True)
    planet_id = Column(Integer, ForeignKey('planet.id'), nullable=True)
    date_added = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")
    character = relationship("Character", back_populates="favorites")
    planet = relationship("Planet", back_populates="favorites")

class BlogPost(Base):
    __tablename__ = 'blogpost'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    content = Column(Text, nullable=False)
    date_posted = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))

    author = relationship("User", back_populates="blogposts")
    comments = relationship("Comment", back_populates="blogpost")
    tags = relationship("Tag", secondary=blogpost_tag_association, back_populates="blogposts")
    favorite_blogposts = relationship("FavoriteBlogPost", back_populates="blogpost")

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    date_posted = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))
    blog_post_id = Column(Integer, ForeignKey('blogpost.id'))

    user = relationship("User", back_populates="comments")
    blogpost = relationship("BlogPost", back_populates="comments")

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    blogposts = relationship("BlogPost", secondary=blogpost_tag_association, back_populates="tags")

class FavoriteBlogPost(Base):
    __tablename__ = 'favorite_blogpost'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    blog_post_id = Column(Integer, ForeignKey('blogpost.id'))
    date_added = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorite_blogposts")
    blogpost = relationship("BlogPost", back_populates="favorite_blogposts")

# Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
