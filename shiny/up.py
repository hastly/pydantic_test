#!/usr/bin/env python
from __future__ import annotations

from devtools import debug  # type: ignore
from pydantic import ValidationError

from shiny.try_basket import BasketStructure


def main():
    print("Up!")

    structure = BasketStructure()
    try:
        root = structure.create()
    except ValidationError as exc:
        print(exc.json() + '\n')
    else:
        debug(root)


if __name__ == "__main__":
    main()
