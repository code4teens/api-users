from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    func,
    SmallInteger,
    String
)
from sqlalchemy.orm import relationship, validates

from database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    password = Column(String(60), nullable=True)  # TODO: phase-out
    name = Column(String(64), nullable=False)
    discriminator = Column(String(4), nullable=False)
    display_name = Column(String(64), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    last_updated = Column(DateTime, nullable=False, default=func.now())

    @validates('id')
    def validate_id(self, _, id):
        if type(id) is not int:
            raise TypeError

        if len(str(id)) != 18:
            raise ValueError

        return id

    # TODO: phase-out
    @validates('password')
    def validate_password(self, _, password):
        if type(password) is not bytes:
            raise TypeError

        return password

    @validates('name')
    def validate_name(self, _, name):
        if type(name) is not str:
            raise TypeError

        if len(name) > 64:
            raise ValueError

        return name

    @validates('discriminator')
    def validate_discriminator(self, _, discriminator):
        if type(discriminator) is not str:
            raise TypeError

        if len(discriminator) != 4:
            raise ValueError

        return discriminator

    @validates('display_name')
    def validate_display_name(self, _, display_name):
        if type(display_name) is not str:
            raise TypeError

        if len(display_name) > 64:
            raise ValueError

        return display_name

    @validates('is_admin')
    def validate_is_admin(self, _, is_admin):
        if type(is_admin) is not bool:
            raise TypeError

        return is_admin


class Cohort(Base):
    __tablename__ = 'cohort'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    nickname = Column(String(16), nullable=False)
    duration = Column(SmallInteger, nullable=False)
    start_date = Column(Date, nullable=False)


class Enrolment(Base):
    __tablename__ = 'enrolment'
    id = Column(SmallInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.id'), nullable=False)
    cohort_id = Column(SmallInteger, ForeignKey('cohort.id'), nullable=False)

    user = relationship('User')
    cohort = relationship('Cohort')

    @validates('user_id')
    def validate_user_id(self, _, user_id):
        if type(user_id) is not int:
            raise TypeError

        if len(str(user_id)) != 18:
            raise ValueError

        return user_id

    @validates('cohort_id')
    def validate_cohort_id(self, _, cohort_id):
        if type(cohort_id) is not int:
            raise TypeError

        return cohort_id
