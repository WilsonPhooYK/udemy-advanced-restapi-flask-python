from ma import ma
from models.confirmation import ConfirmationModel  # type: ignore

SQLAlchemyAutoSchema = ma.SQLAlchemyAutoSchema


class ConfirmationSchema(SQLAlchemyAutoSchema):
    class Meta:  # type: ignore
        model = ConfirmationModel
        load_only = ("user",)
        dump_only = ("id", "expired_at", "confirmed")
        load_instance = True
        include_fk = True
