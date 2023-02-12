import sys
import pygame
import random 

# Initialize Pygame
pygame.init()

# Set up game window
win_width = 800
win_height = 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Pong Game")

# Define menu function
def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        win.fill((0,0,0))
        font = pygame.font.Font(None, 64)
        title = font.render("Pong Game", True, (255, 255, 255))
        title_rect = title.get_rect(center=(win_width/2, win_height/2-50))
        instructions = font.render("Press Enter to Start", True, (255, 255, 255))
        instructions_rect = instructions.get_rect(center=(win_width/2, win_height/2+50))
        win.blit(title, title_rect)
        win.blit(instructions, instructions_rect)

        pygame.display.update()

# Run menu function
menu()

# Define game objects
ball = pygame.Rect(win_width/2-15, win_height/2-15, 30, 30)
player_paddle = pygame.Rect(50, win_height/2-70, 15, 140)
opponent_paddle = pygame.Rect(win_width-65, win_height/2-70, 15, 140)

# Define game variables
ball_speed_x = 7
ball_speed_y = 7
player_paddle_speed = 0
opponent_paddle_speed = 7 # decreased opponent speed
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 64)

# Load sounds
paddle_hit_sound = pygame.mixer.Sound("paddle_hit.wav")
win_sound = pygame.mixer.Sound("win.wav")
wah_sound = pygame.mixer.Sound("wah.wav")

#Variable to keep track of arrow keys that are currently pressed down

keys = set()

# Set up game loop
run = True
clock = pygame.time.Clock()
while run:
# Handle user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
# Add the pressed key to the set of keys
            keys.add(event.key)
        elif event.type == pygame.KEYUP:
# Remove the released key from the set of keys
            keys.discard(event.key)
    
# Update game state
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if pygame.K_UP in keys:
        player_paddle_speed = -7
    elif pygame.K_DOWN in keys:
        player_paddle_speed = 7
    else:
        player_paddle_speed = 0

    player_paddle.y += player_paddle_speed
    opponent_paddle.y += opponent_paddle_speed

    
    # Handle collision detection

    if ball.top <= 0 or ball.bottom >= win_height:
        ball_speed_y *= -1
    if ball.left <= 0:
        opponent_score += 1
        ball_speed_x *= -1
        ball.center = (win_width/2, win_height/2)
    if ball.right >= win_width:
        player_score += 1
        ball_speed_x *= -1
        ball.center = (win_width/2, win_height/2)
    if ball.colliderect(player_paddle):
        ball_speed_x *= -1
        paddle_hit_sound.play()
    if ball.colliderect(opponent_paddle):
        ball_speed_x *= -1
        paddle_hit_sound.play()

    
    # Handle paddle movement
    if player_paddle.top <= 0:
        player_paddle.top = 0
    if player_paddle.bottom >= win_height:
        player_paddle.bottom = win_height
    if opponent_paddle.top <= 0:
        opponent_paddle.top = 0
        opponent_paddle_speed = 5 # change direction
    if opponent_paddle.bottom >= win_height:
        opponent_paddle.bottom = win_height
        opponent_paddle_speed = -5 # change direction
    
    # Handle opponent paddle movement
    if opponent_paddle.top < ball.y:
        opponent_paddle.top += opponent_paddle_speed
    if opponent_paddle.bottom > ball.y:
        opponent_paddle.bottom -= opponent_paddle_speed

    # Draw game objects
    win.fill((0,0,0))
    pygame.draw.line(win, (255, 255, 255), (win_width/2, 0), (win_width/2, win_height), 3)
    pygame.draw.rect(win, (255, 255, 255), player_paddle)
    pygame.draw.rect(win, (255, 255, 255), opponent_paddle)
    pygame.draw.ellipse(win, (255, 255, 255), ball)
    
    # Draw score
    player_text = font.render(str(player_score), True, (255, 255, 255))
    opponent_text = font.render(str(opponent_score), True, (255, 255, 255))
    win.blit(player_text, (win_width/2-player_text.get_width()-10, 10))
    win.blit(opponent_text, (win_width/2+10, 10))
    
    # Display game screen
    pygame.display.flip()
    
    # Handle winning
    if player_score == 10:
        win_sound.play()
        win.fill((0,0,0))
        player_text = font.render("You Win!", True, (255, 255, 255))
        win.blit(player_text, (win_width/2-player_text.get_width()/2, win_height/2-player_text.get_height()/2))
        pygame.display.flip()
        pygame.time.delay(5000)
        run = False
    elif opponent_score == 10:
        wah_sound.play()
        win.fill((0,0,0))
        player_text = font.render("You Lose!", True, (255, 255, 255))
        win.blit(player_text, (win_width/2-player_text.get_width()/2, win_height/2-player_text.get_height()/2))
        pygame.display.flip()
        pygame.time.delay(5000)
        run = False
    
    # Set game speed
    clock.tick(60)

# Close game window
pygame.quit()