import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Flappy Block")  # Set the window title to "Flappy Block"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 177, 76)
BLUE = (135, 206, 235)
RED = (255, 0, 0)
HOVER_COLOR = (255, 255, 150)  # Less saturated yellow
STAR_COLOR = (255, 255, 255)  # White for the stars

# Game settings
gravity = 1.4  # Adjusted for larger bird
bird_flap_strength = -16  # Adjusted for larger bird
bird_width = 60  # 2x original size
bird_height = 60  # 2x original size
pipe_width = 100  # 2x original size
pipe_gap = 300  # 2x original gap size
pipe_velocity = 6  # Adjusted for larger elements
font = pygame.font.SysFont("Arial", 60)  # Scaled font for fullscreen
win_font = pygame.font.SysFont("Arial", 120)  # Scaled font for "You Win!"
menu_font = pygame.font.SysFont("Arial", 80)  # Font for the main menu

# Star class
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.randint(1, 3)  # Randomize star size
        self.speed = random.uniform(0.1, 0.5)  # Randomize fall speed

    def move(self):
        self.y += self.speed  # Move the star down slowly
        if self.y > HEIGHT:
            self.y = -self.size  # Wrap the star to the top if it reaches the bottom

    def draw(self, screen):
        pygame.draw.circle(screen, STAR_COLOR, (self.x, int(self.y)), self.size)

# Bird class
class Bird:
    def __init__(self):
        self.x = WIDTH // 4
        self.y = HEIGHT // 2
        self.width = bird_width
        self.height = bird_height
        self.velocity = 0
        self.angle = 0

    def flap(self):
        self.velocity = bird_flap_strength

    def move(self, noclip=False):
        if noclip:
            return  # No movement if in noclip mode
        
        self.velocity += gravity
        self.y += self.velocity

        # Update rotation angle
        if self.velocity < 0:
            self.angle = max(-45, self.angle - 5)
        elif self.velocity > 0:
            self.angle = min(45, self.angle + 5)

        # Prevent bird from going out of bounds
        if self.y <= 0:
            self.y = 0
        if self.y + self.height >= HEIGHT:
            self.y = HEIGHT - self.height

    def draw(self, screen):
        bird_surface = pygame.Surface((self.width, self.height))
        bird_surface.fill(RED)
        rotated_bird = pygame.transform.rotate(bird_surface, self.angle)
        rotated_rect = rotated_bird.get_rect(center=(self.x, self.y))
        screen.blit(rotated_bird, rotated_rect)

# Pipe class
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(200, HEIGHT - pipe_gap - 200)
        self.width = pipe_width
        self.gap = pipe_gap

    def move(self):
        self.x -= pipe_velocity

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + self.gap, self.width, HEIGHT - (self.height + self.gap)))

    def off_screen(self):
        return self.x + self.width < 0

    def collide(self, bird):
        if bird.x + bird.width > self.x and bird.x < self.x + self.width:
            if bird.y < self.height or bird.y + bird.height > self.height + self.gap:
                return True
        return False

# Scrolling Background class
class ScrollingBackground:
    def __init__(self):
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.fill(BLUE)  # You can customize the color or texture here
        self.y1 = 0
        self.y2 = -HEIGHT  # Initially place the second background image off-screen

    def update(self):
        # Move the backgrounds down
        self.y1 += 1
        self.y2 += 1

        # Reset the background position when it moves off-screen
        if self.y1 >= HEIGHT:
            self.y1 = -HEIGHT
        if self.y2 >= HEIGHT:
            self.y2 = -HEIGHT

    def draw(self, screen):
        screen.blit(self.background, (0, self.y1))
        screen.blit(self.background, (0, self.y2))

# Main menu screen
def main_menu():
    menu_running = True
    play_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 60, 300, 80)
    test_button_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 60, 300, 80)

    while menu_running:
        screen.fill(BLACK)

        # Draw title
        title_text = menu_font.render("Flappy Block", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        # Draw Play and Test buttons with hover effects
        play_color = HOVER_COLOR if play_button_rect.collidepoint(pygame.mouse.get_pos()) else (50, 50, 50)
        test_color = HOVER_COLOR if test_button_rect.collidepoint(pygame.mouse.get_pos()) else (50, 50, 50)

        pygame.draw.rect(screen, play_color, play_button_rect, border_radius=20)
        pygame.draw.rect(screen, test_color, test_button_rect, border_radius=20)

        # Button text
        play_text = menu_font.render("Play", True, WHITE)
        test_text = menu_font.render("Test (Noclip)", True, WHITE)

        screen.blit(play_text, (play_button_rect.centerx - play_text.get_width() // 2, play_button_rect.centery - play_text.get_height() // 2))
        screen.blit(test_text, (test_button_rect.centerx - test_text.get_width() // 2, test_button_rect.centery - test_text.get_height() // 2))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return "play"
                if test_button_rect.collidepoint(event.pos):
                    return "test"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Allow ESC to quit the game
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

# Main game function
def game(mode="play"):
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    clock = pygame.time.Clock()

    # Initialize the scrolling background
    scrolling_bg = ScrollingBackground()  

    # Initialize stars
    stars = [Star() for _ in range(50)]  # Create 50 stars

    running = True
    while running:
        scrolling_bg.update()  # Update the background position
        scrolling_bg.draw(screen)  # Draw the scrolling background

        # Move and draw the stars
        for star in stars:
            star.move()
            star.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
                if event.key == pygame.K_ESCAPE:  # Allow ESC to quit the game
                    pygame.quit()
                    sys.exit()

        bird.move(noclip=(mode == "test"))

        # Move pipes and add new ones
        for pipe in pipes[:]:
            pipe.move()
            if pipe.off_screen():
                pipes.remove(pipe)
                pipes.append(Pipe())
                score += 1

            if pipe.collide(bird) and mode != "test":
                running = False

            pipe.draw(screen)

        bird.draw(screen)

        # Display the score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH - score_text.get_width() - 20, 20))

        # Check if the player wins
        if score >= 10:
            screen.fill(BLACK)
            win_text = win_font.render("You Win!", True, WHITE)
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 30))
            pygame.display.update()
            pygame.time.delay(2000)
            running = False

        pygame.display.update()
        clock.tick(60)

    # Game Over screen if player loses
    if score < 10:
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 30))
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + 30))
        pygame.display.update()
        pygame.time.delay(2000)

    pygame.quit()
    sys.exit()

# Start the game
if __name__ == "__main__":
    mode = main_menu()  # Show the main menu and get the selected mode
    game(mode)  # Start the game with the selected mode
