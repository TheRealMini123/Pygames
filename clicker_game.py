import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Clicker Game with Dark Theme")

# Colors
DARK_BG = (30, 30, 30)  # Dark background
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
GREEN = (34, 139, 34)
GREY = (105, 105, 105)
YELLOW = (255, 215, 0)
LIGHT_GREEN = (144, 238, 144)
HOVER_BLUE = (100, 150, 230)  # Hover color for the button
HOVER_GREEN = (175, 255, 175)  # Hover color for shop items

# Fonts
title_font = pygame.font.Font(None, 60)
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

# Button properties
click_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 100)

# Shop options (Scrollable)
shop_items = [
    {"name": "Upgrade +1 CPS", "cps": 1, "cost": 50},
    {"name": "Upgrade +5 CPS", "cps": 5, "cost": 200},
    {"name": "Golden Clicker +10 CPS", "cps": 10, "cost": 500},
    {"name": "Super Auto Clicker +50 CPS", "cps": 50, "cost": 2000},
    {"name": "Hyper Auto Clicker +100 CPS", "cps": 100, "cost": 5000},
    {"name": "Mega Clicker +200 CPS", "cps": 200, "cost": 10000},
    {"name": "Ultra Clicker +500 CPS", "cps": 500, "cost": 25000},
    {"name": "Infinity Clicker +1000 CPS", "cps": 1000, "cost": 50000},
]

# Shop layout and scrolling
shop_scroll = 0
shop_item_height = 60
shop_area_height = len(shop_items) * shop_item_height
shop_rect = pygame.Rect(50, 450, 400, HEIGHT - 500)

# Game variables
score = 0
clicks_per_second = 0

# Timer for automatic clicks
last_time = time.time()

# Draw the main click button with hover animation
def draw_click_button():
    mouse_pos = pygame.mouse.get_pos()
    is_hovering = click_button_rect.collidepoint(mouse_pos)
    
    # Change button color on hover
    button_color = HOVER_BLUE if is_hovering else BLUE
    pygame.draw.rect(screen, button_color, click_button_rect, border_radius=15)
    
    button_text = font.render("Click Me!", True, WHITE)
    screen.blit(button_text, (click_button_rect.x + 40, click_button_rect.y + 30))

# Draw shop options (with hover effects and scrolling)
def draw_shop():
    title_text = title_font.render("Shop Upgrades", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 380))

    # Draw shop scrollable area
    pygame.draw.rect(screen, DARK_BG, shop_rect)
    pygame.draw.rect(screen, GREY, shop_rect, width=2)

    # Start rendering shop items with hover effect
    for index, item in enumerate(shop_items):
        y = 450 + index * shop_item_height - shop_scroll
        if shop_rect.top <= y < shop_rect.bottom - shop_item_height:
            item_rect = pygame.Rect(50, y, 400, shop_item_height - 5)
            
            # Check if the mouse is hovering over the item
            is_hovering_item = item_rect.collidepoint(pygame.mouse.get_pos())
            item_color = HOVER_GREEN if is_hovering_item else LIGHT_GREEN

            # Draw the item with hover effect
            pygame.draw.rect(screen, item_color, item_rect, border_radius=10)
            text = small_font.render(f"{item['name']} - {item['cost']} pts", True, BLACK)
            screen.blit(text, (item_rect.x + 10, item_rect.y + 10))

# Display the score and CPS
def draw_score():
    score_text = title_font.render(f"Score: {score}", True, YELLOW)
    screen.blit(score_text, (10, 10))
    cps_text = font.render(f"CPS: {clicks_per_second}", True, WHITE)
    screen.blit(cps_text, (10, 70))

# Game loop
running = True
while running:
    # Background color
    screen.fill(DARK_BG)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if click_button_rect.collidepoint(event.pos):
                score += 1
            for index, item in enumerate(shop_items):
                y = 450 + index * shop_item_height - shop_scroll
                item_rect = pygame.Rect(50, y, 400, shop_item_height - 5)
                if item_rect.collidepoint(event.pos) and shop_rect.collidepoint(event.pos):
                    if score >= item["cost"]:
                        clicks_per_second += item["cps"]
                        score -= item["cost"]
                        item["cost"] = int(item["cost"] * 1.5)  # Increase cost
        if event.type == pygame.MOUSEWHEEL:
            # Only scroll if not interacting with the main click button
            if not click_button_rect.collidepoint(pygame.mouse.get_pos()):
                shop_scroll -= event.y * 20
                shop_scroll = max(0, min(shop_scroll, shop_area_height - shop_rect.height))

    # Automatic clicks based on CPS
    current_time = time.time()
    if current_time - last_time >= 1:
        score += clicks_per_second
        last_time = current_time

    # Draw UI elements
    draw_click_button()
    draw_shop()
    draw_score()

    # Refresh the display
    pygame.display.flip()

    # Frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()


