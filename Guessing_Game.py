import random
import pygame
import pygame.freetype

pygame.init()

screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Professional Guessing Game")

pygame.freetype.init()
title_font = pygame.freetype.SysFont("Arial", 36, bold=True)
label_font = pygame.freetype.SysFont("Arial", 24)
input_font = pygame.freetype.SysFont("Arial", 28)
button_font = pygame.freetype.SysFont("Arial", 20, bold=True)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 122, 204)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_RED = (255, 180, 180)
LIGHT_BLUE = (180, 200, 255)
LIGHT_GREEN = (180, 255, 180)
GRAY = (200, 200, 200)
LIGHT_GRAY = (220, 220, 220)

highest_score = None

def draw_text(text, font, position, color=BLACK):
    font.render_to(screen, position, text, color)

def reset_game():
    global number_to_guess, number_of_attempts, input_text, message, game_over, background_color
    number_to_guess = random.randint(1, 100)
    number_of_attempts = 0
    input_text = ""
    message = "Guess a number between 1 and 100"
    game_over = False
    background_color = WHITE

def draw_button(text, position, color):
    button_rect = pygame.Rect(position[0], position[1], 200, 50)
    pygame.draw.rect(screen, color, button_rect, border_radius=5)
    draw_text(text, button_font, (position[0] + (200 - button_font.get_rect(text).width) // 2, position[1] + 15), BLACK)
    return button_rect

def update_highest_score(attempts):
    global highest_score
    if highest_score is None or attempts < highest_score:
        highest_score = attempts

reset_game()

running = True
while running:
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_RETURN:
                try:
                    user_guess = int(input_text)
                    if user_guess < 1 or user_guess > 100:
                        message = "Please enter a number between 1 and 100."
                        background_color = LIGHT_GRAY
                    else:
                        number_of_attempts += 1
                        if user_guess < number_to_guess:
                            message = f"Too low! Attempts: {number_of_attempts}"
                            background_color = LIGHT_RED
                        elif user_guess > number_to_guess:
                            message = f"Too high! Attempts: {number_of_attempts}"
                            background_color = LIGHT_BLUE
                        else:
                            message = f"Correct! Number: {number_to_guess}. Attempts: {number_of_attempts}"
                            background_color = LIGHT_GREEN
                            update_highest_score(number_of_attempts)
                            game_over = True
                except ValueError:
                    message = "Please enter a valid number."
                    background_color = LIGHT_GRAY
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = event.pos
            if restart_button.collidepoint(mouse_pos):
                reset_game()

    draw_text("Guessing Game", title_font, (screen_width // 2 - title_font.get_rect("Guessing Game").width // 2, 30), BLUE)
    draw_text(message, label_font, (screen_width // 2 - label_font.get_rect(message).width // 2, 100), BLACK)
    
    input_box_width = 380
    input_box_rect = pygame.Rect(screen_width // 2 - input_box_width // 2, 160, input_box_width, 40)
    pygame.draw.rect(screen, LIGHT_GRAY, input_box_rect, border_radius=5)
    pygame.draw.rect(screen, BLACK, input_box_rect, 2, border_radius=5)
    draw_text(input_text, input_font, (screen_width // 2 - input_font.get_rect(input_text).width // 2, 170), BLACK)

    if highest_score is not None:
        draw_text(f"Highest Score: {highest_score} attempts", label_font, (screen_width // 2 - label_font.get_rect(f"Highest Score: {highest_score} attempts").width // 2, 220), BLUE)

    if game_over:
        restart_button = draw_button("Play Again", (screen_width // 2 - 100, 280), GRAY)
    
    pygame.display.flip()

pygame.quit()
