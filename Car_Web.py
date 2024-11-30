import pygame
import sys
import os
import subprocess

# Initialize pygame
pygame.init()

# Set up the screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Game Menu")

# Load a professional font
font_path = pygame.font.get_default_font()  # Default font
button_font = pygame.font.Font(font_path, 28)

# Game variables
html_file_path = "car_game.html"

# HTML5/JavaScript content for the car game with updated colors and shapes
html_content = f"""
<html>
<head>
    <title>Car Game</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #1e1e1e;
        }}
        canvas {{
            display: block;
            margin: 0 auto;
            background-color: #444;
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
        let car = {{ x: canvas.width / 2 - 25, y: canvas.height - 100, width: 50, height: 80, velocityX: 0 }};
        let obstacles = [];
        let obstacleSpeed = 5;
        let score = 0;
        let gameOver = false;
        let gameWon = false;

        const maxSpeed = 8; // Maximum speed
        const acceleration = 0.3; // Acceleration rate
        const friction = 0.1; // Friction deceleration

        // Player controls
        const keys = {{ ArrowLeft: false, ArrowRight: false }};

        document.addEventListener('keydown', (e) => {{
            if (keys.hasOwnProperty(e.key)) keys[e.key] = true;
            if (gameOver && e.key === 'r') resetGame(); // Reset on 'R'
            if (gameWon && e.key === 'r') resetGame(); // Reset if the game is won
        }});
        document.addEventListener('keyup', (e) => {{
            if (keys.hasOwnProperty(e.key)) keys[e.key] = false;
        }});

        // Draw the player's car
        function drawCar() {{
            // Apply acceleration or deceleration based on key presses
            if (keys.ArrowLeft) car.velocityX = Math.max(car.velocityX - acceleration, -maxSpeed);
            if (keys.ArrowRight) car.velocityX = Math.min(car.velocityX + acceleration, maxSpeed);

            // Apply friction to gradually reduce speed when no keys are pressed
            if (!keys.ArrowLeft && !keys.ArrowRight) {{
                if (car.velocityX > 0) car.velocityX = Math.max(car.velocityX - friction, 0);
                if (car.velocityX < 0) car.velocityX = Math.min(car.velocityX + friction, 0);
            }}

            // Update car position
            car.x += car.velocityX;

            // Prevent car from going out of bounds
            if (car.x < 0) car.x = 0;
            if (car.x > canvas.width - car.width) car.x = canvas.width - car.width;

            // Draw the player car
            ctx.fillStyle = "green";
            ctx.fillRect(car.x, car.y, car.width, car.height);
        }}

        // Generate and move obstacles
        function drawObstacles() {{
            if (Math.random() < 0.03) {{
                let obsX = Math.random() * (canvas.width - car.width);
                obstacles.push({{ x: obsX, y: -car.height, width: car.width, height: car.height }});
            }}

            for (let i = 0; i < obstacles.length; i++) {{
                let obs = obstacles[i];
                obs.y += obstacleSpeed;

                // Collision detection
                if (
                    car.x < obs.x + obs.width &&
                    car.x + car.width > obs.x &&
                    car.y < obs.y + obs.height &&
                    car.y + car.height > obs.y
                ) {{
                    gameOver = true;
                }}

                // Draw obstacle
                ctx.fillStyle = "red";
                ctx.fillRect(obs.x, obs.y, obs.width, obs.height);

                // Remove off-screen obstacles
                if (obs.y > canvas.height) {{
                    obstacles.splice(i, 1);
                    score++;
                }}
            }}
        }}

        // Display score
        function drawScore() {{
            ctx.fillStyle = "white";
            ctx.font = "20px Arial";
            ctx.fillText("Score: " + score, 10, 30);
        }}

        // Display Game Over
        function drawGameOver() {{
            ctx.fillStyle = "white";
            ctx.font = "40px Arial";
            ctx.fillText("Game Over!", canvas.width / 2 - 100, canvas.height / 2 - 20);
            ctx.font = "20px Arial";
            ctx.fillText("Press R to Restart", canvas.width / 2 - 100, canvas.height / 2 + 30);
        }}

        // Display You Win screen
        function drawYouWin() {{
            ctx.fillStyle = "green";
            ctx.font = "60px Arial";
            ctx.fillText("You Win!", canvas.width / 2 - 150, canvas.height / 2 - 20);
            ctx.font = "20px Arial";
            ctx.fillText("Press R to Restart", canvas.width / 2 - 100, canvas.height / 2 + 30);
        }}

        // Reset game
        function resetGame() {{
            car.x = canvas.width / 2 - car.width / 2;
            car.y = canvas.height - car.height - 20;
            car.velocityX = 0;
            obstacles = [];
            score = 0;
            gameOver = false;
            gameWon = false;
        }}

        // Game loop
        function gameLoop() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            if (gameWon) {{
                drawYouWin();
            }} else if (!gameOver) {{
                drawCar();
                drawObstacles();
                drawScore();

                if (score >= 50) {{
                    gameWon = true;
                }}
            }} else {{
                drawGameOver();
            }}

            requestAnimationFrame(gameLoop);
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

    # Open the custom HTML page with the car game using subprocess to launch browser
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

# Main game loop for the Python side (displaying the menu and launching the game)
running = True

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
