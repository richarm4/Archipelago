from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import HelloKittyWorld
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

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

    regions = [Region(x, world.player, world.multiworld) for x in levels]
    world.multiworld.regions += regions

def connect_regions(world: HelloKittyWorld) -> None:
    regions = [world.get_region(levels[i]) for i in range(16)]
    for x in range(15):
        world.create_entrance(regions[x], regions[x+1], Has("Progressive Stage Unlock", x+1))