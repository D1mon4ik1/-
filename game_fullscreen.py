import pygame
import sys
import random
from pygame.locals import *

pygame.init()
fullscreen_mode = False
current_language = "uk"

window_width = 1600
window_height = 900
elevation = window_height * 0.8
frame_per_second = 45
tower_image = 'images/other/tower-fullscreen.png'
background_image = 'images/other/bg-game-fullscreen.png'
floor_image = 'images/other/down-fullscreen.png'

framepersecond_clock = pygame.time.Clock()
window = pygame.display.set_mode((window_width, window_height))

game_images = {'score_images': [pygame.transform.scale2x(pygame.image.load('images/number/{}.png'.format(i)).convert_alpha()) for i in range(10)]}
dragon_images = [pygame.image.load('images/dragon_green/big/dragon{}.png'.format(i)).convert_alpha() for i in range(1, 9)]
game_images['floor_image'] = pygame.image.load(floor_image).convert_alpha()
game_images['background_image'] = pygame.image.load(background_image).convert_alpha()
game_images['tower_image'] = (pygame.transform.rotate(pygame.image.load(tower_image).convert_alpha(), 180), pygame.image.load(tower_image).convert_alpha())

dragon_skins = {
    'skin1': [pygame.image.load('images/dragon_green/big/dragon{}.png'.format(i)).convert_alpha() for i in range(1, 9)],
    'skin2': [pygame.image.load('images/dragon_blue/big/dragon{}.png'.format(i)).convert_alpha() for i in range(1, 9)],
    'skin3': [pygame.image.load('images/dragon_red/big/dragon{}.png'.format(i)).convert_alpha() for i in range(1, 9)],
}

game_audio_sound = {'hit': pygame.mixer.Sound('sounds/hit.mp3'), 'point': pygame.mixer.Sound('sounds/point.mp3'),
                    'wing': pygame.mixer.Sound('sounds/wing.mp3')}

def enable_sound():
    for sound in game_audio_sound.values():
        sound.set_volume(1.0)
def disable_sound():
    for sound in game_audio_sound.values():
        sound.set_volume(0.0)

def createPipe():
    offset = window_height / 3
    pipeHeight = game_images['tower_image'][0].get_height()
    y2 = offset + random.randrange(0, int(window_height - game_images['floor_image'].get_height() - 1.2 * offset))
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]
    return pipe

def draw_pause_button(window):
    pause_button_image = pygame.image.load('images/other/pause_button.png').convert_alpha()
    pause_button_image = pygame.transform.scale(pause_button_image, (75, 75))
    window.blit(pause_button_image, (window_width - pause_button_image.get_width() - 55, 40))
    return pygame.Rect(window_width - pause_button_image.get_width() - 55, 40, pause_button_image.get_width(), pause_button_image.get_height())

def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation - 25 or vertical < 0:
        game_audio_sound['hit'].play()
        return True

    for pipe in up_pipes:
        pipeHeight = game_images['tower_image'][0].get_height()
        if (vertical < pipeHeight + pipe['y'] and
                abs(horizontal - pipe['x']) < game_images['tower_image'][0].get_width()):
            game_audio_sound['hit'].play()
            return True

    for pipe in down_pipes:
        if (vertical + dragon_images[0].get_height() > pipe['y']) and \
                abs(horizontal - pipe['x']) < game_images['tower_image'][0].get_width():
            game_audio_sound['hit'].play()
            return True
    return False

