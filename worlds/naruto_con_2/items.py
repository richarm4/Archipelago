from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import NarutoWorld

ITEM_NAME_TO_ID = {
    "Iruka Umino Ticket": 1,
    "Neji Hyuga Ticket": 2,
    "Kankuro Ticket": 3,
    "Haku Ticket": 4,
    "Might Guy Ticket": 5,
    "Zabuza Ticket": 6,
    "Crow Ticket": 7,
    "Nine-Tailed Naruto Ticket": 8,
    "Kakashi with Sharingan Ticket": 9,
    "Akamaru Ticket": 10,
    "Sasuke with Sharingan Ticket": 11,
    "Orochimaru Ticket": 12,
    "Mizuki Ticket": 13,
    "Seal Ticket": 14,
    "HP Ticket": 15,
    "1000 Coins": 16
}
ID_TO_ITEM_NAME = dict(zip(ITEM_NAME_TO_ID.values(), ITEM_NAME_TO_ID.keys()))


DEFAULT_ITEM_CLASSIFICATIONS = {
x: ItemClassification.progression if "Ticket" in x else ItemClassification.filler for x in list(ITEM_NAME_TO_ID.keys())
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
