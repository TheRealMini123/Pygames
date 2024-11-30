import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Game settings
basket_width = 100
basket_height = 20
falling_speed = 5
score = 0
win_score = 20  # Score required to win

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Objects")

# Load assets
fruit_image = pygame.Surface((30, 30))
fruit_image.fill(RED)

basket_image = pygame.Surface((basket_width, basket_height))
basket_image.fill(GREEN)

# Basket class
class Basket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = basket_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 30)

    def update(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= 10
        if keys[pygame.K_d]:
            self.rect.x += 10
        # Keep the basket within the screen boundaries
        self.rect.x = max(0, min(WIDTH - basket_width, self.rect.x))

# Falling Object class (Fruit)
class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = fruit_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 30)
        self.rect.y = -30  # Start above the screen

    def update(self):
        self.rect.y += falling_speed
        if self.rect.y > HEIGHT:
            self.kill()  # Remove fruit if it goes off-screen

# Display score
def display_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Win screen
def win_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 72)
    win_text = font.render("YOU WIN!", True, GREEN)
    text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(win_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# Main game loop
def game_loop():
    global score
    basket = Basket()
    basket_group = pygame.sprite.Group(basket)
    fruits = pygame.sprite.Group()

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get key states
        keys = pygame.key.get_pressed()

        # Update basket and fruits
        basket_group.update(keys)

        # Spawn new fruits at random intervals
        if random.random() < 0.02:
            fruit = Fruit()
            fruits.add(fruit)

        # Update fruits
        fruits.update()

        # Check for collisions between basket and fruits
        caught_fruits = pygame.sprite.spritecollide(basket, fruits, True)
        for fruit in caught_fruits:
            score += 1  # Increase score for each caught fruit

        # Check if the player has won
        if score >= win_score:
            win_screen()

        # Draw everything
        basket_group.draw(screen)
        fruits.draw(screen)
        display_score()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Run the game
game_loop()