def draw_pause_menu(window):
    transparent_background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    pygame.draw.rect(transparent_background, (0, 0, 0, 200), (0, 0, window_width, window_height))

    menu_rect = pygame.Rect((window_width - 450) // 2, (window_height - 450) // 2, 450, 450)
    window.blit(transparent_background, (0, 0))
    pygame.draw.rect(window, (90, 90, 90), menu_rect, border_radius=20)

    font_path = "files/BERNIERShade-Regular.otf"
    font = pygame.font.Font(font_path, 70)
    pause_text = font.render(translate_text("Пауза", translations), True, (255, 255, 255))
    text_rect = pause_text.get_rect(center=(window_width // 2, 300))
    window.blit(pause_text, text_rect)

    button_color = (50, 50, 50)
    button_text_color = (255, 255, 255)
    button_font = pygame.font.Font(font_path, 55)

    continue_text_render = button_font.render(translate_text("Продовжити", translations), True, button_text_color)
    continue_text_rect = continue_text_render.get_rect(center=(window_width // 2, (window_height - 450) // 2 + 200))
    continue_button_rect = continue_text_rect.inflate(20, 10)
    pygame.draw.rect(window, button_color, continue_button_rect, border_radius=8)
    window.blit(continue_text_render, continue_text_rect)

    main_menu_text_render = button_font.render(translate_text("Головне меню", translations), True, button_text_color)
    main_menu_text_rect = main_menu_text_render.get_rect(center=(window_width // 2, (window_height - 450) // 2 + 350))
    main_menu_button_rect = main_menu_text_rect.inflate(20, 10)
    pygame.draw.rect(window, button_color, main_menu_button_rect, border_radius=8)
    window.blit(main_menu_text_render, main_menu_text_rect)

    pygame.display.update()
    return continue_button_rect, main_menu_button_rect

def draw_game_over_menu(window, score):
    transparent_background = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
    pygame.draw.rect(transparent_background, (0, 0, 0, 200), (0, 0, window_width, window_height))

    menu_rect = pygame.Rect((window_width - 450) // 2, (window_height - 550) // 2, 450, 550)
    window.blit(transparent_background, (0, 0))
    pygame.draw.rect(window, (90, 90, 90), menu_rect, border_radius=20)

    font_path = "files/BERNIERShade-Regular.otf"
    font = pygame.font.Font(font_path, 65)
    game_over_text = font.render(translate_text("Гра закiнчена", translations), True, (255, 255, 255))
    text_rect = game_over_text.get_rect(center=(window_width // 2, (window_height - 550) // 2 + 75))
    window.blit(game_over_text, text_rect)

    font_score = pygame.font.Font(font_path, 60)
    score_text = font_score.render(translate_text("Рахунок", translations) + ": " + str(score), True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(window_width // 2, (window_height - 550) // 2 + 180))
    window.blit(score_text, score_rect)

    button_color = (50, 50, 50)
    button_text_color = (255, 255, 255)
    button_font = pygame.font.Font(font_path, 55)

    restart_text_render = button_font.render(translate_text("Заново", translations), True, button_text_color)
    restart_text_rect = restart_text_render.get_rect(center=(window_width // 2, (window_height - 550) // 2 + 320))
    restart_button_rect = restart_text_rect.inflate(20, 10)
    pygame.draw.rect(window, button_color, restart_button_rect, border_radius=8)
    window.blit(restart_text_render, restart_text_rect)

    main_menu_text_render = button_font.render(translate_text("Головне меню", translations), True, button_text_color)
    main_menu_text_rect = main_menu_text_render.get_rect(center=(window_width // 2, (window_height - 550) // 2 + 470))
    main_menu_button_rect = main_menu_text_rect.inflate(20, 10)
    pygame.draw.rect(window, button_color, main_menu_button_rect, border_radius=8)
    window.blit(main_menu_text_render, main_menu_text_rect)

    pygame.display.update()
    return restart_button_rect, main_menu_button_rect

def check_game_over(window, score):
    restart_rect, menu_rect = draw_game_over_menu(window, score)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_rect.collidepoint(mouse_pos):
                        return "restart"
                    elif menu_rect.collidepoint(mouse_pos):
                        return "menu"

def dragongame2(dragon_skin=None):
    dragon_images = dragon_skin
    current_dragon_image = 0
    your_score = 0
    horizontal = int(window_width / 5)
    vertical = int((window_height - dragon_images[current_dragon_image].get_height()) / 2)
    ground = 0
    mytempheight = 100

    first_pipe = createPipe()
    second_pipe = createPipe()

    down_pipes = [{'x': window_width + 300 - mytempheight, 'y': first_pipe[1]['y']},
                  {'x': window_width + 300 - mytempheight + (window_width / 2), 'y': second_pipe[1]['y']}]
    up_pipes = [{'x': window_width + 300 - mytempheight, 'y': first_pipe[0]['y']},
                {'x': window_width + 300 - mytempheight + (window_width / 2), 'y': second_pipe[0]['y']}]

    pipeVelX = -10
    bird_velocity_y = -9
    bird_Max_Vel_Y = 50
    birdAccY = 1
    bird_flap_velocity = -11
    bird_flapped = False
    last_update_time = pygame.time.get_ticks()

    paused = False
    pause_button_rect = draw_pause_button(window)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    if vertical > 0:
                        bird_velocity_y = bird_flap_velocity
                        bird_flapped = True
                        game_audio_sound['wing'].play()
                elif event.key == K_ESCAPE:
                    paused = not paused
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if paused:
                        if continue_button_rect.collidepoint(mouse_pos):
                            paused = False
                        elif main_menu_button_rect.collidepoint(mouse_pos):
                            return
                    elif pause_button_rect.collidepoint(mouse_pos):
                        paused = not paused
                    else:
                        if vertical > 0:
                            bird_velocity_y = bird_flap_velocity
                            bird_flapped = True
                            game_audio_sound['wing'].play()

        if not paused:
            if pygame.time.get_ticks() - last_update_time >= 50:
                last_update_time = pygame.time.get_ticks()
                current_dragon_image = (current_dragon_image + 1) % len(dragon_images)

            game_over = isGameOver(horizontal, vertical, up_pipes, down_pipes)
            if game_over:
                result = check_game_over(window, your_score)
                if result == "restart":
                    return dragongame2(dragon_skin)
                elif result == "menu":
                    return

            playerMidPos = horizontal + dragon_images[current_dragon_image].get_width() / 2
            for pipe in up_pipes:
                pipeMidPos = pipe['x'] + game_images['tower_image'][0].get_width() / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 15:
                    your_score += 1
                    game_audio_sound['point'].play()

            if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
                bird_velocity_y += birdAccY

            if bird_flapped:
                bird_flapped = False
            playerHeight = dragon_images[current_dragon_image].get_height()
            vertical = vertical + min(bird_velocity_y, elevation - vertical - playerHeight)

            for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
                upperPipe['x'] += pipeVelX
                lowerPipe['x'] += pipeVelX

            if up_pipes[-1]['x'] < window_width * 0.6:
                newpipe = createPipe()
                up_pipes.append(newpipe[0])
                down_pipes.append(newpipe[1])

            if up_pipes[0]['x'] < -game_images['tower_image'][0].get_width():
                up_pipes.pop(0)
                down_pipes.pop(0)

        window.blit(game_images['background_image'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['tower_image'][0], (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['tower_image'][1], (lowerPipe['x'], lowerPipe['y']))

        window.blit(game_images['floor_image'], (ground, elevation))
        window.blit(dragon_images[current_dragon_image], (horizontal, vertical))

        numbers = [int(x) for x in list(str(your_score))]
        width = 0
        for num in numbers:
            width += game_images['score_images'][num].get_width()
        Xoffset = (window_width - width) / 2
        for num in numbers:
            window.blit(game_images['score_images'][num], (Xoffset, window_width * 0.02))
            Xoffset += game_images['score_images'][num].get_width()

        pause_button_rect = draw_pause_button(window)

        if paused:
            continue_button_rect, main_menu_button_rect = draw_pause_menu(window)

        pygame.display.update()
        framepersecond_clock.tick(frame_per_second)

def load_translations(filename):
    translations = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            key, value = line.strip().split(',')
            translations[key] = value
    return translations

def translate_text(text, translations):
    global current_language
    if current_language == "uk":
        return text
    else:
        return translations.get(text, text)

def change_language():
    global current_language
    if current_language == "uk":
        current_language = "en"
    else:
        current_language = "uk"

translations = load_translations('files/translations.txt')

if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif (event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP)) or (
                            event.type == MOUSEBUTTONDOWN and event.button == 1):
                dragongame2(dragon_images)

        window.blit(game_images['background_image'], (0, 0))
        window.blit(dragon_images[0], (int(window_width / 5), int((window_height - dragon_images[0].get_height()) / 2)))
        window.blit(game_images['floor_image'], (0, elevation))

        draw_pause_button(window)

        pygame.display.update()
        framepersecond_clock.tick(frame_per_second)
