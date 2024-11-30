import pygame
import webbrowser
import sys
import os
import subprocess

# Initialize pygame
pygame.init()

# Set up the screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Geometry Dash Game")

# Load a professional font
font_path = pygame.font.get_default_font()  # Default font
font = pygame.font.Font(font_path, 36)
button_font = pygame.font.Font(font_path, 28)

# Game variables
html_file_path = "geometry_dash_game.html"

# Create a simple HTML file with Geometry Dash game
html_content = f"""
<html>
<head>
    <title>Geometry Dash Game</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #222222;
        }}
        canvas {{
            display: block;
            margin: 0 auto;
            background-color: #333;
        }}
        button {{
            padding: 15px 30px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 20px;
            cursor: pointer;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }}
        button:hover {{
            background-color: #45a049;
        }}
        button:active {{
            transform: translateY(2px);
        }}
    </style>
</head>
<body>
    <canvas id="gameCanvas"></canvas>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        canvas.width = {screen_width};
        canvas.height = {screen_height};

        // Game variables
        let player = {{ x: 50, y: canvas.height - 50, size: 50, velocityY: 0, gravity: 0.6, jumpStrength: -15, isJumping: false }};
        let platforms = [];
        let spikes = [];
        let score = 0;
        let gameOver = false;

        // Handle keypress (player jump)
        document.addEventListener('keydown', () => {{
            if (!gameOver && !player.isJumping) {{
                player.velocityY = player.jumpStrength;
                player.isJumping = true;
            }} else if (gameOver) {{
                resetGame();
            }}
        }});

        // Draw the player (block)
        function drawPlayer() {{
            player.velocityY += player.gravity;
            player.y += player.velocityY;

            if (player.y > canvas.height - player.size) {{
                player.y = canvas.height - player.size;
                player.velocityY = 0;
                player.isJumping = false;
            }}

            ctx.fillStyle = "cyan";
            ctx.fillRect(player.x, player.y, player.size, player.size);
        }}

        // Draw the platforms (rectangles)
        function drawPlatforms() {{
            for (let i = 0; i < platforms.length; i++) {{
                let platform = platforms[i];
                ctx.fillStyle = "green";
                ctx.fillRect(platform.x, platform.y, platform.width, platform.height);
                platform.x -= 6;  // Platforms move to the left

                // Remove platform when it goes off-screen
                if (platform.x + platform.width <= 0) {{
                    platforms.shift();
                    score++;
                }}

                // Collision detection for player landing on platform
                if (player.x + player.size > platform.x && player.x < platform.x + platform.width) {{
                    if (player.y + player.size <= platform.y && player.y + player.size + player.velocityY >= platform.y) {{
                        player.y = platform.y - player.size;  // Land on the platform
                        player.velocityY = 0;
                        player.isJumping = false;
                    }}
                }}
            }}
        }}

        // Draw the spikes (rectangles at the bottom of the canvas)
        function drawSpikes() {{
            for (let i = 0; i < spikes.length; i++) {{
                let spike = spikes[i];
                ctx.fillStyle = "red";
                ctx.fillRect(spike.x, spike.y, spike.width, spike.height);
                spike.x -= 8;  // Spikes move to the left

                // Remove spike when it goes off-screen
                if (spike.x + spike.width <= 0) {{
                    spikes.shift();
                }}

                // Collision detection with spikes
                if (player.x + player.size > spike.x && player.x < spike.x + spike.width) {{
                    if (player.y + player.size > spike.y) {{
                        gameOver = true;
                    }}
                }}
            }}
        }}

        // Generate new platforms
        function generatePlatforms() {{
            if (Math.random() < 0.02) {{
                let platformWidth = 150 + Math.random() * 100;
                let platformHeight = 40;
                let platformY = Math.random() * (canvas.height - 200) + 100;  // Random Y-position for platforms
                platforms.push({{ x: canvas.width, y: platformY, width: platformWidth, height: platformHeight }});
            }}
        }}

        // Generate new spikes at the bottom
        function generateSpikes() {{
            if (Math.random() < 0.01) {{
                let spikeWidth = 50;
                let spikeHeight = 60;
                let spikeY = canvas.height - spikeHeight;
                let spikeX = canvas.width;
                spikes.push({{ x: spikeX, y: spikeY, width: spikeWidth, height: spikeHeight }});
            }}
        }}

        // Draw score
        function drawScore() {{
            ctx.fillStyle = "white";
            ctx.font = "30px Arial";
            ctx.fillText("Score: " + score, 10, 30);
        }}

        // Reset the game
        function resetGame() {{
            player.y = canvas.height - player.size;
            player.velocityY = 0;
            player.isJumping = false;
            platforms = [];
            spikes = [];
            score = 0;
            gameOver = false;
        }}

        // Game loop
        function gameLoop() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            generatePlatforms();
            generateSpikes();
            drawPlatforms();
            drawSpikes();
            drawPlayer();
            drawScore();

            if (gameOver) {{
                ctx.fillStyle = "white";
                ctx.font = "50px Arial";
                ctx.fillText("Game Over!", canvas.width / 2 - 150, canvas.height / 2);
                ctx.fillText("Click to Restart", canvas.width / 2 - 190, canvas.height / 2 + 80);
            }} else {{
                requestAnimationFrame(gameLoop);
            }}
        }}

        gameLoop();
    </script>
</body>
</html>
"""

