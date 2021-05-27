from typing import Any, cast
from flask_marshmallow import Marshmallow


class MarshmallowExtended(Marshmallow):
    Nested: Any = ...


# Modified one that can talk to our flask app
ma: MarshmallowExtended = cast(MarshmallowExtended, Marshmallow())
