from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import HelloKittyWorld

ITEM_NAME_TO_ID = {
    "Progressive Stage Unlock": 1,
    "Haiiii Kitttyyyyy :3": 5,
    "Mama, I have decided to protect our town from the Block Battalion.": 6,
    "Seesaw is watching you.": 7,
    "The Feeling of Being Lost": 8,
    "I will defeat it. Over.": 9,
    "Roger that. Over.": 10,
    "Hydration Check": 11,
    "Hewwo Kittyyy :3": 12
}
ID_TO_ITEM_NAME = dict(zip(ITEM_NAME_TO_ID.values(), ITEM_NAME_TO_ID.keys()))


DEFAULT_ITEM_CLASSIFICATIONS = {
x: ItemClassification.progression if "Progressive Stage Unlock" in x else ItemClassification.filler for x in list(ITEM_NAME_TO_ID.keys())
}


class HelloKittyItem(Item):
    game = "Hello Kitty: Roller Rescue"


def get_random_filler_item_name(world: HelloKittyWorld) -> str:
    fillers = list(ITEM_NAME_TO_ID.keys())
    return fillers[1:][world.random.randint(0,len(fillers)-2)]


def create_item_with_correct_classification(world: HelloKittyWorld, name: str) -> HelloKittyItem:
    return HelloKittyItem(name, DEFAULT_ITEM_CLASSIFICATIONS[name], ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: HelloKittyWorld) -> None:
    itempool = []
    for i in range(15):
        itempool += [world.create_item("Progressive Stage Unlock")]
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
    needed_number_of_filler_items = number_of_unfilled_locations - len(itempool)
   
    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]
    world.multiworld.itempool += itempool
