import pygame
import random
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Pro")

clock = pygame.time.Clock()

# Load Images
bg = pygame.image.load("background.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (40, 40))

pipe_img = pygame.image.load("pipe.png")
pipe_img = pygame.transform.scale(pipe_img, (60, 400))

# Bird
bird_x = 80
bird_y = 300
velocity = 0
gravity = 0.5
jump = -8

# Pipes
pipe_width = 60
pipe_gap = 150
pipes = []

# Score
score = 0
high_score = 0
font = pygame.font.SysFont("Arial", 30)

def reset_game():
    global bird_y, velocity, pipes, score
    bird_y = 300
    velocity = 0
    pipes = []
    score = 0

def draw_bird():
    rotated = pygame.transform.rotate(bird_img, -velocity * 3)
    screen.blit(rotated, (bird_x, int(bird_y)))

def create_pipe():
    height = random.randint(150, 400)
    pipes.append([WIDTH, height])

def move_pipes():
    for pipe in pipes:
        pipe[0] -= 3

def draw_pipes():
    for pipe in pipes:
        # Top pipe (flipped)
        top_pipe = pygame.transform.flip(pipe_img, False, True)
        screen.blit(top_pipe, (pipe[0], pipe[1] - 400))
        # Bottom pipe
        screen.blit(pipe_img, (pipe[0], pipe[1] + pipe_gap))

def check_collision():
    if bird_y <= 0 or bird_y + 40 >= HEIGHT:
        return True

    for pipe in pipes:
        if pipe[0] < bird_x + 40 and pipe[0] + pipe_width > bird_x:
            if bird_y < pipe[1] or bird_y + 40 > pipe[1] + pipe_gap:
                return True
    return False

def show_text(text, size, x, y):
    font_obj = pygame.font.SysFont("Arial", size)
    render = font_obj.render(text, True, (255, 255, 255))
    screen.blit(render, (x, y))

# Game states
game_active = False

# Main Loop
while True:
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    velocity = jump
                else:
                    game_active = True
                    reset_game()

    if game_active:
        # Bird movement
        velocity += gravity
        bird_y += velocity

        # Pipes
        if len(pipes) == 0 or pipes[-1][0] < WIDTH - 200:
            create_pipe()

        move_pipes()
        draw_pipes()

        # Score
        for pipe in pipes:
            if pipe[0] == bird_x:
                score += 1

        # Remove off-screen pipes
        pipes = [p for p in pipes if p[0] > -pipe_width]

        draw_bird()

        # Collision
        if check_collision():
            game_active = False
            if score > high_score:
                high_score = score

        show_text(f"Score: {score}", 30, 10, 10)

    else:
        show_text("Flappy Bird", 40, 90, 200)
        show_text("Press SPACE to Start", 25, 70, 300)
        show_text(f"High Score: {high_score}", 25, 90, 350)

    pygame.display.update()
    clock.tick(60)
