import math
from typing import Tuple
import random
import os
import arcade

SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_ENEMY = 0.5
SPRITE_SCALING_BULLET = 0.25
INDICATOR_BAR_OFFSET = 32
ENEMY_ATTACK_COOLDOWN = 1
BULLET_SPEED = 3
BULLET_DAMAGE = 1
PLAYER_HEALTH = 10^99999999999999999
BULLET_ACCELERATION=1.0010
BULLET_UPDATE=80

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Apple pie is cool"


def sprite_off_screen(
    sprite: arcade.Sprite,
    screen_height: int = SCREEN_HEIGHT,
    screen_width: int = SCREEN_WIDTH,
) -> bool:
    """Checks if a sprite is off-screen or not."""
    return (
        sprite.top < 0
        or sprite.bottom > screen_height
        or sprite.right < 0
        or sprite.left > screen_width
    )


class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Menu Screen", WIDTH / 2, HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", WIDTH / 2, HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Instructions Screen", WIDTH / 2, HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", WIDTH / 2, HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)

class Player(arcade.Sprite):
    def __init__(self, bar_list: arcade.SpriteList) -> None:
        super().__init__(
            filename="Cuphead_in_plane.webp",
            scale=SPRITE_SCALING_PLAYER,
        )
        self.indicator_bar: IndicatorBar = IndicatorBar(
            self, bar_list, (self.center_x, self.center_y)
        )
        self.health: int = PLAYER_HEALTH


class Bullet(arcade.Sprite):
    def __init__(self) -> None:
        super().__init__(
            filename="super shuriken.png",
            scale=SPRITE_SCALING_BULLET,
        )
        self.speed = BULLET_SPEED
        self.timer = 0

    def on_update(self, delta_time: float = 1 / 60) -> None:
        """Updates the bullet's position."""
        self.position = (
            self.center_x + self.change_x * delta_time,
            self.center_y + self.change_y * delta_time,
        )
        self.timer += 1


