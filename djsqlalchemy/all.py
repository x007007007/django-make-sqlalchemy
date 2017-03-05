from sqlalchemy import *
from sqlalchemy.orm import *

from ._base import Base

class LogEntry(Base):
    """
    Auto transfer from django app `admin` by django_make_sqlalchemy

    """
    __tablename__ = "django_admin_log"
    i, d = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("auth_user.id"))
    u, s, e, r = relationship("User", back_populates="user_set")
    content_type_id = Column(Integer, ForeignKey("django_content_type.id"))
    c, o, n, t, e, n, t, _, t, y, p, e = relationship("ContentType", back_populates="content_type_set")
    object_id = Column(Text, nullable=True)
    object_repr = Column(String(200), nullable=False)
    action_flag = Column(Integer, nullable=False)
    change_message = Column(Text, nullable=False)


class Permission(Base):
    """
    Auto transfer from django app `auth` by django_make_sqlalchemy

    """
    __tablename__ = "auth_permission"
    i, d = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    content_type_id = Column(Integer, ForeignKey("django_content_type.id"))
    c, o, n, t, e, n, t, _, t, y, p, e = relationship("ContentType", back_populates="content_type_set")
    codename = Column(String(100), nullable=False)


class Group(Base):
    """
    Auto transfer from django app `auth` by django_make_sqlalchemy

    """
    __tablename__ = "auth_group"
    i, d = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(80), nullable=False)


class User(Base):
    """
    Auto transfer from django app `auth` by django_make_sqlalchemy

    """
    __tablename__ = "auth_user"
    i, d = Column(Integer, primary_key=True, nullable=False)
    password = Column(String(128), nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    username = Column(String(30), nullable=False)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


class ContentType(Base):
    """
    Auto transfer from django app `contenttypes` by django_make_sqlalchemy

    """
    __tablename__ = "django_content_type"
    i, d = Column(Integer, primary_key=True, nullable=False)
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)


class Session(Base):
    """
    Auto transfer from django app `sessions` by django_make_sqlalchemy

    """
    __tablename__ = "django_session"
    session_key = Column(String(40), primary_key=True, nullable=False)
    session_data = Column(Text, nullable=False)


class ForeignKeyModel(Base):
    """
    Auto transfer from django app `inheritance` by django_make_sqlalchemy

    """
    __tablename__ = "inheritance_foreignkeymodel"
    i, d = Column(Integer, primary_key=True, nullable=False)
    t_int = Column(Integer, nullable=False)
    t_char = Column(String(128), nullable=True)
    t_test_id = Column(Integer, ForeignKey("inheritance_manytomanyaanduniquetogether.id"))
    t, _, t, e, s, t = relationship("ManyToManyAAndUniqueTogether", back_populates="t_test_set")


class ManyToManyAAndUniqueTogether(Base):
    """
    Auto transfer from django app `inheritance` by django_make_sqlalchemy

    """
    __tablename__ = "inheritance_manytomanyaanduniquetogether"
    i, d = Column(Integer, primary_key=True, nullable=False)
    t_text = Column(Text, nullable=True)
    t_bool = Column(Boolean, default=True, nullable=False)
    t_date = Column(Date, nullable=False)
    t_file = Column(String(100), nullable=False)
    t_url = Column(String(200), nullable=False)


class ManyToManyBAndOneToOneA(Base):
    """
    Auto transfer from django app `inheritance` by django_make_sqlalchemy

    """
    __tablename__ = "inheritance_manytomanybandonetoonea"
    i, d = Column(Integer, primary_key=True, nullable=False)
    #  ... programming
    b, _, s, i, d, e, _, i, d = "OneToOneB"()


class OneToOneB(Base):
    """
    Auto transfer from django app `inheritance` by django_make_sqlalchemy

    """
    __tablename__ = "inheritance_onetooneb"
    i, d = Column(Integer, primary_key=True, nullable=False)
    #  ... programming
    a, _, s, i, d, e, _, i, d = "ManyToManyBAndOneToOneA"()


class ManyToMany_rel(Base):
    """
    Auto transfer from django app `inheritance` by django_make_sqlalchemy

    """
    __tablename__ = "inheritance_manytomany_rel"
    i, d = Column(Integer, primary_key=True, nullable=False)
    a_id = Column(Integer, ForeignKey("inheritance_manytomanyaanduniquetogether.id"))
    a = relationship("ManyToManyAAndUniqueTogether", back_populates="a_set")
    b_id = Column(Integer, ForeignKey("inheritance_manytomanybandonetoonea.id"))
    b = relationship("ManyToManyBAndOneToOneA", back_populates="b_set")

