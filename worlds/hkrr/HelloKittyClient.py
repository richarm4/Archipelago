import asyncio
import sys
import traceback
import time
from typing import ClassVar

import dolphin_memory_engine as dme
import Utils
from CommonClient import (
    ClientCommandProcessor,
    ClientStatus,
    CommonContext,
    get_base_parser,
    gui_enabled,
    logger,
    server_loop,
)
from MultiServer import mark_raw

from .bit_helper import (
    extract_bitflag_list,
    extract_bits_value,
    get_bit_address,
    read_value_bytes,
    set_flag_bit,
    set_on_or_bytes,
    set_value_bytes,
    swap_endian,
)

from .items import (
    ITEM_NAME_TO_ID,
    ID_TO_ITEM_NAME
)
from .locations import (
    LOCATION_NAME_TO_ID,
    CURRENT_STAGE,
    COIN_LEVEL_BYTES,
    boss_hp
)
tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext


CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a Hello Kitty: Roller Rescue ROM. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Dolphin connection was lost. Please restart your emulator and make sure Hello Kitty: Roller Rescue is running."
)
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."


class HelloKittyCommandProcessor(ClientCommandProcessor):
    """
    Command Processor for Hello Kitty: Roller Rescue client commands.

    This class handles commands specific to Hello Kitty: Roller Rescue.
    """

    def __init__(self, ctx: "HelloKittyContext"):
        """
        Initialize the command processor with the provided context.

        :param ctx: Context for the client.
        """
        self.ctx = ctx


class HelloKittyContext(SuperContext):
    """
    The context for Hello Kitty Roller Rescue's client.

    This class manages all interactions with the Dolphin emulator and the Archipelago server for Hello Kitty: Roller Rescue.
    """

    command_processor = HelloKittyCommandProcessor
    game = "Hello Kitty: Roller Rescue"
    items_handling = 0b111
    received_items_id: ClassVar[list[int]] = []
    slot_data = {}
    expected_idx = 0
    victory = False

    def __init__(self, server_address, password):
        """
        Initialize the Hello Kitty: Roller Rescue context.

        :param server_address: Address of the Archipelago server
        :param password: Password for server authentication
        """
        super().__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        self.dolphin_sync_task: asyncio.Task[None] | None = None
        self.dolphin_status: str = CONNECTION_INITIAL_STATUS
        self.awaiting_rom: bool = False
        self.tags = {"AP"}
        self.sync_task: asyncio.Task[None] | None = None
        self.stages = 0
        self.currstage = 0
        self.currstagecoins = False
        self.timer = 0
        self.loading = False
        self.one_hp = False
        self.coinsanity = False
        self.bossalive = False

    async def server_auth(self, password_requested: bool = False):
        """
        Authenticate with the Archipelago server.

        :param password_requested: Indicates if the server has requested a password
        """
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def make_gui(self):
        """
        Create the GUI for the Hello Kitty: Roller Rescue client.

        :return: The GUI instance
        """
        ui = super().make_gui()
        ui.base_title = "Hello Kitty: Roller Rescue Client"
        return ui

    def on_package(self, cmd: str, args: dict):
        """Handle incoming packages from the server."""
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            self.coinsanity = self.slot_data["options"]["coinsanity"]
            self.one_hp = self.slot_data["options"]["last_breath"]
        return super().on_package(cmd, args)


async def locations_watcher(ctx):
    """
    Watch for location checks in the game and notify the server.

    :param ctx: The Hello Kitty: Roller Rescue context
    """

    def _check_location_flag(ctx: HelloKittyContext, location) -> bool:
        """
        Check if a location has been checked based on its flag.

        :param ctx: The Hello Kitty: Roller Rescue context
        :param location: The location name to check
        """
        
        if LOCATION_NAME_TO_ID[location] not in ctx.server_locations or LOCATION_NAME_TO_ID[location] in ctx.locations_checked or ctx.currstagecoins == False:
            return False
        if location == "The Final Countdown CLEAR":
            if dme.read_byte(CURRENT_STAGE) == 16 and read_value_bytes(0x80DE3FF0, 0, 16, 2, "big") == 17255:
                ctx.locations_checked.add(LOCATION_NAME_TO_ID[location])
                return True
        level = LOCATION_NAME_TO_ID[location]
        clear_byte = dme.read_byte(0x804A2870)
        level_byte = dme.read_byte(CURRENT_STAGE)
        if clear_byte == 255 and level_byte == level:
            ctx.locations_checked.add(LOCATION_NAME_TO_ID[location])
            return True
        return False

    def _check_coin_flag(ctx: HelloKittyContext, location) -> bool:
        if ctx.currstage != dme.read_byte(CURRENT_STAGE):
            ctx.currstage = dme.read_byte(CURRENT_STAGE)
            ctx.bossalive = False
            ctx.currstagecoins = False
        
        if LOCATION_NAME_TO_ID[location] not in ctx.server_locations or LOCATION_NAME_TO_ID[location] in ctx.locations_checked:
            return False

        address, level, amount = COIN_LEVEL_BYTES[location][0], COIN_LEVEL_BYTES[location][1], COIN_LEVEL_BYTES[location][2]
        if ctx.currstage != level: return False
                    
        if level in [12,15]: return False #after checking the stage is loaded we can ignore 12/15 as they have no coins
        coin_byte = read_value_bytes(address, 0, 16, 2, "big")
        # 316 is the max amount of coins because of Freeze Factor being loaded
        # ignore for 255-257 in particular(00FF, 0100, 0101) as these edge cases can cause checks sending too early and there's never just that many coins
        if coin_byte < 12:
            ctx.currstagecoins = True
        if coin_byte >= amount and ctx.currstagecoins == True and coin_byte < 317 and coin_byte not in [255,256,257]:
            ctx.locations_checked.add(LOCATION_NAME_TO_ID[location])
            return True
        return False
    for location_data in COIN_LEVEL_BYTES:
            _check_coin_flag(ctx, location_data)
    for location_data in LOCATION_NAME_TO_ID:
            _check_location_flag(ctx, location_data)

    
    locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
    if locations_checked:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])
    if read_value_bytes(0x80DE3FF0, 0, 16, 2, "big") == 17255 and dme.read_byte(CURRENT_STAGE) == 16 and not ctx.finished_game:
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        ctx.finished_game = True

