import ormar

from ..models.baseMeta.base_meta import BaseMeta
           
class Log(ormar.Model):
    class Meta(BaseMeta):
        tablename = "logs"

    id: int = ormar.Integer(primary_key=True)
    address: str = ormar.String(max_length=64)
    method: str = ormar.String(max_length=10)
    epoch: int = ormar.Integer()
