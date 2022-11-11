from .db import LOCSESSION


def get_db():
    try:
        db=LOCSESSION()
        yield db
    except Exception as e:
        pass
    finally:
        db.close()