class IndicatorBar:
    """
    Represents a bar which can display information about a sprite.

    :param Player owner: The owner of this indicator bar.
    :param arcade.SpriteList sprite_list: The sprite list used to draw the indicator
    bar components.
    :param Tuple[float, float] position: The initial position of the bar.
    :param arcade.Color full_color: The color of the bar.
    :param arcade.Color background_color: The background color of the bar.
    :param int width: The width of the bar.
    :param int height: The height of the bar.
    :param int border_size: The size of the bar's border.
    """

    def __init__(
        self,
        owner: Player,
        sprite_list: arcade.SpriteList,
        position: Tuple[float, float] = (0, 0),
        full_color: arcade.Color = arcade.color.GREEN,
        background_color: arcade.Color = arcade.color.BLACK,
        width: int = 100,
        height: int = 4,
        border_size: int = 4,
    ) -> None:
        # Store the reference to the owner and the sprite list
        self.owner: Player = owner
        self.sprite_list: arcade.SpriteList = sprite_list

        # Set the needed size variables
        self._box_width: int = width
        self._box_height: int = height
        self._half_box_width: int = self._box_width // 2
        self._center_x: float = 0.0
        self._center_y: float = 0.0
        self._fullness: float = 0.0

        # Create the boxes needed to represent the indicator bar
        self._background_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width + border_size,
            self._box_height + border_size,
            background_color,
        )
        self._full_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width,
            self._box_height,
            full_color,
        )
        self.sprite_list.append(self._background_box)
        self.sprite_list.append(self._full_box)

        # Set the fullness and position of the bar
        self.fullness: float = 1.0
        self.position: Tuple[float, float] = position

    def __repr__(self) -> str:
        return f"<IndicatorBar (Owner={self.owner})>"

    @property
    def background_box(self) -> arcade.SpriteSolidColor:
        """Returns the background box of the indicator bar."""
        return self._background_box

    @property
    def full_box(self) -> arcade.SpriteSolidColor:
        """Returns the full box of the indicator bar."""
        return self._full_box

    @property
    def fullness(self) -> float:
        """Returns the fullness of the bar."""
        return self._fullness

    @fullness.setter
    def fullness(self, new_fullness: float) -> None:
        """Sets the fullness of the bar."""
        # Check if new_fullness if valid
        if not (0.0 <= new_fullness <= 1.0):
            raise ValueError(
                f"Got {new_fullness}, but fullness must be between 0.0 and 1.0."
            )

        # Set the size of the bar
        self._fullness = new_fullness
        if new_fullness == 0.0:
            # Set the full_box to not be visible since it is not full anymore
            self.full_box.visible = False
        else:
            # Set the full_box to be visible incase it wasn't then update the bar
            self.full_box.visible = True
            self.full_box.width = self._box_width * new_fullness
            self.full_box.left = self._center_x - (self._box_width // 2)

    @property
    def position(self) -> Tuple[float, float]:
        """Returns the current position of the bar."""
        return self._center_x, self._center_y

    @position.setter
    def position(self, new_position: Tuple[float, float]) -> None:
        """Sets the new position of the bar."""
        # Check if the position has changed. If so, change the bar's position
        if new_position != self.position:
            self._center_x, self._center_y = new_position
            self.background_box.position = new_position
            self.full_box.position = new_position

            # Make sure full_box is to the left of the bar instead of the middle
            self.full_box.left = self._center_x - (self._box_width // 2)



class MyGame(arcade.Window):
    def __init__(self) -> None:
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.bullet_list = arcade.SpriteList()
        self.bar_list = arcade.SpriteList()
        self.player_sprite = Player(self.bar_list)
        self.enemy_sprite = arcade.Sprite("improvdog.png", SPRITE_SCALING_ENEMY)
        self.top_text: arcade.Text = arcade.Text(
            "I love apple pie",
            self.width // 2,
            self.height - 50,
            anchor_x="center",
        )
        self.bottom_text: arcade.Text = arcade.Text(
            "Where can I buy some apple pie!?",
            self.width // 2,
            50,
            anchor_x="center",
        )
        self.enemy_timer = 0
        self.screen_counter = 0

    def setup(self) -> None:
        """Set up the game and initialize the variables."""
        # Setup player and enemy positions
        self.player_sprite.position = self.width // 2, self.height // 4
        self.enemy_sprite.position = self.width // 1.25, self.height // 2

        # Set the background color
        self.background = arcade.load_texture("Imporved night sky background.png")
        self.background1_x = 0
        self.background2_x = SCREEN_WIDTH

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """
        # Gunshot sound
        # arcade.play_sound(self.gun_sound)
        # Create a bullet
        bullet = arcade.Sprite("Mega_Blast.webp")

        # The image points to the right, and we want it to point up. So
        # rotate it.
        bullet.angle = 90
        # Give the bullet a speed

        # Position the bullet
        bullet.center_x = self.player_sprite.center_x
        bullet.bottom = self.player_sprite.top

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)

    def on_draw(self) -> None:
        """Render the screen."""
        # Clear the screen. This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites

        arcade.draw_lrwh_rectangle_textured(self.background1_x, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        arcade.draw_lrwh_rectangle_textured(self.background2_x, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        self.background1_x -= 4
        self.background2_x -= 4
        if self.background1_x == -SCREEN_WIDTH:
            self.background1_x = SCREEN_WIDTH
        if self.background2_x == -SCREEN_WIDTH:
            self.background2_x = SCREEN_WIDTH

        self.player_sprite.draw()
        self.enemy_sprite.draw()
        self.bullet_list.draw()
        self.bar_list.draw()



        # Draw the text objects
        self.top_text.draw()
        self.bottom_text.draw()

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        """Called whenever the mouse moves."""
        self.player_sprite.position = x, y

    def on_update(self, delta_time, enemy=None) -> None:
        """Movement and game logic."""
        self.screen_counter += 1
        # Check if the player is dead. If so, exit the game
        if self.player_sprite.health <= 0:
            arcade.exit()

        # Increase the enemy's timer
        self.enemy_timer += delta_time

        # Update the player's indicator bar position
        self.player_sprite.indicator_bar.position = (
            self.player_sprite.center_x,
            self.player_sprite.center_y + INDICATOR_BAR_OFFSET,
        )

        # Call updates on bullet sprites
        self.bullet_list.on_update(delta_time)

        # Check if the enemy can attack. If so, shoot a bullet from the
        # enemy towards the player
        if self.enemy_timer >= ENEMY_ATTACK_COOLDOWN:
            self.enemy_timer = 0

            # Create the bullet
            bullet = Bullet()

            # Set the bullet's position
            bullet.position = self.enemy_sprite.position

            # Set the bullet's angle to face the player
            diff_x = self.player_sprite.center_x - self.enemy_sprite.center_x
            diff_y = self.player_sprite.center_y - self.enemy_sprite.center_y
            angle = math.atan2(diff_y, diff_x)
            angle_deg = math.degrees(angle)
            if angle_deg < 0:
                angle_deg += 360
            bullet.angle = angle_deg





            # Give the bullet a velocity towards the player
            # bullet.change_x = math.cos(angle) * BULLET_SPEED
            # bullet.change_y = math.sin(angle) * BULLET_SPEED

            # Add the bullet to the bullet list
            self.bullet_list.append(bullet)

        # Loop through each bullet
        for existing_bullet in self.bullet_list:
            existing_bullet: Bullet
            # Check if the bullet has gone off-screen. If so, delete the bullet
            if sprite_off_screen(existing_bullet):
                existing_bullet.remove_from_sprite_lists()
                continue
            if existing_bullet.timer>random.randint(200,400):
                existing_bullet.remove_from_sprite_lists()

            # Check if the bullet has hit the player
            if arcade.check_for_collision(existing_bullet, self.player_sprite):
                # Damage the player and remove the bullet
                self.player_sprite.health -= BULLET_DAMAGE
                existing_bullet.remove_from_sprite_lists()

                # Set the player's indicator bar fullness
                self.player_sprite.indicator_bar.fullness = (
                    self.player_sprite.health / PLAYER_HEALTH
                )


            # First, calculate the angle to the player. We could do this
            # only when the bullet fires, but in this case we will rotate
            # the enemy to face the player each frame, so we'll do this
            # each frame.

            # Position the start at the enemy's current location
            start_x = existing_bullet.center_x
            start_y = existing_bullet.center_y

            if self.screen_counter%BULLET_UPDATE==0:
                # Get the destination location for the bullet
                dest_x = self.player_sprite.center_x
                dest_y = self.player_sprite.center_y

                # Do math to calculate how to get the bullet to the destination.
                # Calculation the angle in radians between the start points
                # and end points. This is the angle the bullet will travel.
                x_diff = dest_x - start_x
                y_diff = dest_y - start_y
                angle = math.atan2(y_diff, x_diff)

                # Set the enemy to face the player.
                existing_bullet.angle = math.degrees(angle) + 180
            else:
                angle = math.radians(existing_bullet.angle - 180)

            existing_bullet.speed *= BULLET_ACCELERATION #accelerate the bullet
            existing_bullet.center_x += math.cos(angle) * existing_bullet.speed
            existing_bullet.center_y += math.sin(angle) * existing_bullet.speed


def main() -> None:
    """Main Program."""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
