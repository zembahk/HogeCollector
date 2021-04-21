
import random
import arcade
import os


SPRITE_AVATAR_SCALING = 0.125
SPRITE_COIN_SCALING = 0.25


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

        # zembahk edit
        self.total_time = -3.0
        self.win_time = 0.0
        self.win_txt = "you won"


    def setup(self):
        """ Set the value of the variable """
       
        # Assign values ​​to background variables
        self.background = arcade.load_texture("images/background.jpg")

        # Instantiate a list of roles
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set player character
        self.score = 0
        self.player_sprite = arcade.Sprite("images/character.png", SPRITE_AVATAR_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        for i in range(100):

            # Instantiate gold coins
            coin = arcade.Sprite("images/hoge_coin.png", SPRITE_COIN_SCALING)

            # Place gold coins
            coin.center_x = random.randrange((coin.width + 150), SCREEN_WIDTH - (coin.width + 150))
            coin.center_y = random.randrange((coin.height + 150), SCREEN_HEIGHT - (coin.height + 150))

            # Give direction
            coin_slowest = 30
            coin_fastest = 350
            while True:
                coin.delta_x = random.randrange(coin_fastest * -1, coin_fastest)
                coin.delta_y = random.randrange(coin_fastest * -1, coin_fastest)
                if (coin.delta_x > coin_slowest or coin.delta_x < coin_slowest * -1) and (coin.delta_y > coin_slowest or coin.delta_y < coin_slowest * -1):
                    break
                
            # Set up the initial angle, and the "spin"
            coin.angle = random.randrange(360)
            while True:
                coin.change_angle = random.randrange(-2, 7)
                if coin.change_angle > 1 or coin.change_angle < -0.5:
                    break
            # Add gold coins to the list
            self.coin_list.append(coin)
            

    def on_draw(self):
        """
        Render screen
        """

        # Start rendering screen
        arcade.start_render()

        # Draw a textured rectangle 
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw title box in the middle of the screen.
        if self.total_time < 0:
            output = "HOGE COLLECTOR"
            arcade.draw_text(output, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.3, arcade.color.WHITE, 36, width=400, align="center", anchor_x="center", anchor_y="center")

            if self.total_time < -2:
                arcade.draw_text("3", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5, arcade.color.WHITE, 54, width=75, align="center", anchor_x="center", anchor_y="center")
            if self.total_time > -2 and self.total_time < -1:
                arcade.draw_text("2", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5, arcade.color.WHITE, 54, width=75, align="center", anchor_x="center", anchor_y="center")
            if self.total_time > -1 and self.total_time < 0:
                arcade.draw_text("1", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5, arcade.color.WHITE, 54, width=75, align="center", anchor_x="center", anchor_y="center")

        else:
            

            # Draw all characters
            self.coin_list.draw()
            self.player_list.draw()

            # Draw text 
            arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)


            # Calculate seconds by using a modulus (remainder)
            seconds = float(self.total_time) % 60

            # Figure out our output
            output = f"Time: {seconds:.2f}"
            # zemabhk edit
            self.win_txt = f"Won in {self.win_time:.6f} seconds"
        
            # Output the timer text.
            # zembahk edit
            if self.win_time == 0:
                arcade.draw_text(output, 10, 50, arcade.color.WHITE, 18)
            else:
                arcade.draw_text(self.win_txt, 10, 50, arcade.color.WHITE, 26)
            
    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """

        self.total_time += delta_time

        if self.win_time > 0 and self.total_time - self.win_time > 2:
            arcade.close_window()
            #return self.win_txt
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
        coin_left = len(self.coin_list)
        for i in range(0, coin_left):
            coin = self.coin_list[i]
            
            # Figure out if we hit the edge and need to reverse.
            wall_buffer = 5
            if coin.center_x < coin.width // 2 + wall_buffer or coin.center_x > SCREEN_WIDTH - coin.width // 2 - wall_buffer:
                coin.delta_x *= -1
            if coin.center_y < coin.height // 2 + wall_buffer or coin.center_y > SCREEN_HEIGHT - coin.height // 2 - wall_buffer:
                coin.delta_y *= -1

            coin.center_x += coin.delta_x * delta_time
            coin.center_y += coin.delta_y * delta_time

        # Collision detection between player and gold coin
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Directly kill the gold coins encountered and add points
        for coin in hit_list:
            coin.kill()
            self.score += 1

        # zembahk edit
        if self.score == 100 and self.win_time == 0: 
            self.win_time = self.total_time
            

def play():
    """ Main method """
    
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    #while True:
        play()
        #print(MyGame.win_time)
        #answer = input("Restart?(y/n)  ")
        #if answer == 'y':
            
           # continue
       # else:
          #  break
    
