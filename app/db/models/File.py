import ormar

from ...utils.env import get_env

from ..models.baseMeta.base_meta import BaseMeta
           
config = get_env("app", False)

class File(ormar.Model):
    class Meta(BaseMeta):
        tablename = "files"

    id: int = ormar.Integer(primary_key=True)
    original_namestring: str = ormar.String(max_length=int(config("MAX_FILENAME_LENGTH")), nullable=False)
    headers: str = ormar.String(max_length=2048)
