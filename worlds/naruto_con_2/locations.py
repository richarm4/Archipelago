from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items

if TYPE_CHECKING:
    from .world import NarutoWorld

LOCATION_NAME_TO_ID = {
    "Iruka Umino": 1,
    "Neji Hyuga": 2,
    "Kankuro": 3,
    "Haku": 4,
    "Might Guy": 5,
    "Zabuza": 6,
    "Crow": 7,
    "Nine-Tailed Naruto": 8,
    "Kakashi with Sharingan": 9,
    "Akamaru": 10,
    "Orochimaru": 11,
    "Mizuki": 12,
    "Attack PWR UP (Sm)": 13,
    "Attack PWR UP (L)": 14,
    "Projectile UP": 15,
    "Chakra MAX": 16,
    "Secret Attack UP": 17,
    "Absorb HP": 18,
    "ATTK Property UP": 19,
    "Seal Endure": 20,
    "Substitution Jutsu Seal": 21,
    "Seal Evade": 22,
    "Seal Taijutsu": 23,
    "Seal Ninjutsu": 24,
    "Seal Secret": 25,
    "Seal Throw Techs": 26,
    "Seal Throw Escape": 27,
    "Seal Chakra": 28,
    "Seal Jump": 29,
    "Seal Guard": 30,
    "Seal Projectiles": 31,
    "HP Decrease": 32,
    "Attack PWR 50% DOWN": 33,
    "Seal Gauge": 34,
    "HP Increase (Sm)": 35,
    "HP Increase (M)": 36,
    "HP Increase (L)": 37,
    "Auto Throw Escape": 38,
    "Auto Endure": 39,
    "Body Activation": 40,
    "Auto Recovery": 41,
    "Invincible (ltd.)": 42,
    "Absolute Guard": 43,
    "Food Pills": 44,
    
}

LOCATION_ADDRESS_BITS = {
    "Iruka Umino": (0x801AD2CF, 0),
    "Neji Hyuga": (0x801AD2CF, 1),
    "Kankuro": (0x801AD2CF, 2),
    "Haku": (0x801AD2CF, 3),
    "Might Guy": (0x801AD2CF, 4),
    "Zabuza": (0x801AD2CF, 5),
    "Crow": (0x801AD2CF, 6),
    "Nine-Tailed Naruto": (0x801AD2CF, 7),
    "Kakashi with Sharingan": (0x801AD2CE, 0),
    "Akamaru": (0x801AD2CE, 1),
    "Orochimaru": (0x801AD2CE, 3),
    "Mizuki": (0x801AD2CE, 4),
    "Attack PWR UP (Sm)": (0x801AD2DF, 0),
    "Attack PWR UP (L)": (0x801AD2DF, 1),
    "Projectile UP": (0x801AD2DF, 2),
    "Chakra MAX": (0x801AD2DF, 3),
    "Secret Attack UP": (0x801AD2DF, 4),
    "Absorb HP": (0x801AD2DF, 5),
    "ATTK Property UP": (0x801AD2DF, 6),
    "Seal Endure": (0x801AD2DD, 1),
    "Substitution Jutsu Seal": (0x801AD2DD, 2),
    "Seal Evade": (0x801AD2DD, 3),
    "Seal Taijutsu": (0x801AD2DD, 4),
    "Seal Ninjutsu": (0x801AD2DD, 5),
    "Seal Secret": (0x801AD2DD, 6),
    "Seal Throw Techs": (0x801AD2DD, 7),
    "Seal Throw Escape": (0x801AD2DC, 0),
    "Seal Chakra": (0x801AD2DC, 1),
    "Seal Jump": (0x801AD2DC, 2),
    "Seal Guard": (0x801AD2DC, 3),
    "Seal Projectiles": (0x801AD2DC, 4),
    "HP Decrease": (0x801AD2DC, 5),
    "Attack PWR 50% DOWN": (0x801AD2DC, 6),
    "Seal Gauge": (0x801AD2DC, 7),
    "HP Increase (Sm)": (0x801AD2DF, 7),
    "HP Increase (M)": (0x801AD2DE, 0),
    "HP Increase (L)": (0x801AD2DE, 1),
    "Auto Throw Escape": (0x801AD2DE, 2),
    "Auto Endure": (0x801AD2DE, 3),
    "Body Activation": (0x801AD2DE, 4),
    "Auto Recovery": (0x801AD2DE, 5),
    "Invincible (ltd.)": (0x801AD2DE, 6),
    "Absolute Guard": (0x801AD2DE, 7),
    "Food Pills": (0x801AD2DD, 0)
}

