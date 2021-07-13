from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    password = Column(String)
    picture = Column(String)
    google_auth = Column(Boolean)
    hse_auth = Column(Boolean)

    def get_display_name(self) -> str:
        return self.first_name if self.first_name is not None else self.email