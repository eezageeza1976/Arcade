import time

from arcade import Sprite, Texture
import enum
import logging
import math


class PlayerState(enum.Enum):
    FACE_DOWN = 1
    FACE_LEFT = 2
    FACE_RIGHT = 3
    FACE_UP = 4
    DIE = 5


logger = logging.getLogger("arcade")


class AnimatedPlayerSprite(Sprite):
    """
    Deprecated Sprite for platformer games that supports walking animations.
    Make sure to call update_animation after loading the animations so the
    initial texture can be set. Or manually set it.

    It is highly recommended you create your own version of this class rather than
    try to use this pre-packaged one.

    For an example, see this section of the platformer tutorial:
    :ref:`platformer_part_twelve`.

    Args:
        scale:
            Initial scale of the sprite.
        center_x:
            Initial x position of the sprite.
        center_y:
            Initial y position of the sprite.
    """

    def __init__(
        self,
        scale: float = 1.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        **kwargs,
    ):
        super().__init__(
            None,
            scale=scale,
            center_x=center_x,
            center_y=center_y,
        )
        self.time = None
        self.state = PlayerState.FACE_RIGHT
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

    def change_state(self, change_state):
        self.state = change_state

    def update_animation(self, delta_time: float = 1 / 60) -> None:
        """
        Logic for texture animation.

        Args:
            delta_time: Time since last update.
        """
        x1 = self.center_x
        x2 = self.last_texture_change_center_x
        y1 = self.center_y
        y2 = self.last_texture_change_center_y
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        texture_list: list[Texture] = []

        change_direction = False
        if (
            self.change_x > 0
            and self.change_y == 0
            and self.state != PlayerState.FACE_RIGHT
            and len(self.walk_right_textures) > 0
        ):
            self.state = PlayerState.FACE_RIGHT
            change_direction = True
        elif (
            self.change_x < 0
            and self.change_y == 0
            and self.state != PlayerState.FACE_LEFT
            and len(self.walk_left_textures) > 0
        ):
            self.state = PlayerState.FACE_LEFT
            change_direction = True
        elif (
            self.change_y < 0
            and self.change_x == 0
            and self.state != PlayerState.FACE_DOWN
            and len(self.walk_down_textures) > 0
        ):
            self.state = PlayerState.FACE_DOWN
            change_direction = True
        elif (
            self.change_y > 0
            and self.change_x == 0
            and self.state != PlayerState.FACE_UP
            and len(self.walk_up_textures) > 0
        ):
            self.state = PlayerState.FACE_UP
            change_direction = True

        if self.change_x == 0 and self.change_y == 0:
            if self.state == PlayerState.FACE_LEFT:
                self.texture = self.stand_left_textures[0]
            elif self.state == PlayerState.FACE_RIGHT:
                self.texture = self.stand_right_textures[0]
            elif self.state == PlayerState.FACE_UP:
                self.texture = self.walk_up_textures[0]
            elif self.state == PlayerState.FACE_DOWN:
                self.texture = self.walk_down_textures[0]
            elif self.state == PlayerState.DIE:
                self.texture = self.die_textures[5]

        elif change_direction or distance >= self.texture_change_distance:
            self.last_texture_change_center_x = self.center_x
            self.last_texture_change_center_y = self.center_y

            if self.state == PlayerState.FACE_LEFT:
                texture_list = self.walk_left_textures
                if texture_list is None or len(texture_list) == 0:
                    raise RuntimeError(
                        "update_animation was called on a sprite that doesn't have a "
                        "list of walk left textures."
                    )
            elif self.state == PlayerState.FACE_RIGHT:
                texture_list = self.walk_right_textures
                if texture_list is None or len(texture_list) == 0:
                    raise RuntimeError(
                        "update_animation was called on a sprite that doesn't have a list of "
                        "walk right textures."
                    )
            elif self.state == PlayerState.FACE_UP:
                texture_list = self.walk_up_textures
                if texture_list is None or len(texture_list) == 0:
                    raise RuntimeError(
                        "update_animation was called on a sprite that doesn't have a list of "
                        "walk up textures."
                    )
            elif self.state == PlayerState.FACE_DOWN:
                texture_list = self.walk_down_textures
                if texture_list is None or len(texture_list) == 0:
                    raise RuntimeError(
                        "update_animation was called on a sprite that doesn't "
                        "have a list of walk down textures."
                    )
            elif self.state == PlayerState.DIE:
                texture_list = self.die_textures
                if texture_list is None or len(texture_list) == 0:
                    raise RuntimeError(
                        "update_animation was called on a sprite that doesn't "
                        "have a list of die textures."
                    )
                # self.automatic_animation()

            self.cur_texture_index += 1
            if self.cur_texture_index >= len(texture_list):
                self.cur_texture_index = 0

            self.texture = texture_list[self.cur_texture_index]

        if self._texture is None:
            logger.warning("Error, no texture set")
        else:
            self.width = self._texture.width * self.scale_x
            self.height = self._texture.height * self.scale_x

    def automatic_animation(self, delta_time: float = 1 / 60, **kwargs) -> None:
        """
        Logic for updating the animation.

        Args:
            delta_time: Time since last update.
        """
        if self.die_textures is None:
            raise RuntimeError("No animation set for this sprite.")

        if self.cur_texture_index >= len(self.die_textures):
            self.cur_texture_index = 0
            time.sleep(2)
            self.change_state(PlayerState.FACE_DOWN)
        else:
            self.texture = self.die_textures[self.cur_texture_index]
            self.change_x = 0
            self.change_y = 0
            self.cur_texture_index += 1
            time.sleep(0.1)
