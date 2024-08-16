import arcade
import animated_player


class Player(animated_player.AnimatedPlayerSprite):
    def __init__(self, center_x=0, center_y=0, scale=1):
        super().__init__(center_x=center_x, center_y=center_y, scale=scale)

        self.stand_right_textures = []
        self.stand_left_textures = []
        self.stand_down_textures = []
        self.stand_up_textures = []
        self.walk_left_textures = []
        self.walk_right_textures = []
        self.walk_up_textures = []
        self.walk_down_textures = []
        self.die_textures = []
        self.cur_texture_index = 0
        self.texture_change_distance = 20
        self.last_texture_change_center_x: float = 0.0
        self.last_texture_change_center_y: float = 0.0

        player_spritesheet_character1 = arcade.SpriteSheet("sprites/character1_universal.png")

        for i in range(0, 9, 1):
            self.walk_up_textures.append(player_spritesheet_character1.get_texture(
                x=i * 64, y=512, width=64, height=64))
            self.walk_left_textures.append(player_spritesheet_character1.get_texture(
                x=i * 64, y=576, width=64, height=64))
            self.walk_down_textures.append(player_spritesheet_character1.get_texture(
                x=i * 64, y=640, width=64, height=64))
            self.walk_right_textures.append(player_spritesheet_character1.get_texture(
                x=i * 64, y=704, width=64, height=64))
            if i == 0:
                self.stand_up_textures.append(self.walk_up_textures[0])
                self.stand_left_textures.append(self.walk_left_textures[0])
                self.stand_down_textures.append(self.walk_down_textures[0])
                self.stand_right_textures.append(self.walk_right_textures[0])

        for i in range(0, 6):
            self.die_textures.append(player_spritesheet_character1.get_texture(
                x=i * 64, y=1280, width=64, height=64))
