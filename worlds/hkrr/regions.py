from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import HelloKittyWorld


def create_and_connect_regions(world: HelloKittyWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

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

def create_all_regions(world: HelloKittyWorld) -> None:

    regions = [Region(x, world.player, world.multiworld) for x in levels] + [Region("Menu", world.player, world.multiworld)]
    world.multiworld.regions += regions

# I tried writing this as a simple loop and it didn't work so I unrolled it >:(
def connect_regions(world: HelloKittyWorld) -> None:
    menu = world.get_region("Menu")
    menu.connect(world.get_region(levels[0]), f"Menu to {levels[0]}")
    newhope = world.get_region("New Hope")
    newhope.connect(world.get_region(levels[1]), f"New Hope to {levels[1]}", lambda state: state.has("Progressive Stage Unlock", world.player, 1))
    foodfear = world.get_region(levels[1])
    foodfear.connect(world.get_region(levels[2]), f"{levels[1]} to {levels[2]}", lambda state: state.has("Progressive Stage Unlock", world.player, 2))
    tankattack = world.get_region(levels[2])
    tankattack.connect(world.get_region(levels[3]), f"{levels[2]} to {levels[3]}", lambda state: state.has("Progressive Stage Unlock", world.player, 3))
    sleepypony = world.get_region(levels[3])
    sleepypony.connect(world.get_region(levels[4]), f"{levels[3]} to {levels[4]}", lambda state: state.has("Progressive Stage Unlock", world.player, 4))
    messypark = world.get_region(levels[4])
    messypark.connect(world.get_region(levels[5]), f"{levels[4]} to {levels[5]}", lambda state: state.has("Progressive Stage Unlock", world.player, 5))
    station = world.get_region(levels[5])
    station.connect(world.get_region(levels[6]), f"{levels[5]} to {levels[6]}", lambda state: state.has("Progressive Stage Unlock", world.player, 6))
    scam = world.get_region(levels[6])
    scam.connect(world.get_region(levels[7]), f"{levels[6]} to {levels[7]}", lambda state: state.has("Progressive Stage Unlock", world.player, 7))
    freezefactor = world.get_region(levels[7])
    freezefactor.connect(world.get_region(levels[8]), f"{levels[7]} to {levels[8]}", lambda state: state.has("Progressive Stage Unlock", world.player, 8))
    redalert = world.get_region(levels[8])
    redalert.connect(world.get_region(levels[9]), f"{levels[8]} to {levels[9]}", lambda state: state.has("Progressive Stage Unlock", world.player, 9))
    hauntedlot = world.get_region(levels[9])
    hauntedlot.connect(world.get_region(levels[10]), f"{levels[9]} to {levels[10]}", lambda state: state.has("Progressive Stage Unlock", world.player, 10))
    dangerarena = world.get_region(levels[10])
    dangerarena.connect(world.get_region(levels[11]), f"{levels[10]} to {levels[11]}", lambda state: state.has("Progressive Stage Unlock", world.player, 11))
    projecthr = world.get_region(levels[11])
    projecthr.connect(world.get_region(levels[12]), f"{levels[11]} to {levels[12]}", lambda state: state.has("Progressive Stage Unlock", world.player, 12))
    uc = world.get_region(levels[12])
    uc.connect(world.get_region(levels[13]), f"{levels[12]} to {levels[13]}", lambda state: state.has("Progressive Stage Unlock", world.player, 13))
    lbr = world.get_region(levels[13])
    lbr.connect(world.get_region(levels[14]), f"{levels[13]} to {levels[14]}", lambda state: state.has("Progressive Stage Unlock", world.player, 14))
    controldeck = world.get_region(levels[14])
    controldeck.connect(world.get_region(levels[15]), f"{levels[14]} to {levels[15]}", lambda state: state.has("Progressive Stage Unlock", world.player, 15))