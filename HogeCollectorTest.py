import subprocess
import sys
import os
import shutil

from tempfile import gettempdir
tmp = os.path.join(gettempdir(), '.{}'.format(hash(os.times())))
if not os.path.exists(tmp):
    os.makedirs(tmp)


def GetPackage(package):
    try:
        try:
            module = __import__(package)
            return module
        except Exception:
            subprocess.check_call([sys.executable, \
                                   '-m', 'pip', 'install', package])
            module = __import__(package)
            return module
    except Exception as e:
        print('Error: %s' % str(e))


if 'requests' not in sys.modules:
    requests = GetPackage('requests')
if 'arcade' not in sys.modules:
    arcade = GetPackage('arcade')


def GetFile(url, file_name):
    FILE = requests.get(url, stream=True)
    if FILE.status_code == 200:
        FILE.raw.decode_content = True
        saved_file = tmp + '\\' + file_name
        with open(saved_file, 'wb') as f:
            shutil.copyfileobj(FILE.raw, f)
            print('%s' % str(saved_file))
        return str(saved_file)
    else:
        print('%s couldn\'t be retreived' % str(file_name))


url_base = 'https://ipfs.io/ipfs/'
file_hash = 'QmXFTAUy2mRo4Lcb4yi7aeyBTJoADnEqqnH8zwNC3EdTge'
background_ipfs = 'QmZocCDpmZTundwxqVSW73CZ7kmHFKSrreF7hzzqiB2kcT'
avatar_ipfs = 'QmUg7Hgv4jRcqrFhnhY6DdqKsP9W71ram22GXayZhaDuvE'
coin_ipfs = 'QmVsaqaWAYe4L6Z4uzXka7B3d4jYGrpJEGzZYc2d7oXth5'
HOGE_GAME = GetFile(url_base + file_hash, 'HogeCollector.py')
BACKGROUND_IMAGE = GetFile(url_base + background_ipfs, 'background.png')
AVATAR_IMAGE = GetFile(url_base + avatar_ipfs, 'avatar.png')
COIN_IMAGE = GetFile(url_base + coin_ipfs, 'coin.png')




import random


SPRITE_AVATAR_SCALING = 1
SPRITE_COIN_SCALING = 1

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Hoge coin collecting game'