# Write the HTML content to the file
def create_html_file():
    try:
        with open(html_file_path, "w") as file:
            file.write(html_content)
        print(f"HTML file created successfully at: {html_file_path}")
    except Exception as e:
        print(f"Error creating HTML file: {e}")

    # Open the custom HTML page with the "Geometry Dash" game using subprocess to launch browser
    try:
        if sys.platform == 'win32':  # Windows
            subprocess.Popen(['start', 'chrome', f'file://{os.path.abspath(html_file_path)}'], shell=True)
        elif sys.platform == 'darwin':  # macOS
            subprocess.Popen(['open', '-a', 'Safari', f'file://{os.path.abspath(html_file_path)}'])
        else:  # Linux
            subprocess.Popen(['xdg-open', f'file://{os.path.abspath(html_file_path)}'])
    except Exception as e:
        print(f"Error opening browser: {e}")

# Function to delete HTML file when the program closes
def delete_html_file():
    if os.path.exists(html_file_path):
        os.remove(html_file_path)
        print(f"Deleted {html_file_path}")

# Main game loop for the Python side (displaying the game and then deleting the file)
running = True
game_won = False
start_time = None  # Variable to track when the webpage was opened
game_over_time = None  # Time when the game over happened

# Define button areas
start_button_rect = pygame.Rect((screen_width // 2 - 100, screen_height // 2 - 50, 200, 100))
close_button_rect = pygame.Rect((screen_width // 2 - 100, screen_height // 2 + 60, 200, 100))

start_button_color = (0, 128, 0)
close_button_color = (255, 0, 0)

start_button_text = button_font.render("Start Game", True, (255, 255, 255))
close_button_text = button_font.render("Close", True, (255, 255, 255))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            delete_html_file()  # Delete the HTML file when the program is closed
        
        # Check if the "Start Game" button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button_rect.collidepoint(event.pos):
                create_html_file()

        # Check if the "Close" button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if close_button_rect.collidepoint(event.pos):
                running = False
                delete_html_file()  # Delete the HTML file when closing the program

    # Fill the screen with a color (e.g., black)
    screen.fill((0, 0, 0))

    # Draw the buttons
    pygame.draw.rect(screen, start_button_color, start_button_rect)
    pygame.draw.rect(screen, close_button_color, close_button_rect)
    
    # Draw the button texts
    screen.blit(start_button_text, (start_button_rect.x + (start_button_rect.width - start_button_text.get_width()) // 2, 
                                    start_button_rect.y + (start_button_rect.height - start_button_text.get_height()) // 2))
    screen.blit(close_button_text, (close_button_rect.x + (close_button_rect.width - close_button_text.get_width()) // 2, 
                                    close_button_rect.y + (close_button_rect.height - close_button_text.get_height()) // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
