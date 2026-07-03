from worlds.LauncherComponents import Component, Type, components, icon_paths, launch

from .world import HelloKittyWorld as HelloKittyWorld

def run_client(*args: str) -> None:
    """Run the Hello Kitty: Roller Rescue client with the provided arguments."""
    from .HelloKittyClient import main

    launch(main, name="Hello Kitty: Roller Rescue Client", args=args)

components.append(
    Component(
        "Hello Kitty: Roller Rescue Client",
        func=run_client,
        game_name="Hello Kitty: Roller Rescue Client",
        component_type=Type.CLIENT,
        supports_uri=True
    )
)
