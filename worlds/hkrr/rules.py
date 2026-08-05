from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

if TYPE_CHECKING:
    from .world import HelloKittyWorld


def set_all_rules(world: HelloKittyWorld) -> None:
    set_all_location_rules(world)
    set_completion_condition(world)

def set_all_location_rules(world: HelloKittyWorld) -> None:
    world.set_rule(world.get_location("Save the World"), Has("Progressive Stage Unlock", 15))

def set_completion_condition(world: HelloKittyWorld) -> None:
    world.set_completion_rule(Has("Victory"))