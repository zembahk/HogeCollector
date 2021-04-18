
import random
import arcade
import os

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Hoge coin collecting game"


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        """ Initializer """

        # Call the parent class method, create a new window
        super().__init__(width, height, title)

        # Set the working directory, 
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Background image definition
        self.background = None

        # Player list and gold coin list definition
        self.player_list = None
        self.coin_list = None

        # Player information
        self.player_sprite = None
        self.score = 0
        self.score_text = None

        # Do not display the mouse pointer
        self.set_mouse_visible(False)

        # Set background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set the value of the variable """
        # Assign values ​​to background variables
        self.background = arcade.load_texture("images/background.jpg")

        # Instantiate a list of roles
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set player character
        self.score = 0
        self.player_sprite = arcade.Sprite("images/character.png", SPRITE_SCALING / 4)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        for i in range(50):

            # Instantiate gold coins
            coin = arcade.Sprite("images/hoge_coin.png", SPRITE_SCALING / 2)

            # Place gold coins
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            # Add gold coins to the list
            self.coin_list.append(coin)

    def on_draw(self):
        """
        Render screen
        """

        # Start rendering screen
        arcade.start_render()

        # Draw a textured rectangle 
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw all characters
        self.coin_list.draw()
        self.player_list.draw()

        # Draw text 
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Mouse movement event
        """
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def update(self, delta_time):
        """ Mobile game logic"""

        # Gold coin list update
        self.coin_list.update()

        # Collision detection between player and gold coin
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Directly kill the gold coins encountered and add points
        for coin in hit_list:
            coin.kill()
            self.score += 1


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