MOUSE_X = SCREEN_WIDTH / 2
MOUSE_Y = SCREEN_HEIGHT / 2
BEST_SCORE = 0.0

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
        self.win_txt = 'You Won!'
        self.restart_wait = 1.0

    def setup(self):
        """ Set the value of the variable """

        self.total_time = -3.0
        self.win_time = 0.0
                
        # Assign values ??????to background variables
        self.background = arcade.load_texture(BACKGROUND_IMAGE)

        # Instantiate a list of roles
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set player character
        self.score = 0
        self.player_sprite = arcade.Sprite(AVATAR_IMAGE, SPRITE_AVATAR_SCALING)
        self.player_sprite.center_x = MOUSE_X
        self.player_sprite.center_y = MOUSE_Y
        self.player_list.append(self.player_sprite)

        for i in range(100):

            # Instantiate gold coins
            coin = arcade.Sprite(COIN_IMAGE, SPRITE_COIN_SCALING)

            # Place gold coins
            coin.center_x = random.randrange((coin.width + 150), \
                                             SCREEN_WIDTH - (coin.width + 150))
            coin.center_y = random.randrange((coin.height + 150), \
                                             SCREEN_HEIGHT - (coin.height + 150))

            # Give direction
            coin_slowest = 30
            coin_fastest = 350
            while True:
                coin.delta_x = random.randrange(coin_fastest * -1, coin_fastest)
                coin.delta_y = random.randrange(coin_fastest * -1, coin_fastest)
                if (coin.delta_x > coin_slowest or \
                            coin.delta_x < coin_slowest * -1) \
                      and (coin.delta_y > coin_slowest or \
                            coin.delta_y < coin_slowest * -1):
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
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, \
                                SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        global BEST_SCORE
        arcade.draw_text(f'Best: {BEST_SCORE:.6f}', 20, \
                         SCREEN_HEIGHT * 0.95, arcade.color.WHITE, 20)

        # Draw title box in the middle of the screen.
        if self.total_time < 0:
            output = 'HOGE COLLECTOR'
            arcade.draw_text(output, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.3, \
                        arcade.color.WHITE, 36, width=400, \
                        align='center', anchor_x='center', anchor_y='center')
            self.player_list.draw()
            if self.total_time < -2:
                arcade.draw_text('3', SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5, \
                        arcade.color.WHITE, 54, width=75, \
                        align='center', anchor_x='center', anchor_y='center')
            if self.total_time > -2 and self.total_time < -1:
                arcade.draw_text('2', SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5, \
                        arcade.color.WHITE, 54, width=75, \
                        align='center', anchor_x='center', anchor_y='center')
            if self.total_time > -1 and self.total_time < 0:
                arcade.draw_text('1', SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5, \
                        arcade.color.WHITE, 54, width=75, \
                        align='center', anchor_x='center', anchor_y='center')

        else:

            # Draw all characters
            self.coin_list.draw()
            self.player_list.draw()

            # Draw text 
            arcade.draw_text(f'Score: {self.score}', 10, 20, \
                             arcade.color.WHITE, 14)

            # Calculate seconds by using a modulus (remainder)
            seconds = float(self.total_time) % 60

            # Figure out our output
            output = f'Time: {seconds:.2f}'
            # zemabhk edit
            self.win_txt = f'Won in {self.win_time:.6f} seconds'

            # Output the timer text.
            # zembahk edit
            
            if self.win_time == 0:
                arcade.draw_text(output, 10, 50, arcade.color.WHITE, 18)
            elif self.win_time != 0 and \
                 self.total_time - self.win_time > self.restart_wait:
                arcade.draw_text(f'{self.win_time:.6f}', SCREEN_WIDTH // 2, \
                        SCREEN_HEIGHT // 1.3, arcade.color.WHITE, 64, \
                        align='center', anchor_x='center', anchor_y='center')
                arcade.draw_text('Press Space or Click', SCREEN_WIDTH // 2, \
                        SCREEN_HEIGHT // 5, arcade.color.WHITE, 26, \
                        align='center', anchor_x='center', anchor_y='center')
            else:
                arcade.draw_text(self.win_txt, 10, 50, arcade.color.WHITE, 26)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called whenever the mouse button is clicked.
        """
        if self.win_time != 0 and \
           self.total_time - self.win_time > self.restart_wait:
            self.setup()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        """
        if self.win_time != 0 and key == 32 and \
           self.total_time - self.win_time > self.restart_wait:
            self.setup()

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """

        self.total_time += delta_time

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Mouse movement event
        """
        global MOUSE_X
        global MOUSE_Y
        MOUSE_X = x
        MOUSE_Y = y
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
            if coin.center_x < (coin.width // 2) + wall_buffer or \
               coin.center_x > SCREEN_WIDTH - (coin.width // 2) - wall_buffer:
                coin.delta_x *= -1
            if coin.center_y < (coin.height // 2) + wall_buffer or \
               coin.center_y > SCREEN_HEIGHT - (coin.height // 2) - wall_buffer:
                coin.delta_y *= -1

            coin.center_x += coin.delta_x * delta_time
            coin.center_y += coin.delta_y * delta_time

        # Collision detection between player and gold coin
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, \
                                                        self.coin_list)

        # Directly kill the gold coins encountered and add points
        for coin in hit_list:
            coin.kill()
            self.score += 1

        # zembahk edit
        global BEST_SCORE
        if self.score == 100 and self.win_time == 0:
            self.win_time = self.total_time
        if self.win_time !=0:
            if (BEST_SCORE == 0 and BEST_SCORE != self.win_time) \
                    or (BEST_SCORE != 0 and self.win_time < BEST_SCORE):
                BEST_SCORE = self.win_time


def play():
    """ Main method """
    try:
        window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        window.setup()
        arcade.run()
    except Exception as e:
        print('Error: %s' % str(e))     
    finally:
        print(f'Best: {BEST_SCORE:.6f}')
    
    
if __name__ == '__main__':
    play()
    
