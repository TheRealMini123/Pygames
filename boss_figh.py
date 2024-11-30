import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boss Fight Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.health = 100
        self.last_shot = 0
        self.score = 0

    def update(self, keys):
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= 5
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += 5
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += 5


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 100))
        pygame.draw.circle(self.image, RED, (50, 50), 50)
        self.rect = self.image.get_rect(center=(WIDTH // 2, 100))
        self.health = 200
        self.last_shot = 0

    def update(self):
        self.rect.x += random.choice([-3, 3])
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, color):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction

    def update(self):
        self.rect.y += self.direction * 10
        if not screen.get_rect().contains(self.rect):
            self.kill()


# Functions
def display_text(text, x, y, color=WHITE):
    screen.blit(font.render(text, True, color), (x, y))


def game_over_screen(win):
    screen.fill(BLACK)
    if win:
        text = "YOU WIN!"
    else:
        text = "GAME OVER!"
    screen.blit(big_font.render(text, True, WHITE), (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    display_text("Press ENTER to restart", WIDTH // 2 - 150, HEIGHT // 2 + 50, WHITE)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False


# Game setup
player = Player()
player_group = pygame.sprite.Group(player)

boss = Enemy()
enemy_group = pygame.sprite.Group(boss)

bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# Main game loop
running = True
while running:
    keys = pygame.key.get_pressed()
    screen.fill((30, 30, 30))  # Dark background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player shoots bullets
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pygame.time.get_ticks() - player.last_shot >= 500:
                bullet = Bullet(player.rect.centerx, player.rect.top, -1, GREEN)
                bullets.add(bullet)
                player.last_shot = pygame.time.get_ticks()

    # Enemy shoots bullets
    if pygame.time.get_ticks() - boss.last_shot >= 1000:
        enemy_bullet = Bullet(boss.rect.centerx, boss.rect.bottom, 1, RED)
        enemy_bullets.add(enemy_bullet)
        boss.last_shot = pygame.time.get_ticks()

    # Update game objects
    player.update(keys)
    boss.update()
    bullets.update()
    enemy_bullets.update()

    # Check bullet collisions
    for bullet in bullets:
        if boss.rect.colliderect(bullet.rect):
            bullet.kill()
            boss.health -= 10
            if boss.health <= 0:
                running = False
                game_over_screen(True)

    for enemy_bullet in enemy_bullets:
        if player.rect.colliderect(enemy_bullet.rect):
            enemy_bullet.kill()
            player.health -= 10
            if player.health <= 0:
                running = False
                game_over_screen(False)

    # Draw everything
    player_group.draw(screen)
    enemy_group.draw(screen)
    bullets.draw(screen)
    enemy_bullets.draw(screen)

    # Display HUD
    display_text(f"Player Health: {player.health}", 10, 10, GREEN)
    display_text(f"Boss Health: {boss.health}", 10, 40, RED)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
