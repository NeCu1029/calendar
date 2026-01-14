# 잡다한 것들

import random
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


def make_code(length: int) -> str:
    res = []
    for _ in range(length):
        res.append(chr(random.randint(0, 25) + 97))
    return "".join(res)
