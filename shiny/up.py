#!/usr/bin/env python
from __future__ import annotations

from datetime import datetime
from enum import IntEnum
from functools import partial

from typing import (
    List,
    Union,
    ForwardRef,
    Type,
    Optional,
)

from devtools import debug
from pydantic import (
    BaseModel,
    ValidationError,
)


def all_enum_values(int_enum_type):
    return [el for el in int_enum_type]


class Colors(IntEnum):
    RED, GREEN, BLUE, ORANGE, YELLOW = range(5)


class AppleVariety(IntEnum):
    ANTONOVKA, NEANTONOVKA = range(2)


class OrangeVariety(IntEnum):
    SMALL, BIG, PLANET_SIZE = range(3)


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


Basket = ForwardRef('Basket')
BasketItem = Union[Fruit, Basket]
BasketList = List[BasketItem]
BasketListType = List[Union[Type[Apple], Type[Orange], Type[Basket]]]


class BasketRestrictions(BaseModel):
    limit: int = 3
    max_weight: float = 10.0
    allowed_colors: List[Colors] = all_enum_values(Colors)
    allowed_types: BasketListType = [Fruit, Basket]


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


BasketRestrictions.update_forward_refs()
Basket.update_forward_refs()


def process_baskets():
    """Test basket structure with the following rules
        1. Root bucket can contain only buckets
        2. 2nd level buckets can contain either fruits or buckets
        3. 3rd level buckets can contain only fruits of its 2nd level type

    :return:
    """
    try:
        apple_basket_outside_restrictions = BasketRestrictions(
            limit=7,
            max_weight=20.0,
            allowed_colors=[Colors.GREEN, Colors.YELLOW, Colors.RED],
            allowed_types=[Basket, Apple],
        )
        apple_basket_inside_restrictions = BasketRestrictions(
            **{
                **apple_basket_outside_restrictions.dict(),
                'allowed_types': [Apple]
            }
        )
        orange_basket_outside_restrictions = BasketRestrictions(
            limit=2,
            allowed_colors=[Colors.ORANGE, Colors.YELLOW],
            allowed_types=[Basket, Orange]
        )
        orange_basket_inside_restrictions = BasketRestrictions(
            **{
                **apple_basket_outside_restrictions.dict(),
                'limit': 3,
                'allowed_types': [Orange],
            }
        )
        root_restrictions = BasketRestrictions(
            allowed_types=[Basket, Fruit],
        )

        root = Basket(
            id=1,
            items=[
                Basket(
                    id=11,
                    items=[
                        Apple(weight=1.7, color=Colors.GREEN),
                        Apple(weight=4.8, color=Colors.YELLOW),
                        Apple(weight=2.3, color=Colors.RED),
                        Basket(
                            id=111,
                            items=[
                                Apple(weight=2.0, color=Colors.GREEN),
                                Apple(weight=2.2, color=Colors.GREEN),
                            ],
                            restrictions=apple_basket_inside_restrictions,
                        ),
                    ],
                    restrictions=apple_basket_outside_restrictions,
                ),
                Basket(
                    id=12,
                    items=[
                        Orange(weight=3.2, color=Colors.YELLOW),
                        Basket(
                            id=121,
                            items=[
                            ],
                            restrictions=orange_basket_inside_restrictions,
                        ),
                    ],
                    restrictions=orange_basket_outside_restrictions,
                ),
            ],
            restrictions=root_restrictions,
        )
    except ValidationError as exc:
        print(exc.json() + '\n')
    else:
        debug(root)


def main():
    print("Up!")
    process_baskets()


if __name__ == "__main__":
    main()
