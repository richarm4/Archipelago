from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md

class Coinsanity(Toggle):
    """
    Make each new amount of coins on each stage a check. There's 1777 of them.
    """

    display_name = "Coinsanity"

class Lastbreath(Toggle):
    """
    Forces you to enter each stage with 1 HP. Not for the faint of heart.
    """

    display_name = "Last Breath"

# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class HelloKittyOptions(PerGameCommonOptions):
    coinsanity: Coinsanity
    last_breath: Lastbreath