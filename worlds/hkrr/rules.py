from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import HelloKittyWorld


def set_all_rules(world: HelloKittyWorld) -> None:
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_location_rules(world: HelloKittyWorld) -> None:
    set_rule(world.get_location("Save the World"), lambda state: state.has("Progressive Stage Unlock", world.player, 15))

def set_completion_condition(world: HelloKittyWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)