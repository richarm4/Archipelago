import asyncio
import sys
import traceback
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
    LOCATION_ADDRESS_BITS,
    LOCATION_NAME_TO_ID,
    TICKET_ADDRESSES,
    UNTICKETED
)



CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a Clash of Ninja 2 ROM. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Dolphin connection was lost. Please restart your emulator and make sure Naruto Clash of Ninja 2 is running."
)
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."


class NarutoCommandProcessor(ClientCommandProcessor):
    """
    Command Processor for Naruto Clash of Ninja 2 client commands.

    This class handles commands specific to Naruto Clash of Ninja 2.
    """

    def __init__(self, ctx: "NarutoContext"):
        """
        Initialize the command processor with the provided context.

        :param ctx: Context for the client.
        """
        self.ctx = ctx


class NarutoContext(CommonContext):
    """
    The context for Naruto Clash of Ninja 2's client.

    This class manages all interactions with the Dolphin emulator and the Archipelago server for Naruto Clash of Ninja 2.
    """

    command_processor = NarutoCommandProcessor
    game = "Naruto Clash of Ninja 2"
    items_handling = 0b111
    received_items_id: ClassVar[list[int]] = []
    slot_data = {}
    regular_price = 5959
    expected_idx = 0
    shopinit = False
    victory = False

    def __init__(self, server_address, password):
        """
        Initialize the Naruto Clash of Ninja 2 context.

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
        Create the GUI for the Naruto Clash of Ninja 2 client.

        :return: The GUI instance
        """
        ui = super().make_gui()
        ui.base_title = "Naruto Clash of Ninja 2 Client"
        return ui

    def on_package(self, cmd: str, args: dict):
        """Handle incoming packages from the server."""
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            self.regular_price = self.slot_data["price"]
        return super().on_package(cmd, args)



async def locations_watcher(ctx):
    """
    Watch for location checks in the game and notify the server.

    :param ctx: The Naruto Clash of Ninja 2 context
    """

    def _check_location_flag(ctx: NarutoContext, location) -> bool:
        """
        Check if a location has been checked based on its flag.

        :param ctx: The Naruto Clash of Ninja 2 context
        :param location: The location name to check
        """

        if LOCATION_NAME_TO_ID[location] not in ctx.server_locations or LOCATION_NAME_TO_ID[location] in ctx.locations_checked:
            return False
        address, bit_position = LOCATION_ADDRESS_BITS[location][0], LOCATION_ADDRESS_BITS[location][1]
        byte = dme.read_byte(address)
        if bit_position in extract_bitflag_list(byte):
            ctx.locations_checked.add(LOCATION_NAME_TO_ID[location])
            return True
        return False
    for location_data in LOCATION_ADDRESS_BITS:
            _check_location_flag(ctx, location_data)
    address, bit_position = 0x801AD2CE, 2
    byte = dme.read_byte(address)
    if bit_position in extract_bitflag_list(byte):
        ctx.victory = True
    
    locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
    if locations_checked:
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": locations_checked}])

    if ctx.victory and not ctx.finished_game:
        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
        ctx.finished_game = True


async def give_items(ctx: NarutoContext):
    """
    Give items to the player in the game.

    :param ctx: The Naruto Clash of Ninja 2 context
    """
    expected_idx = ctx.expected_idx

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


def _give_item_in_game(ctx: NarutoContext, item) -> bool:
    """
    Give an item to the player in the game.

    :param ctx: The Naruto Clash of Ninja 2 context
    :param item: The item data to give
    :return: True if the item was given successfully, False otherwise
    """
    itemname = ID_TO_ITEM_NAME[item.item]
    if "Coupon" in itemname:
        set_value_bytes(TICKET_ADDRESSES[itemname], 0, ctx.regular_price, 32, 4, "big")
    else:
        money = read_value_bytes(0x801AD2A0, 0, 32, 4, "big")
        set_value_bytes(0x801AD2A0, 0, money+1000, 32, 4, "big")
    return True



async def game_watcher(ctx: NarutoContext):
    """
    Main game watcher loop.

    :param ctx: The Naruto Clash of Ninja 2 context
    """
    while not ctx.exit_event.is_set():
        try:
            if not dme.is_hooked() or ctx.slot is None:
                await asyncio.sleep(1)
                continue
            if ctx.shopinit == False:
                for x in TICKET_ADDRESSES:
                    set_value_bytes(TICKET_ADDRESSES[x], 0, 123456, 32, 4, "big")
                for x in UNTICKETED:
                    set_value_bytes(UNTICKETED[x], 0, ctx.regular_price, 32, 4, "big")
                ctx.shopinit = True
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


async def dolphin_sync_task(ctx: NarutoContext) -> None:
    """
    Task to manage the connection and synchronization with the Dolphin emulator.

    :param ctx: The Naruto Clash of Ninja 2 context
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
                    if dme.read_bytes(0x80000000, 6) != b"GNUEDA":
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
    Main entry point for the Naruto Clash of Ninja 2 client.

    :param launch_args: Command-line arguments for the client
    """
    parser = get_base_parser()
    args = parser.parse_args(launch_args)

    async def _main(connect, password):
        """
        Main asynchronous function for the Naruto Clash of Ninja 2 client.

        :param connect: The server address to connect to
        :param password: The password for server authentication
        """
        ctx = NarutoContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

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
    Utils.init_logging("NarutoClient", exception_logger="Client")
    main(*sys.argv[1:])
