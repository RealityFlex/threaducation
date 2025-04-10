import sqlalchemy as sa
from database import Base


class ProfileType(Base):
    __tablename__ = "profile_type"
    
    type_id = sa.Column(sa.BigInteger, primary_key=True)
    name = sa.Column(sa.String, nullable=False, unique=True)


class User(Base):
    __tablename__ = "user_table"
    
    user_id = sa.Column(sa.BigInteger, primary_key=True)
    login = sa.Column(sa.String, nullable=False, unique=True)
    password = sa.Column(sa.String, nullable=False)
    type_id = sa.Column(sa.BigInteger, sa.ForeignKey("profile_type.type_id"), nullable=False)
    name = sa.Column(sa.String, nullable=False)
    image = sa.Column(sa.String, nullable=True)
    description = sa.Column(sa.Text, nullable=True)
    rating = sa.Column(sa.Integer, nullable=True)