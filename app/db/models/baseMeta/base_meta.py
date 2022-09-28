import ormar 

import app.db.db as _file_

class BaseMeta(ormar.ModelMeta):
    metadata = _file_.metadata
    database = _file_.db