TICKET_ADDRESSES = {
    "Iruka Umino Ticket": 0x80192FD8,
    "Neji Hyuga Ticket": 0x80192FE8,
    "Kankuro Ticket": 0x80192FF0,
    "Haku Ticket": 0x80192FF8,
    "Might Guy Ticket": 0x80193008,
    "Zabuza Ticket": 0x80193000,
    "Crow Ticket": 0x80193010,
    "Nine-Tailed Naruto Ticket": 0x80193020,
    "Kakashi with Sharingan Ticket": 0x80193028,
    "Akamaru Ticket": 0x80193018,
    "Sasuke with Sharingan Ticket": 0x80193030,
    "Orochimaru Ticket": 0x80193038,
    "Mizuki Ticket": 0x80193040,
    "Seal Ticket": 0x80193280,
    "HP Ticket": 0x80193230
}

UNTICKETED = {
    "Attack PWR UP (Sm)": 0x801931F8,
    "Attack PWR UP (L)": 0x80193200,
    "Projectile UP": 0x80193208,
    "Chakra MAX": 0x80193210,
    "Secret Attack UP": 0x80193218,
    "Absorb HP": 0x80193220,
    "ATTK Property UP": 0x80193228,
    "Substitution Jutsu Seal": 0x80193288,
    "Seal Evade": 0x80193290,
    "Seal Taijutsu": 0x80193298,
    "Seal Ninjutsu": 0x801932A0,
    "Seal Secret": 0x801932A8,
    "Seal Throw Techs": 0x801932B0,
    "Seal Throw Escape": 0x801932B8,
    "Seal Chakra": 0x801932C0,
    "Seal Jump": 0x801932C8,
    "Seal Guard": 0x801932D0,
    "Seal Projectiles": 0x801932D8,
    "HP Decrease": 0x801932E0,
    "Attack PWR 50% DOWN": 0x801932E8,
    "Seal Gauge": 0x801932F0,
    "HP Increase (M)": 0x80193238,
    "HP Increase (L)": 0x80193240,
    "Auto Throw Escape": 0x80193248,
    "Auto Endure": 0x80193250,
    "Body Activation": 0x80193258,
    "Auto Recovery": 0x80193260,
    "Invincible (ltd.)": 0x80193268,
    "Absolute Guard": 0x80193270,
    "Food Pills": 0x80193278
}

class NarutoLocation(Location):
    game = "Naruto"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: NarutoWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: NarutoWorld) -> None:
    level1 = world.get_region("Menu")
    level2 = world.get_region("Post-Seal Ticket")
    level3 = world.get_region("Post-HP Ticket")

    level1_locations = get_location_names_with_ids([list(LOCATION_NAME_TO_ID.keys())[list(LOCATION_NAME_TO_ID.values()).index(x)] for x in range(1,20)])
    level1.add_locations(level1_locations, NarutoLocation)
    
    level2_locations = get_location_names_with_ids([list(LOCATION_NAME_TO_ID.keys())[list(LOCATION_NAME_TO_ID.values()).index(x)] for x in range(20,32)])
    level2.add_locations(level2_locations, NarutoLocation)
    
    level3_locations = get_location_names_with_ids([list(LOCATION_NAME_TO_ID.keys())[list(LOCATION_NAME_TO_ID.values()).index(x)] for x in range(32,45)])
    level3.add_locations(level3_locations, NarutoLocation)

def create_events(world: NarutoWorld) -> None:
    menu = world.get_region("Menu")
    menu.add_event(
        "Purchase Sasuke with Sharingan", "Victory", location_type=NarutoLocation, item_type=items.NarutoItem
    )