from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import validates

from database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    password = Column(String(60), nullable=False)

    @validates('password')
    def validate_password(self, key, password):
        if type(password) is not bytes:
            raise TypeError

        return password
