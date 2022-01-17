from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import validates

from database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    password = Column(String(60), nullable=False)
    name = Column(String(64), nullable=False)
    discriminator = Column(String(4), nullable=False)
    display_name = Column(String(64), nullable=False)

    @validates('id')
    def validate_id(self, key, id):
        if type(id) is not int:
            raise TypeError

        if len(str(id)) != 18:
            raise ValueError

        return id

    @validates('password')
    def validate_password(self, key, password):
        if type(password) is not bytes:
            raise TypeError

        return password

    @validates('name')
    def validate_name(self, key, name):
        if type(name) is not str:
            raise TypeError

        if len(name) > 64:
            raise ValueError

        return name

    @validates('discriminator')
    def validate_name(self, key, discriminator):
        if type(discriminator) is not str:
            raise TypeError

        if len(discriminator) != 4:
            raise ValueError

        return discriminator

    @validates('display_name')
    def validate_display_name(self, key, display_name):
        if type(display_name) is not str:
            raise TypeError

        if len(display_name) > 64:
            raise ValueError

        return display_name
