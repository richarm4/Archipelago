from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import NarutoWorld


def set_all_rules(world: NarutoWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_location_rules(world: NarutoWorld) -> None:
    iruka = world.get_location("Iruka Umino")
    neji = world.get_location("Neji Hyuga")
    set_rule(iruka, lambda state: state.has("Iruka Umino Ticket", world.player))
    set_rule(neji, lambda state: state.has("Neji Hyuga Ticket", world.player))
    kankuro = world.get_location("Kankuro")
    set_rule(kankuro, lambda state: state.has("Kankuro Ticket", world.player) and state.can_reach_location("Neji Hyuga", world.player))
    haku = world.get_location("Haku")
    zabuza = world.get_location("Zabuza")
    set_rule(haku, lambda state: state.has("Haku Ticket", world.player) and state.can_reach_location("Iruka Umino", world.player)) 
    set_rule(zabuza, lambda state: state.has("Zabuza Ticket", world.player) and state.can_reach_location("Iruka Umino", world.player)) 
    guy = world.get_location("Might Guy")   
    set_rule(guy, lambda state: state.has("Might Guy Ticket", world.player) and state.can_reach_location("Kankuro", world.player))
    akamaru = world.get_location("Akamaru")
    crow = world.get_location("Crow")
    set_rule(akamaru, lambda state: state.has("Akamaru Ticket", world.player) and state.can_reach_location("Might Guy", world.player))
    set_rule(crow, lambda state: state.has("Crow Ticket", world.player) and state.can_reach_location("Might Guy", world.player))
    ntn = world.get_location("Nine-Tailed Naruto")
    set_rule(ntn, lambda state: state.has("Nine-Tailed Naruto Ticket", world.player) and state.can_reach_location("Akamaru", world.player) and state.can_reach_location("Crow", world.player))
    kws = world.get_location("Kakashi with Sharingan")
    set_rule(kws, lambda state: state.has("Kakashi with Sharingan Ticket", world.player) and state.can_reach_location("Nine-Tailed Naruto", world.player))
    mizuki = world.get_location("Mizuki")
    set_rule(mizuki, lambda state: state.has("Mizuki Ticket", world.player) and state.can_reach_location("Iruka Umino", world.player) and state.can_reach_location("Kakashi with Sharingan", world.player))
    orochimaru = world.get_location("Orochimaru")
    set_rule(orochimaru, lambda state: state.has("Orochimaru Ticket", world.player) and state.can_reach_location("Mizuki", world.player) and state.can_reach_location("Zabuza", world.player) and state.can_reach_location("Haku", world.player))
    goal = world.get_location("Purchase Sasuke with Sharingan")
    set_rule(goal, lambda state: state.has("Sasuke with Sharingan Ticket", world.player) and state.can_reach_location("Orochimaru", world.player))
    return


def set_completion_condition(world: NarutoWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)