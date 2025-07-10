from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    def __repr__(self):
        cls = type(self)
        attrs = ", ".join(
            f"{key}={getattr(self, key)!r}"
            for key in self.__table__.columns.keys()
        )
        return f"<{cls.__name__}({attrs})>"
