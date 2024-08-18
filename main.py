import arcade
from arcade import PymunkPhysicsEngine

from animated_player import PlayerState
from game_sprites import Player

SCALE = 3

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.camera = None

        # Our TileMap Object
        self.tile_map = None
        # Name of map file to load
        map_name = "maps/dungeon.tmx"
        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Bricks": {
                "use_spatial_hash": True,
            },
        }
        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, SCALE, layer_options)

        player_position = self.tile_map.object_lists["Sprite Positions"][0].properties
        self.player = Player(center_x=player_position["X"]*SCALE, center_y=player_position["Y"]*SCALE, scale=1)

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # Our Scene Object
        self.scene = None
        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Our physics engine
        self.physics_engine = None

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            walls=self.scene["Bricks"]
        )

        self.camera = arcade.Camera2D([0, 0, width, height])

    def on_draw(self):
        self.clear()
        self.camera.use()

        # Draw our Scene
        self.scene.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player.update_animation()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = 5
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -5
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = -5
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 5
        elif key == arcade.key.SPACE:
            self.player.change_state(PlayerState.DIE)
            self.player.change_x = 0
            self.player.change_y = 0

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player.change_y = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0
        elif key == arcade.key.SPACE:
            self.player.change_state(PlayerState.DIE)
            # pass


def main():
    window = MyGame(1280, 720, "My Game")
    arcade.run()


if __name__ == "__main__":
    main()
