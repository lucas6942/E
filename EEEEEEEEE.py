import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Set the window size and title
win_width = 800
win_height = 600
window = pygame.display.set_mode((win_width, win_height), pygame.FULLSCREEN)
pygame.display.set_caption("Walk To school in ohio")

# Set the font
font = pygame.font.SysFont(None, 30)

# Set the colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

# Load the player and obstacle images
player_img = pygame.image.load("Ohio.png")
obstacle_img = pygame.image.load("Obstacle.png")

# Set the player properties
player_width = 50
player_height = 200
player_x = win_width / 2 - player_width / 2
player_y = win_height - player_height - 10
player_speed = 1
player_health = 100

# Set the obstacle properties
obstacle_width = 50
obstacle_height = 50
obstacle_speed = 1
obstacle_gap = 2000
obstacle_spawn_rate = 1000
obstacles = []

# Set the score
score = 0

# Set the game over properties
game_over = False
game_over_text = font.render("Your a Facking failure when i was kid,i had to fight two lions to school", True, red)
game_over_text_rect = game_over_text.get_rect(center=(win_width / 2, win_height / 3))

# Set menu properties
menu = True
menu_options = ['Level 1', 'Level 2', 'Level 3']
menu_option_selected = 0

# Set level properties
level = 1
level_images = ['level1.png', 'level2.png', 'level3.png']
level_image = pygame.image.load(level_images[level - 1])
level_obstacle_spawn_rate = [1000, 800, 600][level - 1]
level_obstacle_speed = [1, 2, 3][level - 1]

# Set play again properties
play_again = False

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if menu:
                if event.key == pygame.K_DOWN:
                    menu_option_selected = (menu_option_selected + 1) % len(menu_options)
                elif event.key == pygame.K_UP:
                    menu_option_selected = (menu_option_selected - 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if menu_options[menu_option_selected] == 'Level 1':
                        level = 1
                        level_image = pygame.image.load(level_images[level - 1])
                        level_obstacle_spawn_rate = [1000, 800, 600][level - 1]
                        level_obstacle_speed = [1, 2, 3][level - 1]
                        menu = False
                    elif menu_options[menu_option_selected] == 'Level 2':
                        level = 2
                        level_image = pygame.image.load(level_images[level - 1])
                        level_obstacle_spawn_rate = [1000, 800, 600][level - 1]
                        level_obstacle_speed = [1, 2, 3][level - 1]
                        menu = False
                    elif menu_options[menu_option_selected] == 'Level 3':
                        level = 3
                        level_image = pygame.image.load(level_images[level - 1])
                        level_obstacle_spawn_rate = [1000, 800, 600][level - 1]
                        level_obstacle_speed = [1, 2, 3][level - 1]
                        menu = False
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_MINUS:
                menu = True
                play_again = False
                score = 0
                player_health = 100
                obstacles.clear()

    if not menu:
        # Move the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < win_width - player_width:
            player_x += player_speed

        # Spawn obstacles
        if random.randint(1, level_obstacle_spawn_rate) == 1:
            obstacle_x = random.randint(0, win_width - obstacle_width)
            obstacle_y = -obstacle_height - obstacle_gap
            obstacles.append(pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height))

        # Move obstacles
        for obstacle in obstacles:
            obstacle.move_ip(0, level_obstacle_speed)
            if obstacle.bottom >= player_y and obstacle.left <= player_x + player_width and obstacle.right >= player_x:
                player_health -= 10
                obstacles.remove(obstacle)
            elif obstacle.top >= win_height:
                obstacles.remove(obstacle)
                score += 1

        # Update the health bar
        health_bar_width = player_health
        if health_bar_width < 0:
            health_bar_width = 0
            game_over = True
        health_bar_text = font.render("Health: {}".format(player_health), True, white)
        health_bar_text_rect = health_bar_text.get_rect(center=(win_width / 2, 20))
        health_bar = pygame.Rect(0, 0, health_bar_width, 10)
        health_bar.x = win_width / 2 - health_bar.width / 2
        health_bar.y = 40

        # Draw the game
        window.fill(black)
        window.blit(level_image, (0, 0))
        window.blit(player_img, (player_x, player_y))
        pygame.draw.rect(window, white, health_bar)
        window.blit(health_bar_text, health_bar_text_rect)
        for obstacle in obstacles:
            window.blit(obstacle_img, obstacle)
        score_text = font.render("Score: {}".format(score), True, white)
        score_text_rect = score_text.get_rect(center=(win_width / 2, win_height - 20))
        window.blit(score_text, score_text_rect)

        # Draw the game over screen if game over
        if game_over:
            game_over_text_rect = game_over_text.get_rect(center=(win_width / 2, win_height / 2))
            window.blit(game_over_text, game_over_text_rect)
            play_again_text = font.render("Press ESC or - to play again", True, white)
            play_again_text_rect = play_again_text.get_rect(center=(win_width / 2, win_height / 2 + 50))
            window.blit(play_again_text, play_again_text_rect)
            play_again = True

    # Draw the menu screen if menu
    if menu:
        menu_text = font.render('Select level:', True, white)
        menu_text_rect = menu_text.get_rect(center=(win_width / 2, win_height / 3))
        window.blit(menu_text, menu_text_rect)
        for i, option in enumerate(menu_options):
            option_text = font.render(option, True, white if i != menu_option_selected else green)
            option_text_rect = option_text.get_rect(center=(win_width / 2, win_height / 3 + 30 * (i + 1)))
            window.blit(option_text, option_text_rect)

    # Handle play again button
    if play_again:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] or keys[pygame.K_MINUS]:
            menu = True
            play_again = False
            score = 0
            player_health = 100
            obstacles.clear()

    # Update the display
    pygame.display.update()

# Quit pygame
pygame.quit()