import datetime
import sqlalchemy as sa
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    DateTime,
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words
from pyramid.security import Allow, ALL_PERMISSIONS
import random


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    email = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    posts = relationship("Post", backref="users")
    last_logged = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def by_name(cls, name):
        return DBSession.query(User).filter(User.name == name).first()

    def verify_password(self, password):
        return self.password == password


class TempUser(Base):
    __tablename__ = 'tempusers'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), unique=True, nullable=False)
    email = Column(Unicode(255), unique=True, nullable=False)
    password = Column(Unicode(255), nullable=False)
    verify = Column(Integer, nullable=False)

    def __init__(self):
        self.verify = random.getrandbits(31) + (1 << 31)

    @classmethod
    def by_verify(cls, verify):
        return DBSession.query(TempUser).filter(TempUser.verify == verify).first()

    def upgrade(self):
        user = User()
        user.name = self.name
        user.email = self.email
        user.password = self.password
        DBSession.add(user)
        DBSession.delete(self)
        return None


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    owner = Column(Integer, ForeignKey('users.name'))
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def all(cls):
        return DBSession.query(Post).order_by(sa.desc(Post.created))

    @classmethod
    def by_id(cls, id):
        return DBSession.query(Post).filter(Post.id == id).first()

    @classmethod
    def get_owner(cls, owner):
        return DBSession.query(Post).filter(Post.owner == owner).all()

    @property
    def slug(self):
        return urlify(self.title)

    @property
    def created_in_words(self):
        return time_ago_in_words(self.created)

    @property
    def __acl__(self):
        return [
            (Allow, self.owner, 'edit'),
        ]

    @classmethod
    def get_paginator(cls, request, page=1):
        page_url = PageURL_WebOb(request)
        return Page(Post.all(), page, url=page_url, items_per_page=15)
