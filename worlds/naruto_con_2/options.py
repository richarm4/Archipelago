from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md

class Price(Range):
    """
    The price of an item not currently locked behind a Ticket, ranging from 0 to 10000.
    """

    display_name = "Regular Price"

    range_start = 0
    range_end = 10000
    default = 1234


# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class NarutoOptions(PerGameCommonOptions):
    price: Price