import pygame
import random
import simpleaudio as sa

food_sound = sa.WaveObject.from_wave_file("sounds/food_sound.wav")

pygame.init()

green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (255, 255, 0)

window_width = 400
window_height = 300

dis = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

snake_speed_normal = 10
snake_speed_boost = 30
snake_speed = snake_speed_normal
snake_block = 10

font_style = pygame.font.SysFont(None, 25, True)


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [window_width / 6, window_height / 3])


def end_game():
    dis.fill(black)
    message("You Lost! Press C-Play Again or Q-Quit", red)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_c:
                    game()


def draw_snake(snake_list):
    for snake in snake_list:
        pygame.draw.rect(dis, green, [snake[0], snake[1], snake_block, snake_block])


def display_score(score):
    value = font_style.render("Your Score: " + str(score), True, blue)
    dis.blit(value, [0, 0])


def randomizer(food, blitz, food_x, food_y, blitz_x, blitz_y):
    if food:
        food_x = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
        food_y = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0
    if blitz:
        blitz_x = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
        blitz_y = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0

    while blitz_x == food_x and blitz_y == food_y:
        if food:
            food_x = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0
        if blitz:
            blitz_x = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
            blitz_y = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0
    return food_x, food_y, blitz_x, blitz_y


def game():
    global snake_speed
    x_pos_change, y_pos_change = 0, 0
    x_pos = window_width / 2
    y_pos = window_height / 2

    food_x, food_y, blitz_x, blitz_y = 0, 0, 0, 0
    food_x, food_y, blitz_x, blitz_y = randomizer(True, True, food_x, food_y, blitz_x, blitz_y)

    snake_length = 1
    snake_list = []

    timer = 50
    active_blitz = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x_pos_change == snake_block and snake_length > 2:
                        continue
                    x_pos_change = -snake_block
                    y_pos_change = 0
                elif event.key == pygame.K_RIGHT:
                    if x_pos_change == -snake_block and snake_length > 2:
                        continue
                    x_pos_change = snake_block
                    y_pos_change = 0
                elif event.key == pygame.K_UP:
                    if y_pos_change == snake_block and snake_length > 2:
                        continue
                    x_pos_change = 0
                    y_pos_change = -snake_block
                elif event.key == pygame.K_DOWN:
                    if y_pos_change == -snake_block and snake_length > 2:
                        continue
                    x_pos_change = 0
                    y_pos_change = snake_block
        x_pos += x_pos_change
        y_pos += y_pos_change

        if x_pos >= window_width or x_pos < 0 or y_pos < 0 or y_pos >= window_height:
            end_game()

        dis.fill(black)
        # food draw
        pygame.draw.rect(dis, red, [food_x, food_y, snake_block, snake_block])
        # blitz draw
        pygame.draw.rect(dis, yellow, [blitz_x, blitz_y, snake_block, snake_block])

        snake_list.append([x_pos, y_pos])
        if len(snake_list) > snake_length:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == [x_pos, y_pos]:
                end_game()

        draw_snake(snake_list)
        display_score(snake_length - 1)
        pygame.display.update()

        if x_pos == food_x and y_pos == food_y:
            food_sound.play()
            food_x, food_y, blitz_x, blitz_y = randomizer(True, False, food_x, food_y, blitz_x, blitz_y)
            snake_length += 1

        if x_pos == blitz_x and y_pos == blitz_y:
            food_sound.play()
            food_x, food_y, blitz_x, blitz_y = randomizer(False, True, food_x, food_y, blitz_x, blitz_y)
            snake_speed = snake_speed_boost
            active_blitz = True

        if active_blitz:
            timer -= 1

        if timer == 0:
            active_blitz = False
            timer = 50
            snake_speed = snake_speed_normal

        clock.tick(snake_speed)


if __name__ == '__main__':
    game()
