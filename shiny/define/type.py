from enum import IntEnum


def all_enum_values(int_enum_type):
    return [el for el in int_enum_type]


class Colors(IntEnum):
    RED, GREEN, BLUE, ORANGE, YELLOW = range(5)


class AppleVariety(IntEnum):
    ANTONOVKA, NEANTONOVKA = range(2)


class OrangeVariety(IntEnum):
    SMALL, BIG, PLANET_SIZE = range(3)