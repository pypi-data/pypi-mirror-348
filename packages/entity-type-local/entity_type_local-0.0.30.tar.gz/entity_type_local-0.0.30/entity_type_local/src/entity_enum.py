import enum

# TODO We should generate this with Sql2Code to become table driven and always updated


class EntityTypeId(enum.Enum):
    ENTITY_TYPE = 2
    PERSONAL_PROFILE = 6
    CONTACT = 7
    SMARTLINK = 18
    TEST = 22
