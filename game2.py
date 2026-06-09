import pygame
import random
import sys
import os

# Initialize mixer before pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Base path for assets
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def load_image(filename, size=None):
    path = os.path.join(BASE_PATH, filename)
    image = pygame.image.load(path).convert_alpha()
    if size:
        image = pygame.transform.scale(image, size)
    return image

def load_sound(filename):
    path = os.path.join(BASE_PATH, filename)
    return pygame.mixer.Sound(path)

# Screen setup
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Pro")
clock = pygame.time.Clock()

# Load Images
bg = load_image("background.png", (WIDTH, HEIGHT))
bird_img = load_image("bird.png", (40, 40))
pipe_img = load_image("pipe.png", (60, 400))

# Load Sounds
try:
    pygame.mixer.music.load(os.path.join(BASE_PATH, "background.mp3"))
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)  # Loop forever

    jump_sound = load_sound("jump.wav")
    hit_sound = load_sound("hit.wav")
    jump_sound.set_volume(0.6)
    hit_sound.set_volume(0.7)
except pygame.error:
    print("Audio files not found or audio device unavailable.")
    jump_sound = None
    hit_sound = None

# Bird properties
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
        top_pipe = pygame.transform.flip(pipe_img, False, True)
        screen.blit(top_pipe, (pipe[0], pipe[1] - 400))
        screen.blit(pipe_img, (pipe[0], pipe[1] + pipe_gap))

def check_collision():
    if bird_y <= 0 or bird_y + 40 >= HEIGHT:
        return True

    for pipe in pipes:
        if pipe[0] < bird_x + 40 and pipe[0] + pipe_width > bird_x:
            if bird_y < pipe[1] or bird_y + 40 > pipe[1] + pipe_gap:
                return True
    return False

def show_text(text, size, x, y, color=(255, 255, 255)):
    font_obj = pygame.font.SysFont("Arial", size)
    render = font_obj.render(text, True, color)
    screen.blit(render, (x, y))

# Game state
game_active = False

# Main loop
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
                    if jump_sound:
                        jump_sound.play()
                else:
                    game_active = True
                    reset_game()

    if game_active:
        # Bird movement
        velocity += gravity
        bird_y += velocity

        # Pipe generation
        if len(pipes) == 0 or pipes[-1][0] < WIDTH - 200:
            create_pipe()

        move_pipes()
        draw_pipes()

        # Update score
        for pipe in pipes:
            if pipe[0] == bird_x:
                score += 1

        # Remove off-screen pipes
        pipes = [p for p in pipes if p[0] > -pipe_width]

        draw_bird()

        # Collision detection
        if check_collision():
            if hit_sound:
                hit_sound.play()
            pygame.time.delay(500)
            game_active = False
            if score > high_score:
                high_score = score

        show_text(f"Score: {score}", 30, 10, 10)

    else:
        show_text("Flappy Bird", 40, 100, 200)
        show_text("Press SPACE to Start", 25, 70, 300)
        show_text(f"High Score: {high_score}", 25, 90, 350)

    pygame.display.update()
    clock.tick(60)
