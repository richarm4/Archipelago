from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import NarutoWorld

ITEM_NAME_TO_ID = {
    "Iruka Umino Coupon": 1,
    "Neji Hyuga Coupon": 2,
    "Kankuro Coupon": 3,
    "Haku Coupon": 4,
    "Might Guy Coupon": 5,
    "Zabuza Coupon": 6,
    "Crow Coupon": 7,
    "Nine-Tailed Naruto Coupon": 8,
    "Kakashi with Sharingan Coupon": 9,
    "Akamaru Coupon": 10,
    "Sasuke with Sharingan Coupon": 11,
    "Orochimaru Coupon": 12,
    "Mizuki Coupon": 13,
    "Seal Coupon": 14,
    "HP Coupon": 15,
    "1000 Coins": 16
}
ID_TO_ITEM_NAME = dict(zip(ITEM_NAME_TO_ID.values(), ITEM_NAME_TO_ID.keys()))


DEFAULT_ITEM_CLASSIFICATIONS = {
x: ItemClassification.progression if "Coupon" in x else ItemClassification.filler for x in list(ITEM_NAME_TO_ID.keys())
}


class NarutoItem(Item):
    game = "Naruto Clash of Ninja 2"


def get_random_filler_item_name(world: NarutoWorld) -> str:
    return "1000 Coins"


def create_item_with_correct_classification(world: NarutoWorld, name: str) -> NarutoItem:
    return NarutoItem(name, DEFAULT_ITEM_CLASSIFICATIONS[name], ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: NarutoWorld) -> None:

    itempool: list[Item] = [
        world.create_item(x) for x in list(ITEM_NAME_TO_ID.keys())
    ]

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items
   
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    world.multiworld.itempool += itempool
