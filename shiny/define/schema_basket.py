from __future__ import annotations
from typing import (
    List,
    Union,
    Type,
)

from pydantic import (
    BaseModel,
)

from .type import (
    all_enum_values,
    Colors,
)
from .schema_fruit import (
    Fruit,
    Apple,
    Orange,
)


BasketItem = Union[Fruit, "Basket"]
BasketList = List[BasketItem]
BasketListType = List[Union[Type[Fruit], Type[Basket]]]


class BasketRestrictions(BaseModel):
    limit: int = 3
    max_weight: float = 10.0
    allowed_colors: List[Colors] = all_enum_values(Colors)
    allowed_types: BasketListType = [Type[Fruit], Type[Basket]]


BasketRestrictions.update_forward_refs()


class Basket(BaseModel):
    id: int
    restrictions: BasketRestrictions = BasketRestrictions()
    items: BasketList

    def __pretty__(*args, **kwargs):
        self = None
        if args and args[0] and isinstance(args[0], Basket):
            self = args[0]
            args = args[1:]
            return super(Basket, self).__pretty__(**kwargs)

        return ["Basket Type"]


Basket.update_forward_refs()
