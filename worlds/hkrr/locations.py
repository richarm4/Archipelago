from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import HelloKittyWorld
levels = ["New Hope",
            "Food Fear",
            "Tank Attack", 
            "The Sleepy Pony", 
            "Messy Park", 
            "Protect the Station", 
            "Shopping Scam", 
            "Freeze Factor", 
            "Red Alert", 
            "The Haunted Lot", 
            "Arena of Danger", 
            "Project Home Run",
            "Under Construction",
            "Last Breath of Reliance",
            "Control Deck",
            "The Final Countdown"]
#coin grabbed amount, check total
level_coins = [(0x813B0047, 20), (0x80DD3627, 20),
               (0x80CA2387, 10), (0x8120F2E7, 10), 
               (0x80D5B807, 10), (0x80CCE527, 10),
               (0x80D2E227, 10), (0x811FD547, 10), 
               (0x80C4BF67, 10), (0x81267107, 10), 
               (0x8118B487, 10), (0x69, 10), 
               (0x8120C8C7, 10), (0x811B3C67, 20), 
               (0x69, 10), (0x80DB4827, 10)]
    
LOCATION_NAME_TO_ID = {
            "New Hope CLEAR": 1,
            "Food Fear CLEAR": 2,
            "Tank Attack CLEAR": 3, 
            "The Sleepy Pony CLEAR": 4, 
            "Messy Park CLEAR": 5, 
            "Protect the Station CLEAR": 6, 
            "Shopping Scam CLEAR": 7, 
            "Freeze Factor CLEAR": 8, 
            "Red Alert CLEAR": 9, 
            "The Haunted Lot CLEAR": 10, 
            "Arena of Danger CLEAR": 11, 
            "Project Home Run CLEAR": 12,
            "Under Construction CLEAR": 13,
            "Last Breath of Reliance CLEAR": 14,
            "Control Deck CLEAR": 15,
            "The Final Countdown CLEAR": 16}
for i in range(16):
    if levels[i] not in ["Project Home Run", "Control Deck"]:
        LOCATION_NAME_TO_ID = LOCATION_NAME_TO_ID | {f"{levels[i]} {x+1} Coin" if x==0 else f"{levels[i]} {x+1} Coins": (i+1)*1000 + x+1 for x in range(level_coins[i][1])}


LEVEL_CLEAR_BYTES = {
    "New Hope CLEAR": (0x808D2DAC, 1),
    "Food Fear CLEAR": (0x808E7FEE, 2),
    "Tank Attack CLEAR": (0x80D9D3B4, 3),
    "The Sleepy Pony CLEAR": (0x8143F86E, 4),
    "Messy Park CLEAR": (0x808D59FF, 5),
    "Protect the Station CLEAR": (0x8134B86B, 6), 
    "Shopping Scam CLEAR": (0x808D1584, 7), 
    "Freeze Factor CLEAR": (0x808DEA3F, 8),
    "Red Alert CLEAR": (0x808A535F, 9),
    "The Haunted Lot CLEAR": (0x808EF3FE, 10),
    "Arena of Danger CLEAR": (0x804A2870, 11),
    "Project Home Run CLEAR": (0x80C91323,12),
    "Under Construction CLEAR": (0x8153AA90, 13),
    "Last Breath of Reliance CLEAR": (0x808DECFE, 14),
    "Control Deck CLEAR": (0x802B0FF0, 15),
    "The Final Countdown CLEAR": (0x802BC136, 16)
}
#(grabbed_count, stage, amount
COIN_LEVEL_BYTES = {}
for i in range(16):
    if levels[i] not in ["Project Home Run", "Control Deck"]:
        COIN_LEVEL_BYTES = COIN_LEVEL_BYTES | {f"{levels[i]} {x+1} Coin" if x==0 else f"{levels[i]} {x+1} Coins": (level_coins[i][0], i+1, x+1) for x in range(level_coins[i][1])}


CURRENT_STAGE = 0x806D4267

class HelloKittyLocation(Location):
    game = "Hello Kitty: Roller Rescue"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: HelloKittyWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: HelloKittyWorld) -> None:
    for i in range(16):
        level = world.get_region(levels[i])
        level_locations = get_location_names_with_ids([f"{levels[i]} CLEAR"])
        if levels[i] not in ["Project Home Run", "Control Deck"]:
            level_locations = level_locations | get_location_names_with_ids([f"{levels[i]} {x+1} Coin" if x==0 else f"{levels[i]} {x+1} Coins" for x in range(level_coins[i][1])])  
        level.add_locations(level_locations, HelloKittyLocation)



def create_events(world: HelloKittyWorld) -> None:
    menu = world.get_region("Menu")
    menu.add_event(
        "Save the World", "Victory", location_type=HelloKittyLocation, item_type=items.HelloKittyItem
    )