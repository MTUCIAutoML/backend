from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from models.base import Base

pwd_context = CryptContext(schemes=["sha256_crypt"])


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True,
                                       deferred=True, deferred_group="sensitive")
    __password: Mapped[str] = mapped_column("password", nullable=False,
                                            deferred=True, deferred_group="sensitive")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False,
                                                 server_default=func.current_timestamp(),
                                                 deferred=True, deferred_group="date")

    @hybrid_property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = pwd_context.hash(password)

    @hybrid_method
    def verify_password(self, password):
        return pwd_context.verify(password, self.__password)
