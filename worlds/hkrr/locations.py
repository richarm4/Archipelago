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
level_coins = [(0x813B0046, 20), (0x80DD3626, 20),
               (0x80CA2386, 10), (0x8120F2E6, 10), 
               (0x80D5B806, 10), (0x80CCE526, 10),
               (0x80D2E226, 10), (0x811FD546, 10), 
               (0x80C4BF66, 10), (0x81267106, 10), 
               (0x8118B486, 10), (0x69, 10), 
               (0x8120C8C6, 10), (0x811B3C66, 20), 
               (0x69, 10), (0x80DB4826, 10)]

level_coinsanity = [(0x813B0046, 69), (0x80DD3626, 42),
               (0x80CA2386, 41), (0x8120F2E6, 79), 
               (0x80D5B806, 169), (0x80CCE526, 130),
               (0x80D2E226, 122), (0x811FD546, 316), 
               (0x80C4BF66, 69), (0x81267106, 101), 
               (0x8118B486, 269), (0x69, 10), 
               (0x8120C8C6, 35), (0x811B3C66, 211), 
               (0x69, 10), (0x80DB4826, 124)]

boss_hp = [0,0,0,0x80F48BBF,0,0,0x812CA977,0,0,0x80E5585F,0,0,0x80C91323,0,0,0x813148C3,0]

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
        LOCATION_NAME_TO_ID = LOCATION_NAME_TO_ID | {f"{levels[i]} {x+1} Coin" if x==0 else f"{levels[i]} {x+1} Coins": (i+1)*1000 + x+1 for x in range(level_coinsanity[i][1])}

#(grabbed_count, stage, amount)
COIN_LEVEL_BYTES = {}
for i in range(16):
    if levels[i] in ["Project Home Run", "Control Deck"]:
        COIN_LEVEL_BYTES = COIN_LEVEL_BYTES | {f"{levels[i]} CLEAR": (0x69, i+1, 69696969)}
    else: COIN_LEVEL_BYTES = COIN_LEVEL_BYTES | {f"{levels[i]} {x+1} Coin" if x==0 else f"{levels[i]} {x+1} Coins": (level_coinsanity[i][0], i+1, x+1) for x in range(level_coinsanity[i][1])}


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
        coin_counts = level_coinsanity if world.options.coinsanity else level_coins
        if levels[i] not in ["Project Home Run", "Control Deck"]:
            level_locations = level_locations | get_location_names_with_ids([f"{levels[i]} {x+1} Coin" if x==0 else f"{levels[i]} {x+1} Coins" for x in range(coin_counts[i][1])])  
        level.add_locations(level_locations, HelloKittyLocation)



def create_events(world: HelloKittyWorld) -> None:
    tfc = world.get_region("The Final Countdown")
    tfc.add_event(
        "Save the World", "Victory", location_type=HelloKittyLocation, item_type=items.HelloKittyItem
    )