from enum import Enum


class Category(Enum):
    APP = "app"
    TASK = "task"
    QUERY = "query"


class Valid(Enum):
    YES = "yes"
    NO = "no"


class Apps(Enum):
    PADDY_FIELD = "paddyfield"
