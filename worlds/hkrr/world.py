from collections.abc import Mapping
from typing import Any


from worlds.AutoWorld import World


from . import items, locations, options, regions, rules, web_world


class HelloKittyWorld(World):
    """
    Hello Kitty: Roller Rescue is an action game in which Hello Kitty is
    slaying a battalion of aliens that have invaded her world.
    """
    game = "Hello Kitty: Roller Rescue"


    web = web_world.HelloKittyWebWorld()


    options_dataclass = options.HelloKittyOptions
    options: options.HelloKittyOptions


    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "New Hope"
    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)


    def set_rules(self) -> None:
        rules.set_all_rules(self)


    def create_items(self) -> None:
        items.create_all_items(self)


    def create_item(self, name: str) -> items.HelloKittyItem:
        return items.create_item_with_correct_classification(self, name)


    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)


    def fill_slot_data(self) -> Mapping[str, Any]:
        return {
            "options": self.options.as_dict("coinsanity", "last_breath", toggles_as_bools=True),
            }

    def generate_early(self) -> None:
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]

            slot_options: dict[str, Any] = slot_data.get("options", {})
            # Set all your options here instead of getting them from the yaml
            for key, value in slot_options.items():
                opt: Optional[Option] = getattr(self.options, key, None)
                if opt is not None:
                    # You can also set .value directly but that won't work if you have OptionSets
                    setattr(self.options, key, opt.from_any(value))
    
    ut_can_gen_without_yaml = True
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # Trigger a regen in UT
        return slot_data