from worlds.LauncherComponents import Component, Type, components, icon_paths, launch

from .world import NarutoWorld as NarutoWorld

def run_client(*args: str) -> None:
    """Run the Naruto Clash of Ninja 2 client with the provided arguments."""
    from .NarutoClient import main

    launch(main, name="Naruto Clash of Ninja 2 Client", args=args)

components.append(
    Component(
        "Naruto Clash of Ninja 2 Client",
        func=run_client,
        game_name="Naruto Clash of Ninja 2",
        component_type=Type.CLIENT,
        supports_uri=True
    )
)