from typing import cast
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from typings.sql_alchemy import SQLAlchemy as SQLAlchemyStub

convention = {
    "ix": "ix_%(column_0_label)s", # Index names - 1st column in compound index as label
    "uq": "uq_%(table_name)s_%(column_0_name)s", # Unique constraint
    "ck": "ck_%(table_name)s_%(constraint_name)s", # Check constraint
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s", # Foreign key constraint
    "pk": "pk_%(table_name)s", # Primary key constraint
}

metadata = MetaData(naming_convention=convention)
db: SQLAlchemyStub = cast(SQLAlchemyStub, SQLAlchemy(metadata=metadata))
