
import arcade
import math
import os

from pyglet.media import player

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Craphead"
BULLET_SPEED = 10



class MyGame(arcade.Window):
    """ Main application class """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)


        self.gun_sound = arcade.sound.load_sound(":resources:sounds/laser1.wav")
        self.hit_sound = arcade.sound.load_sound(":resources:sounds/phaseJump1.wav")
        self.gun_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")
        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.BLACK)

        self.frame_count = 0

        self.enemy_list = None
        self.bullet_list = None
        self.player_list = None
        self.player = None
        self.background = None





    def setup(self):
        self.background = arcade.load_texture("Imporved night sky background.png")
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()




        # Add player ship
        self.player = arcade.Sprite("Cuphead_in_plane.webp", 0.75)
        self.player_list.append(self.player)
        self.player.angle = 0

        # Add top-left enemy ship
        enemy = arcade.Sprite("improvdog.png", 1)
        enemy.center_x = SCREEN_WIDTH - enemy.height
        enemy.center_y = 120
        enemy.angle = 270
        self.enemy_list.append(enemy)

        # Add top-right enemy ship
        enemy = arcade.Sprite("improvdog.png", 1)
        enemy.center_x = SCREEN_WIDTH - 120
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)



    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """
        # Gunshot sound
        arcade.play_sound(self.gun_sound)
        # Create a bullet
        bullet = arcade.Sprite("Mega_Blast.webp")

        # The image points to the right, and we want it to point up. So
        # rotate it.
        bullet.angle = 90

        # Give the bullet a speed
        bullet.change_y = BULLET_SPEED

        # Position the bullet
        bullet.center_x = self.player.center_x
        bullet.bottom = self.player.top

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)


    def on_draw(self):
        """Render the screen. """

        self.clear()

        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

    def on_update(self, delta_time):
        """All the logic to move, and the game logic goes here. """

        self.frame_count += 1

        # Loop through each enemy that we have
        for enemy in self.enemy_list:

            # First, calculate the angle to the player. We could do this
            # only when the bullet fires, but in this case we will rotate
            # the enemy to face the player each frame, so we'll do this
            # each frame.

            # Position the start at the enemy's current location
            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = self.player.center_x
            dest_y = self.player.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle) +180

            # Shoot every 60 frames change of shooting each frame
            if self.frame_count % 80  == 0:
                bullet = arcade.Sprite("projectile.png")
                bullet.center_x = start_x
                bullet.center_y = start_y

                # Angle the bullet sprite
                bullet.angle = math.degrees(angle) +180

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                self.bullet_list.append(bullet)

        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

        self.bullet_list.update()
    def on_update(self, delta_time):
        """All the logic to move, and the game logic goes here. """

        self.frame_count += 1

        # Loop through each enemy that we have
        for enemy in self.enemy_list:

            # First, calculate the angle to the player. We could do this
            # only when the bullet fires, but in this case we will rotate
            # the enemy to face the player each frame, so we'll do this
            # each frame.

            # Position the start at the enemy's current location
            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = self.player.center_x
            dest_y = self.player.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle) +180

            # Shoot every 60 frames change of shooting each frame
            if self.frame_count % 27 == 0:
                bullet = arcade.Sprite("projectile.png")
                bullet.center_x = start_x
                bullet.center_y = start_y

                # Angle the bullet sprite
                bullet.angle = math.degrees(angle) +180

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                self.bullet_list.append(bullet)

        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

        self.bullet_list.update()



    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """Called whenever the mouse moves. """
        self.player.center_x = x
        self.player.center_y = y


def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