async def give_items(ctx: HelloKittyContext):
    """
    Give items to the player in the game.

    :param ctx: The Hello Kitty: Roller Rescue context
    """
    expected_idx = ctx.expected_idx
    set_value_bytes(0x806D4283, 0, ctx.stages, 8, 1, "big")
    if ctx.one_hp:
        set_value_bytes(0x806D428F, 0, 1, 8, 1, "big")
    # Check if there are new items.
    received_items = ctx.items_received
    if len(received_items) <= expected_idx:
        # There are no new items.
        return

    # Loop through items to give.
    # Give the player all items at an index greater than or equal to the expected index.
    for idx, item in enumerate(received_items[expected_idx:], expected_idx):
        # Attempt to give the item and increment the expected index.
        logger.debug(f"Received item: {item}")
        ctx.received_items_id.append(item.item)
        while not _give_item_in_game(ctx, item):
            await asyncio.sleep(0.01)
        ctx.expected_idx = idx + 1


def _give_item_in_game(ctx: HelloKittyContext, item) -> bool:
    """
    Give an item to the player in the game.

    :param ctx: The Hello Kitty: Roller Rescue context
    :param item: The item data to give
    :return: True if the item was given successfully, False otherwise
    """
    itemname = ID_TO_ITEM_NAME[item.item]
    if "Progressive" in itemname and ctx.stages != 15:
        ctx.stages += 1
    return True



async def game_watcher(ctx: HelloKittyContext):
    """
    Main game watcher loop.

    :param ctx: The Hello Kitty: Roller Rescue context
    """
    while not ctx.exit_event.is_set():
        try:
            if not dme.is_hooked() or ctx.slot is None:
                await asyncio.sleep(1)
                continue
            await locations_watcher(ctx)
            await give_items(ctx)

            if ctx.victory and not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

            await asyncio.sleep(0.1)
        except Exception:
            logger.debug(traceback.format_exc())
            dme.un_hook()
            ctx.dolphin_status = CONNECTION_LOST_STATUS


async def dolphin_sync_task(ctx: HelloKittyContext) -> None:
    """
    Task to manage the connection and synchronization with the Dolphin emulator.

    :param ctx: The Hello Kitty: Roller Rescue context
    """
    logger.info("Starting Dolphin connector.")
    sleep_time = 0.0
    while not ctx.exit_event.is_set():
        if sleep_time > 0.0:
            try:
                # ctx.watcher_event gets set when receiving ReceivedItems or LocationInfo, or when shutting down.
                await asyncio.wait_for(ctx.watcher_event.wait(), sleep_time)
            except TimeoutError:
                pass
            sleep_time = 0.0
        ctx.watcher_event.clear()

        try:
            if dme.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if ctx.awaiting_rom:
                    logger.info("Connected to Dolphin")
                    await ctx.server_auth()
                sleep_time = 0.1
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin...")
                dme.hook()
                if dme.is_hooked():
                    if dme.read_bytes(0x80000000, 6) != b"GH6EAF":
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dme.un_hook()
                        await asyncio.sleep(5)
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        ctx.locations_checked = set()
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    dme_status = dme.get_status()
                    logger.info(dme_status)
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await asyncio.sleep(5)
                    continue
        except Exception:
            dme.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await asyncio.sleep(5)
            continue


def main(*launch_args: str):
    """
    Main entry point for the Hello Kitty: Roller Rescue client.

    :param launch_args: Command-line arguments for the client
    """
    parser = get_base_parser()
    args = parser.parse_args(launch_args)

    async def _main(connect, password):
        """
        Main asynchronous function for the Hello Kitty: Roller Rescue client.

        :param connect: The server address to connect to
        :param password: The password for server authentication
        """
        ctx = HelloKittyContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

        if tracker_loaded:
            ctx.run_generator()
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="SmsDolphinSync")
        progression_watcher = asyncio.create_task(game_watcher(ctx), name="SmsProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await ctx.dolphin_sync_task

        if progression_watcher:
            await progression_watcher

    asyncio.run(_main(args.connect, args.password))


if __name__ == "__main__":
    Utils.init_logging("HelloKittyClient", exception_logger="Client")
    main(*sys.argv[1:])
