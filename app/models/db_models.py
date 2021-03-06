from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String, nullable=True)
    password = Column(String, nullable=True)
    disabled = Column(Boolean, default=False)
    picture = Column(String, nullable=True)
    google_auth = Column(Boolean)
    hse_auth = Column(Boolean)

    def get_display_name(self) -> str:
        return self.first_name if self.first_name is not None else self.email