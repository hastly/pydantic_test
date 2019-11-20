from pydantic import (
    BaseModel,
)

from .type import (
    AppleVariety,
    OrangeVariety,
    Colors,
)


class Fruit(BaseModel):
    weight: float
    color: Colors

    def __pretty__(*args, **kwargs):
        if args and args[0] and isinstance(args[0], Fruit):
            self = args[0]
            args = args[1:]
            return super(Fruit, self).__pretty__(**kwargs)

        return ["Fruit Type"]


class Apple(Fruit):
    variety: AppleVariety = AppleVariety.ANTONOVKA

    def __pretty__(*args, **kwargs):
        self = None
        if args and args[0] and isinstance(args[0], Apple):
            self = args[0]
            args = args[1:]
            return super(Apple, self).__pretty__(**kwargs)

        return ["Apple Type"]


class Orange(Fruit):
    variety: OrangeVariety = OrangeVariety.PLANET_SIZE

    def __pretty__(*args, **kwargs):
        self = None
        if args and args[0] and isinstance(args[0], Orange):
            self = args[0]
            args = args[1:]
            return super(Orange, self).__pretty__(**kwargs)

        return ["Orange Type"]
