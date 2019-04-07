import pygame
import random
import math
import tkinter as tk
from tkinter import messagebox as ms
import sys

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
BLUE     = (0,   0, 255)

# --- Classes
class Block(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([20, 20])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        
        # The "center" the sprite will orbit
        self.center_x = 0
        self.center_y = 0

        # Current angle in radians
        self.angle =0.523599

        # How far away from the center to orbit, in pixels
        self.radius = 0

        # How fast to orbit, in radians per frame
        self.speed = 0.05
    def update(self):
        """ Update the ball's position. """
        # Calculate a new x, y
        self.rect.x = self.radius * math.sin(self.angle) + self.center_x
        self.rect.y = self.radius * math.cos(self.angle) + self.center_y

        # Increase the angle in prep for the next round.
        self.angle += self.speed


class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """

    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([20, 10])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Set the player x position to the mouse x position
        self.rect.x = pos[0]
        
class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([4, 10])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 3
# --- Create the window
# Initialize Pygame
pygame.init()
root=tk.Tk()
root.withdraw()
# Set the height and width of the screen
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])
back_image=pygame.image.load("saturn_family1.jpg").convert()
pygame.display.set_caption("Hit It :))")
# --- Sprite lists
font=pygame.font.SysFont("comicsans",30)
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

# List of each block in the game
block_list = pygame.sprite.Group()

# List of each bullet
bullet_list = pygame.sprite.Group()
start_ticks=pygame.time.get_ticks()

# --- Create the sprites
for i in range(70):
    # This represents a block    
    block = Block((i+50,i+3,(i+20)*2))
    # Set a random center location for the block to orbit
    block.center_x = random.randrange(screen_width)
    block.center_y = random.randrange(screen_width)
    # Random radius from 10 to 200
    block.radius = random.randrange(10, 200)
    # Random start angle from 0 to 2pi
    block.angle = random.random() * 2 * math.pi
    # radians per frame
    block.speed = 0.008
    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)   

# Create a red player block
player = Player()
all_sprites_list.add(player)
#Loop until the user clicks the close button.
run = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
score = 0
player.rect.y = 370

# -------- Main Program Loop -----------
while not run:
    # --- Event Processing
    seconds=(pygame.time.get_ticks()-start_ticks)/1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = True
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Fire a bullet if the user clicks the mouse button
            bullet = Bullet()
            # Set the bullet so it is where the player is
            bullet.rect.x = player.rect.x
            bullet.rect.y = player.rect.y
            # Add the bullet to the lists
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)
    # --- Game logic

    # Call the update() method on all the sprites
    all_sprites_list.update()
    
    # Calculate mechanics for each bullet
    for bullet in bullet_list:

        # See if it hit a block
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)

        # For each block hit, remove the bullet and add to the score
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
         #calculate how many seconds
        if seconds<30: # if more than 10 seconds close the game
            pass
        else:
            if ms.showinfo("End Of Game", "Upps!!! Game Over"):
                pygame.quit()
                run = True
                sys.exit()
        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
        
    # --- Draw a frame
        
    screen.blit(back_image,(0,0))
    # Draw all the spites
    all_sprites_list.draw(screen)
    text=font.render("Score="+str(score),1,(0,250,255))
    screen.blit(text,(0,0))
    text1=font.render("timer="+str(seconds),1,(0,255,255))
    screen.blit(text1,(650,0))
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 20 frames per second
    clock.tick(60)
pygame.quit()
