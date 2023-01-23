# Import necessary libraries
import pygame
import random
import time
from pygame.locals import *
from pygame.locals import (RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT)

# Define constants and variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 771
GAME_NAME = "Racer MIN302"
GAME_ICON = "pngeggg.png"
BACKGROUNG = pygame.image.load("3-lane_interstate_highway_road.png")

# Initialize the game variables
score = 0
start_time = time.time()

# Load the button images
play_image = pygame.image.load("play.png")
exit_image = pygame.image.load("exit.png")

# Get the button rects
play_rect = play_image.get_rect()
exit_rect = exit_image.get_rect()

# Set the position of the buttons
play_rect.x = 300
play_rect.y = 250
exit_rect.x = 400
exit_rect.y = 250

# Define player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("pngeggg.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.center = (406, SCREEN_HEIGHT)

    # Define movements based on keypress
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 10)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)
        
        # Keep the player on the screen
        if self.rect.left < 170:
            self.rect.left = 170
        elif self.rect.right > 628:
            self.rect.right = 628
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define car class
class Car(pygame.sprite.Sprite):
    def __init__(self):
        super(Car, self).__init__()
        self.surf = pygame.image.load("pngegg_11.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)

        # Define random positions and speeds
        position = [240,406]
        self.rect = self.surf.get_rect(
            center = (
                random.choice(position),
                random.randint(-500, -20)
            )
        )
        self.speed = random.randint(2, 4)

    # Move and remove the enemies
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > SCREEN_HEIGHT+200:
            self.kill()


# Define bus class
class Bus(pygame.sprite.Sprite):
    def __init__(self):
        super(Bus, self).__init__()
        self.surf = pygame.image.load("pngegg_22.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)

        # Define random positions and speeds
        position = [406,560]
        self.rect = self.surf.get_rect(
            center = (
                random.choice(position),
                random.randint(-1200, -30)
            )
        )
        self.speed = random.randint(1,1)

    # Move and remove the clouds
    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > SCREEN_HEIGHT+200:
            self.kill()

# Setup for sounds
pygame.mixer.init()

# Initialize pygame
pygame.init()

# Setup a clock for frame rate
clock = pygame.time.Clock()

# Create screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define game name and icon
pygame.display.set_caption(GAME_NAME)
game_icon = pygame.image.load(GAME_ICON)
pygame.display.set_icon(game_icon)

# Create custom events for adding a new enemy and cloud
ADD_CAR = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_CAR, 10000)
ADD_BUS = pygame.USEREVENT
pygame.time.set_timer(ADD_BUS, 10000)

# Create Player
player = Player()

# Create groups to hold elements sprite
cars = pygame.sprite.Group()
buss = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Load all sounds files
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops = -1)
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

# Set the base volume for the all sounds
move_up_sound.set_volume(0.5)
move_down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)

# Define the variable for game loop
is_running = True

# Function to display game over message
def game_over():
    """The function game_over is called when the player dies, which happens when the player rect and the enemy rect are overlapping (colliding)."""
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(text, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    text = font.render("Score: " + str(score), True, (255, 0, 0))
    screen.blit(text, (250, 200))
    screen.blit(play_image, play_rect)
    screen.blit(exit_image, exit_rect)
    player.kill
    cars.empty()
    buss.empty()
    move_down_sound.stop()
    move_up_sound.stop()
    collision_sound.stop()
    pygame.display.flip()


# Define the main loop
while is_running:

    # Loop for every event in queue
    for event in pygame.event.get():

        # User pressed any button
        if event.type == KEYDOWN:
            # Exit if user press the Esc button
            if event.type == K_ESCAPE:
                is_running = False

        # Exit from game if user press the exit button
        elif event.type == QUIT:
            is_running = False

        # Add new car
        elif event.type == ADD_CAR:
            new_car = Car()
            cars.add(new_car)
            all_sprites.add(new_car)

        # Add new bus
        elif event.type == ADD_BUS:
            new_bus = Bus()
            buss.add(new_bus)
            all_sprites.add(new_bus)

    # Get the set of the keys pressed
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the position of the cars and buses
    cars.update()
    buss.update()

    # Create the road
    screen.fill((0,0,0))
    screen.blit(BACKGROUNG,(0,0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemy has collided with the player
    if pygame.sprite.spritecollideany(player, cars):
        game_over()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the play button is clicked
            if play_rect.collidepoint(event.pos):
                player.alive()
                cars.update()
                buss.update()
                score = 0
                start_time = time.time()
            else:
                # Stop the main loop
                is_running = False

    elif pygame.sprite.spritecollideany(player, buss):
        game_over()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the play button is clicked
            if play_rect.collidepoint(event.pos):
                player.alive()
                cars.update()
                buss.update()
                score = 0
                start_time = time.time()
            else:
                # Stop the main loop
                is_running = False

    # Update the score based on the elapsed time
    elapsed_time = time.time() - start_time
    score = int(elapsed_time * 5)

    # Draw the score on the screen
    font = pygame.font.Font(None, 40)
    text = font.render("Score: " + str(score), True, (10, 50, 200))
    screen.blit(text, (10, 10))

    # Flip all event to the display
    pygame.display.flip()

    # Set 30 frames per second rate
    clock.tick(35)

# Stop the music mixer
pygame.mixer.music.stop()
pygame.mixer.quit()

# Exit from game
pygame.quit()
