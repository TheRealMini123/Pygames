import pygame
import webbrowser
import sys
import os

# Initialize pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((600, 800))  # Increased screen size
pygame.display.set_caption("Flappy Bird Game")

# Game variables
font = pygame.font.Font(None, 36)
text = font.render("You Win!", True, (255, 255, 255))

# Path for the temporary HTML file
html_file_path = "flappy_bird_game.html"

# Create a simple HTML file with Flappy Bird game
html_content = """
<html>
<head>
    <title>Flappy Bird Game</title>
    <style>
        body { margin: 0; padding: 0; overflow: hidden; background-color: #70c5ce; }
        canvas { display: block; margin: 0 auto; }
    </style>
</head>
<body>
    <canvas id="gameCanvas"></canvas>
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        canvas.width = 600;  // Increased canvas width
        canvas.height = 800;  // Increased canvas height

        // Game variables
        let birdY = canvas.height / 2;
        let birdX = 50;
        let birdVelocity = 0;
        let gravity = 0.1;  // Gravity set to 0.1 for less bounce
        let jump = -4;  // Jump strength set to -4 for a moderate jump
        let isGameOver = false;
        let pipes = [];
        let pipeWidth = 50;
        let pipeGap = 200;  // Increased gap between pipes
        let pipeSpeed = 2;
        let score = 0;
        let pipeDelay = 5000;  // Delay for first pipe generation (5 seconds)
        let lastPipeTime = Date.now();
        
        // Bird image (Use a rectangle for simplicity)
        const birdWidth = 50;  // Increased bird size
        const birdHeight = 50;  // Increased bird size

        // Handle keypress (bird jump)
        document.addEventListener('keydown', () => {
            if (!isGameOver) {
                birdVelocity = jump;
            } else {
                resetGame();
            }
        });

        // Draw the bird
        function drawBird() {
            birdY += birdVelocity;
            birdVelocity += gravity;
            ctx.fillStyle = 'yellow';
            ctx.fillRect(birdX, birdY, birdWidth, birdHeight);
        }

        // Draw the pipes
        function drawPipes() {
            for (let i = 0; i < pipes.length; i++) {
                let pipe = pipes[i];
                ctx.fillStyle = "#009900";
                ctx.fillRect(pipe.x, 0, pipeWidth, pipe.topHeight);
                ctx.fillRect(pipe.x, pipe.bottomY, pipeWidth, canvas.height - pipe.bottomY);
                pipe.x -= pipeSpeed;

                if (pipe.x + pipeWidth <= 0) {
                    pipes.shift();
                    score++;
                }

                // Collision detection with pipes
                if (pipe.x <= birdX + birdWidth && pipe.x + pipeWidth >= birdX) {
                    if (birdY < pipe.topHeight || birdY + birdHeight > pipe.bottomY) {
                        isGameOver = true;
                    }
                }
            }
        }

        // Generate pipes with a delay
        function generatePipes() {
            if (Date.now() - lastPipeTime > pipeDelay) {
                let pipeHeight = Math.random() * (canvas.height - pipeGap);
                let topHeight = pipeHeight;
                let bottomY = pipeHeight + pipeGap;
                pipes.push({ x: canvas.width, topHeight, bottomY });
                pipes.push({ x: canvas.width + 300, topHeight, bottomY });  // Generate two pipes at once
                lastPipeTime = Date.now();
            }
        }

        // Draw score
        function drawScore() {
            ctx.fillStyle = "white";
            ctx.font = "30px Arial";
            ctx.fillText("Score: " + score, 10, 30);
        }

        // Reset the game
        function resetGame() {
            birdY = canvas.height / 2;
            birdVelocity = 0;
            pipes = [];
            score = 0;
            isGameOver = false;
            lastPipeTime = Date.now();  // Reset pipe timer
        }

        // Game loop
        function gameLoop() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            drawBird();
            generatePipes();
            drawPipes();
            drawScore();

            if (birdY + birdHeight > canvas.height) {
                isGameOver = true;
            }

            if (isGameOver) {
                ctx.fillStyle = "white";
                ctx.font = "50px Arial";
                ctx.fillText("Game Over!", 150, 350);  // Adjusted text position for bigger screen
                ctx.font = "30px Arial";
                ctx.fillText("Click to Restart", 180, 400);  // Adjusted text position for bigger screen
            } else {
                requestAnimationFrame(gameLoop);
            }
        }

        gameLoop();
    </script>
</body>
</html>
"""

# Write the HTML content to the file
with open(html_file_path, "w") as file:
    file.write(html_content)

# Main game loop for the Python side (displaying the game and then deleting the file)
running = True
game_won = False
start_time = None  # Variable to track when the webpage was opened

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Check if the user wins (e.g., pressing the spacebar)
        if not game_won and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_won = True
            # Open the custom HTML page with the "Flappy Bird" game
            webbrowser.open(f"file://{os.path.abspath(html_file_path)}")
            start_time = pygame.time.get_ticks()  # Record the time when the page is opened
            pygame.time.delay(1000)  # Wait for a second before continuing the loop

    # Fill the screen with a color (e.g., black)
    screen.fill((0, 0, 0))

    if game_won:
        # Display the win message on the screen
        screen.blit(text, (180, 280))

    pygame.display.flip()

    # Check if 3 seconds have passed after opening the webpage
    if game_won and start_time is not None and pygame.time.get_ticks() - start_time >= 3000:
        # Delete the HTML file after 3 seconds
        if os.path.exists(html_file_path):
            os.remove(html_file_path)
            print(f"Deleted {html_file_path}")

        # Close the Pygame window after a brief delay
        pygame.quit()
        sys.exit()
