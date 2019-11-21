from __future__ import annotations
import string
from typing import (
    Union,
    Dict,
    AnyStr,
)

from .define import (
    Basket,
    BasketRestrictions,
    Fruit,
    Apple,
    Orange,
)
from .define.type import (
    Colors,
    BasketRestrictionsSet,
)


class BasketStructure:
    def __init__(self):
        self.restrictions = self.define_restrictions()
        self.root = None

    @staticmethod
    def define_restrictions() -> BasketRestrictionsSet:
        apple_basket_outside_restrictions = BasketRestrictions(
            limit=7,
            max_weight=20.0,
            allowed_colors=[Colors.GREEN, Colors.YELLOW, Colors.RED],
            allowed_types=[Basket, Apple],
        )
        orange_basket_outside_restrictions = BasketRestrictions(
            limit=2,
            allowed_colors=[Colors.ORANGE, Colors.YELLOW],
            allowed_types=[Basket, Orange]
        )

        return {
            'root': BasketRestrictions(
                allowed_types=[Basket, Fruit],
            ),
            'apple': {
                'inside': BasketRestrictions(**{
                    **apple_basket_outside_restrictions.dict(),
                    'allowed_types': [Apple]
                }),
                'outside': apple_basket_outside_restrictions,
            },
            'orange': {
               'inside': BasketRestrictions(**{
                        **orange_basket_outside_restrictions.dict(),
                        'limit': 3,
                        'allowed_types': [Orange],
                }),
               'outside': orange_basket_outside_restrictions,
            },
        }

    def create(self: BasketStructure) -> Basket:
        """Test basket structure with the following rules
            1. Root bucket can contain only buckets
            2. 2nd level buckets can contain either fruits or buckets
            3. 3rd level buckets can contain only fruits of its 2nd level type

        :return:
        """
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
                            restrictions=self.restrictions['apple']['inside'],
                        ),
                    ],
                    restrictions=self.restrictions['apple']['outside'],
                ),
                Basket(
                    id=12,
                    items=[
                        Orange(weight=3.2, color=Colors.YELLOW),
                        Basket(
                            id=121,
                            items=[
                            ],
                            restrictions=self.restrictions['orange']['inside'],
                        ),
                    ],
                    restrictions=self.restrictions['orange']['outside'],
                ),
            ],
            restrictions=self.restrictions['root'],
        )

        self.root = root
        return root
