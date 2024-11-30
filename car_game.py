import pygame
import random

# Initialize Pygame
pygame.init()

# Set up fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Car Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Car settings (2x larger)
CAR_WIDTH, CAR_HEIGHT = 100, 160
car_image = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
car_image.fill(GREEN)  # Player is green

# Obstacle settings (2x larger)
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 100, 160
obstacle_image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
obstacle_image.fill(RED)  # Enemies are red

# Game variables
car_x = WIDTH // 2 - CAR_WIDTH // 2
car_y = HEIGHT - CAR_HEIGHT - 20
car_speed = 7

obstacles = []
obstacle_speed = 7
obstacle_spawn_timer = 0

score = 0
time_elapsed = 0

# Font
font = pygame.font.Font(None, 36)
win_font = pygame.font.Font(None, 72)  # Larger font for the win screen

# Function to draw score
def draw_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Function to display the win screen
def draw_win_screen():
    screen.fill(BLACK)  # Black background
    win_text = win_font.render("You Win!", True, WHITE)
    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - win_text.get_height() // 2))

# Function to check collision
def check_collision(car_rect, obstacles):
    for obstacle in obstacles:
        if car_rect.colliderect(obstacle):
            return True
    return False

# Main game loop
running = True
game_won = False
while running:
    if game_won:
        draw_win_screen()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        continue

    screen.fill(BLACK)  # Set background to black

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False  # Allow quitting with ESC key

    # Car movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < WIDTH - CAR_WIDTH:
        car_x += car_speed

    # Create obstacles
    obstacle_spawn_timer += 1
    if obstacle_spawn_timer > 50:  # Add a new obstacle more frequently
        obstacle_x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
        obstacles.append(pygame.Rect(obstacle_x, -OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        obstacle_spawn_timer = 0

    # Move obstacles
    for obstacle in obstacles:
        obstacle.y += obstacle_speed
    # Remove obstacles that are off-screen
    obstacles = [obstacle for obstacle in obstacles if obstacle.y < HEIGHT]

    # Check collision
    car_rect = pygame.Rect(car_x, car_y, CAR_WIDTH, CAR_HEIGHT)
    if check_collision(car_rect, obstacles):
        print("Game Over!")
        running = False

    # Update score every second
    time_elapsed += 1
    if time_elapsed >= FPS:  # Increment score every second
        score += 1
        time_elapsed = 0

    # Check if the player has won
    if score >= 30:
        game_won = True
        continue

    # Draw car
    screen.blit(car_image, (car_x, car_y))

    # Draw obstacles
    for obstacle in obstacles:
        screen.blit(obstacle_image, (obstacle.x, obstacle.y))

    # Draw score
    draw_score(score)

    # Update display and tick clock
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
