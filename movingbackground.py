import arcade
import os

# --- Constants ---
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 300
IMAGE_WIDTH = 500
SCROLL_SPEED = 5

class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

    def setup(self):

    
        self.background_list = arcade.SpriteList()

        self.background_sprite = arcade.Sprite("Imporved night sky background.png")

        self.background_sprite.center_x = IMAGE_WIDTH // 2
        self.background_sprite.center_y = SCREEN_HEIGHT // 2
        self.background_sprite.change_x = -SCROLL_SPEED

        self.background_list.append(self.background_sprite)


        self.background_sprite_2 = arcade.Sprite("Imporved night sky background.png")

        self.background_sprite_2.center_x = SCREEN_WIDTH + IMAGE_WIDTH // 2
        self.background_sprite_2.center_y = SCREEN_HEIGHT // 2
        self.background_sprite_2.change_x = -SCROLL_SPEED

        self.background_list.append(self.background_sprite_2)

    def on_draw(self):
        arcade.start_render()
        self.background_list.draw()

    def on_update(self, delta_time):

        if self.background_sprite.left == -IMAGE_WIDTH:
            self.background_sprite.center_x = SCREEN_WIDTH + IMAGE_WIDTH // 2

        if self.background_sprite_2.left == -IMAGE_WIDTH:
            self.background_sprite_2.center_x = SCREEN_WIDTH + IMAGE_WIDTH // 2

        self.background_list.update()

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()