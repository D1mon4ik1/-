import pygame
import sys
import os
import pickle
import game_window
import game_fullscreen

fullscreen_mode = False
current_language = "uk"
selected_skin1 = game_window.dragon_skins['skin1']
selected_skin2 = game_fullscreen.dragon_skins['skin1']

def play_music():
    pygame.mixer.music.load("sounds/music.mp3")
    pygame.mixer.music.play(-1)

def some_function():
    pygame.init()
    framepersecond_clock = pygame.time.Clock()
    return framepersecond_clock

def create_button_rect(center_x, center_y, width, height):
    button_rect = pygame.Rect(0, 0, width, height)
    button_rect.center = (center_x, center_y)
    return button_rect

def main_game():
    global fullscreen_mode, music_paused, sound_paused, selected_skin1, selected_skin2
    sound_paused = False
    music_paused = False
    window_title = "Fly Dragon"
    window_width, window_height = 854, 480
    window = pygame.display.set_mode((window_width, window_height))

    def load_background(screen_width, screen_height):
        bg_image = pygame.image.load("images/other/bg-menu.png")
        return pygame.transform.scale(bg_image, (screen_width, screen_height))

    def draw_button(surface, color, rect, button_text, button_font, text_color, translations):
        pygame.draw.rect(surface, color, rect, border_radius=8)
        text_surface = button_font.render(translate_text(button_text, translations), True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    button_color = (50, 50, 50, 200)
    button_hover_color = (125, 125, 125)
    button_text_color = (255, 255, 255)
    font_path = "files/BERNIERShade-Regular.otf"
    font = pygame.font.Font(font_path, 32)
    font_text = pygame.font.Font(None, 30)
    font_name = pygame.font.Font(font_path, 35)

    logo_image = pygame.image.load("images/other/logo.png")
    icon = pygame.image.load("images/other/logo.ico")
    pygame.display.set_icon(icon)
    pygame.display.set_caption(window_title)

    author_image = pygame.image.load("images/other/author.png")
    scaled_author_image = pygame.transform.scale(author_image, (35, 35))

    def draw_author_info_block(surface, x, y, width, height, font_info, text_color):
        info_text = translate_text("Гра", translations) + ": Fly Dragon©\n" + translate_text("Розробник", translations) + ": D1mon4ik1"
        block_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(block_surface, (50, 50, 50, 200), (0, 0, width, height), border_radius=10)
        lines = info_text.split('\n')
        text_surface_line1 = font_info.render(lines[0], True, text_color)
        text_surface_line2 = font_info.render(lines[1], True, text_color)
        if fullscreen_mode:
            text_rect_line1 = text_surface_line1.get_rect(center=(width // 2, height // 2 - 40))
            text_rect_line2 = text_surface_line2.get_rect(center=(width // 2, height // 2 + 40))
        else:
            text_rect_line1 = text_surface_line1.get_rect(center=(width // 2, height // 2 - 20))
            text_rect_line2 = text_surface_line2.get_rect(center=(width // 2, height // 2 + 20))
        block_surface.blit(text_surface_line1, text_rect_line1)
        block_surface.blit(text_surface_line2, text_rect_line2)
        surface.blit(block_surface, (x, y))

    info_image = pygame.image.load("images/other/info.png")
    scaled_info_image = pygame.transform.scale(info_image, (35, 35))

    def draw_info_block(surface, x, y, width, height, font_info, text_color):
        name_text = translate_text("Iнструкцiя", translations)
        info_text = translate_text("Керування в грі відбувається", translations) + "\n" + translate_text("при натисканні клавіші", translations) \
                    + " SPACE,\nUP " + translate_text("(стрілка вгору) або", translations) + " LMB\n" + translate_text("(ліва кнопка миші)", translations)\
                    + ".\n" + translate_text("Пауза активується при натисканні", translations) + "\n" + translate_text("клавіші", translations) \
                    + " ESCAPE.\n" + translate_text("ПРИЄМНОЇ ГРИ!", translations)
        block_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(block_surface, (50, 50, 50, 200), (0, 0, width, height), border_radius=10)
        lines = info_text.split('\n')
        text_surface_name = font_name.render(name_text, True, text_color)
        text_surface_line1 = font_info.render(lines[0], True, text_color)
        text_surface_line2 = font_info.render(lines[1], True, text_color)
        text_surface_line3 = font_info.render(lines[2], True, text_color)
        text_surface_line4 = font_info.render(lines[3], True, text_color)
        text_surface_line5 = font_info.render(lines[4], True, text_color)
        text_surface_line6 = font_info.render(lines[5], True, text_color)
        text_surface_line7 = font_info.render(lines[6], True, text_color)
        if fullscreen_mode:
            text_rect_name = text_surface_name.get_rect(center=(width // 2, 75))
            text_rect_line1 = text_surface_line1.get_rect(center=(width // 2, height // 2 - 230))
            text_rect_line2 = text_surface_line2.get_rect(center=(width // 2, height // 2 - 140))
            text_rect_line3 = text_surface_line3.get_rect(center=(width // 2, height // 2 - 50))
            text_rect_line4 = text_surface_line4.get_rect(center=(width // 2, height // 2 + 40))
            text_rect_line5 = text_surface_line5.get_rect(center=(width // 2, height // 2 + 130))
            text_rect_line6 = text_surface_line6.get_rect(center=(width // 2, height // 2 + 220))
            text_rect_line7 = text_surface_line7.get_rect(center=(width // 2, height // 2 + 350))
        else:
            text_rect_name = text_surface_name.get_rect(center=(width // 2, 40))
            text_rect_line1 = text_surface_line1.get_rect(center=(width // 2, height // 2 - 130))
            text_rect_line2 = text_surface_line2.get_rect(center=(width // 2, height // 2 - 80))
            text_rect_line3 = text_surface_line3.get_rect(center=(width // 2, height // 2 - 30))
            text_rect_line4 = text_surface_line4.get_rect(center=(width // 2, height // 2 + 20))
            text_rect_line5 = text_surface_line5.get_rect(center=(width // 2, height // 2 + 70))
            text_rect_line6 = text_surface_line6.get_rect(center=(width // 2, height // 2 + 120))
            text_rect_line7 = text_surface_line7.get_rect(center=(width // 2, height // 2 + 185))
        block_surface.blit(text_surface_name, text_rect_name)
        block_surface.blit(text_surface_line1, text_rect_line1)
        block_surface.blit(text_surface_line2, text_rect_line2)
        block_surface.blit(text_surface_line3, text_rect_line3)
        block_surface.blit(text_surface_line4, text_rect_line4)
        block_surface.blit(text_surface_line5, text_rect_line5)
        block_surface.blit(text_surface_line6, text_rect_line6)
        block_surface.blit(text_surface_line7, text_rect_line7)
        surface.blit(block_surface, (x, y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_exit.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    if button_skins.collidepoint(event.pos):
                        skins_select()
                    if button_settings.collidepoint(event.pos):
                        setting(window)
                    if button_start.collidepoint(event.pos):
                        if fullscreen_mode:
                            game_fullscreen.dragongame2(selected_skin2)
                        else:
                            game_window.dragongame1(selected_skin1)

            if event.type == pygame.VIDEORESIZE:
                window_width, window_height = event.w, event.h
                if fullscreen_mode:
                    window = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)
                else:
                    window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

            window.fill((0, 0, 0))
            background_image = load_background(window.get_width(), window.get_height())
            window.blit(background_image, (0, 0))

            if fullscreen_mode:
                font = pygame.font.Font(font_path, 60)
                logo_x = (window_width - logo_image.get_width()) // 2 + 370
                logo_y = 0
                logo_width = 400
                logo_height = 392
                button_start = create_button_rect(window_width // 2 + 370, window_height // 2 + 220, 320, 80)
                button_skins = create_button_rect(window_width // 2 + 370, window_height // 2 + 340, 180, 80)
                scaled_author_image = pygame.transform.scale(author_image, (70, 70))
                author_x = 1500
                author_y = 800
                font_text = pygame.font.Font(None, 55)
                author_info_x = 1120
                author_info_y = 575
                block_width = 450
                block_height = 200
                scaled_info_image = pygame.transform.scale(info_image, (70, 70))
                info_x = 1500
                info_y = 30
                font_name = pygame.font.Font(font_path, 65)
                info_info_x = 530
                info_info_y = 30
                block_info_width = 750
                block_info_height = 850
                info_image_rect = info_image.get_rect(bottomleft=(info_x, info_y + 70))
                if current_language == "uk":
                    button_settings = create_button_rect(window_width // 2 + 370, window_height // 2 + 460, 420, 80)
                    button_exit = create_button_rect(window_width // 2 + 370, window_height // 2 + 580, 195, 80)
                else:
                    button_settings = create_button_rect(window_width // 2 + 370, window_height // 2 + 460, 270, 80)
                    button_exit = create_button_rect(window_width // 2 + 370, window_height // 2 + 580, 150, 80)
            else:
                font = pygame.font.Font(font_path, 32)
                logo_x = (window_width - logo_image.get_width()) // 2
                logo_y = 0
                logo_width = 200
                logo_height = 200
                button_start = create_button_rect(window_width // 2, window_height // 2, 170, 50)
                button_skins = create_button_rect(window_width // 2, window_height // 2 + 65, 110, 50)
                scaled_author_image = pygame.transform.scale(author_image, (35, 35))
                author_x = 800
                author_y = 430
                font_text = pygame.font.Font(None, 30)
                author_info_x = 585
                author_info_y = 320
                block_width = 250
                block_height = 100
                scaled_info_image = pygame.transform.scale(info_image, (35, 35))
                info_x = 800
                info_y = 15
                font_name = pygame.font.Font(font_path, 35)
                info_info_x = 270
                info_info_y = 15
                block_info_width = 400
                block_info_height = 450
                info_image_rect = info_image.get_rect(bottomleft=(info_x, info_y + 35))
                if current_language == "uk":
                    button_settings = create_button_rect(window_width // 2, window_height // 2 + 130, 220, 50)
                    button_exit = create_button_rect(window_width // 2, window_height // 2 + 195, 120, 50)
                else:
                    button_settings = create_button_rect(window_width // 2, window_height // 2 + 130, 140, 50)
                    button_exit = create_button_rect(window_width // 2, window_height // 2 + 195, 80, 50)

        author_image_rect = author_image.get_rect(topleft=(author_x, author_y))
        window.blit(scaled_author_image, (author_x, author_y))
        window.blit(scaled_info_image, (info_x, info_y))
        window.blit(logo_image, (logo_x, logo_y))
        logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
        draw_button(window, button_color, button_start, "Почати гру", font, button_text_color, translations)
        draw_button(window, button_color, button_skins, "Скiни", font, button_text_color, translations)
        draw_button(window, button_color, button_settings, "Налаштування", font, button_text_color, translations)
        draw_button(window, button_color, button_exit, "Вийти", font, button_text_color, translations)

        mouse_pos = pygame.mouse.get_pos()
        for button, text in [(button_start, "Почати гру"), (button_skins, "Скiни"), (button_settings, "Налаштування"),
                             (button_exit, "Вийти")]:
            if button.collidepoint(mouse_pos):
                draw_button(window, button_hover_color, button, text, font, button_text_color, translations)
            if author_image_rect.collidepoint(mouse_pos):
                draw_author_info_block(window, author_info_x, author_info_y, block_width, block_height, font_text, button_text_color)
            elif info_image_rect.collidepoint(mouse_pos):
                draw_info_block(window, info_info_x, info_info_y, block_info_width, block_info_height, font_text, button_text_color)

        pygame.display.flip()
    pass

def skins_select():
    global selected_skin1, selected_skin2
    bg_image = pygame.image.load("images/other/bg-menu.png")
    if fullscreen_mode:
        window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        background_image = pygame.transform.scale(bg_image, window.get_size())
    else:
        window = pygame.display.set_mode((854, 480))
        background_image = pygame.transform.scale(bg_image, window.get_size())
    window_width, window_height = 854, 480
    button_color = (50, 50, 50)
    button_hover_color = (125, 125, 125)
    button_text_color = (255, 255, 255)
    button_back = pygame.Rect(20, 20, 200, 50)
    font_path = "files/BERNIERShade-Regular.otf"
    font = pygame.font.Font(font_path, 40)
    header_font = pygame.font.Font(font_path, 40)
    button_top = 120

    def draw_button(surface, color, rect, button_text, button_font, text_color, translations):
        pygame.draw.rect(surface, color, rect, border_radius=8)
        text_surface = button_font.render(translate_text(button_text, translations), True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    def cut_circle(surface):
        circle_surface = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        circle_surface.fill((0, 0, 0, 0))
        circle_rect = circle_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        pygame.draw.circle(circle_surface, (255, 255, 255, 255), circle_rect.center,
                           min(circle_rect.width, circle_rect.height) // 2)
        surface.blit(circle_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        return surface

    def save_selected_skin(selected_skin):
        with open("files/selected_skin.pkl", "wb") as f:
            pickle.dump(selected_skin, f, protocol=-1)

    def load_selected_skin():
        try:
            with open("files/selected_skin.pkl", "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return 1

    selected_block = load_selected_skin()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_back.collidepoint(event.pos):
                        return
                    mouse_x, mouse_y = event.pos
                    if skin1_button_pos[0] <= mouse_x <= skin1_button_pos[0] + button_width and \
                            skin1_button_pos[1] <= mouse_y <= skin1_button_pos[1] + button_height:
                        selected_skin1 = game_window.dragon_skins['skin1']
                        selected_skin2 = game_fullscreen.dragon_skins['skin1']
                        skin1_block.fill((100, 200, 100, 230))
                        skin2_block.fill((0, 0, 0, 0))
                        skin3_block.fill((0, 0, 0, 0))
                        skin1_block = cut_circle(skin1_block)
                        selected_block = 1
                        save_selected_skin(selected_block)
                    elif skin2_button_pos[0] <= mouse_x <= skin2_button_pos[0] + button_width and \
                            skin2_button_pos[1] <= mouse_y <= skin2_button_pos[1] + button_height:
                        selected_skin1 = game_window.dragon_skins['skin2']
                        selected_skin2 = game_fullscreen.dragon_skins['skin2']
                        skin1_block.fill((0, 0, 0, 0))
                        skin2_block.fill((100, 100, 200, 230))
                        skin3_block.fill((0, 0, 0, 0))
                        skin2_block = cut_circle(skin2_block)
                        selected_block = 2
                        save_selected_skin(selected_block)
                    elif skin3_button_pos[0] <= mouse_x <= skin3_button_pos[0] + button_width and \
                            skin3_button_pos[1] <= mouse_y <= skin3_button_pos[1] + button_height:
                        selected_skin1 = game_window.dragon_skins['skin3']
                        selected_skin2 = game_fullscreen.dragon_skins['skin3']
                        skin1_block.fill((0, 0, 0, 0))
                        skin2_block.fill((0, 0, 0, 0))
                        skin3_block.fill((200, 100, 100, 230))
                        skin3_block = cut_circle(skin3_block)
                        selected_block = 3
                        save_selected_skin(selected_block)
                    elif button_back.collidepoint(event.pos):
                        return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        window.fill((0, 0, 0))
        window.blit(background_image, (0, 0))

        header_text_surface = header_font.render(translate_text("Скiни", translations), True, (50, 50, 50))
        switch_text = font.render(translate_text("Оберiть скiн", translations), True, (255, 255, 255))

        if fullscreen_mode:
            font = pygame.font.Font(font_path, 60)
            font_back = pygame.font.Font(font_path, 53)
            block_surface = pygame.Surface((1400, 550), pygame.SRCALPHA)
            pygame.draw.rect(block_surface, (100, 100, 100, 200), block_surface.get_rect(), border_radius=10)
            header_font = pygame.font.Font(font_path, 75)
            header_text_rect = header_text_surface.get_rect(center=(window_width // 2 + 370, 100))
            switch_rect = switch_text.get_rect(center=(window_width - 60, button_top + 130))

            skin1_image = pygame.transform.scale(pygame.image.load("images/other/green.png"), (250, 250))
            skin2_image = pygame.transform.scale(pygame.image.load("images/other/blue.png"), (250, 250))
            skin3_image = pygame.transform.scale(pygame.image.load("images/other/red.png"), (250, 250))

            button_width, button_height = 250, 250
            skin1_button_pos = (window_width // 2 - 175, window_height // 2 + 120)
            skin2_button_pos = (window_width // 2 + 250, window_height // 2 + 120)
            skin3_button_pos = (window_width // 2 + 675, window_height // 2 + 120)

            skin1_block_pos = (skin1_button_pos[0] - 65, skin1_button_pos[1] - 65)
            skin2_block_pos = (skin2_button_pos[0] - 65, skin2_button_pos[1] - 65)
            skin3_block_pos = (skin3_button_pos[0] - 65, skin3_button_pos[1] - 65)

            skin1_block = pygame.Surface((375, 375), pygame.SRCALPHA)
            skin2_block = pygame.Surface((375, 375), pygame.SRCALPHA)
            skin3_block = pygame.Surface((375, 375), pygame.SRCALPHA)
            if selected_block == 1:
                skin1_block = pygame.Surface((375, 375), pygame.SRCALPHA)
                skin1_block.fill((100, 200, 100, 230))
                skin1_block = cut_circle(skin1_block)
            elif selected_block == 2:
                skin2_block = pygame.Surface((375, 375), pygame.SRCALPHA)
                skin2_block.fill((100, 100, 200, 230))
                skin2_block = cut_circle(skin2_block)
            elif selected_block == 3:
                skin3_block = pygame.Surface((375, 375), pygame.SRCALPHA)
                skin3_block.fill((200, 100, 100, 230))
                skin3_block = cut_circle(skin3_block)

            if current_language == "uk":
                button_back = pygame.Rect(50, 50, 200, 75)
            else:
                button_back = pygame.Rect(50, 50, 170, 75)
        else:
            font = pygame.font.Font(font_path, 40)
            font_back = pygame.font.Font(font_path, 30)
            block_surface = pygame.Surface((700, 300), pygame.SRCALPHA)
            pygame.draw.rect(block_surface, (100, 100, 100, 200), block_surface.get_rect(), border_radius=10)
            header_font = pygame.font.Font(font_path, 40)
            header_text_rect = header_text_surface.get_rect(center=(window_width // 2, 40))
            switch_rect = switch_text.get_rect(center=(window_width - 430, button_top + 15))

            skin1_image = pygame.transform.scale(pygame.image.load("images/other/green.png"), (130, 130))
            skin2_image = pygame.transform.scale(pygame.image.load("images/other/blue.png"), (130, 130))
            skin3_image = pygame.transform.scale(pygame.image.load("images/other/red.png"), (130, 130))

            button_width, button_height = 130, 130
            skin1_button_pos = (window_width // 2 - 270, window_height // 2 - 30)
            skin2_button_pos = (window_width // 2 - 70, window_height // 2 - 30)
            skin3_button_pos = (window_width // 2 + 130, window_height // 2 - 30)

            skin1_block_pos = (skin1_button_pos[0] - 30, skin1_button_pos[1] - 30)
            skin2_block_pos = (skin2_button_pos[0] - 30, skin2_button_pos[1] - 30)
            skin3_block_pos = (skin3_button_pos[0] - 30, skin3_button_pos[1] - 30)

            skin1_block = pygame.Surface((190, 190), pygame.SRCALPHA)
            skin2_block = pygame.Surface((190, 190), pygame.SRCALPHA)
            skin3_block = pygame.Surface((190, 190), pygame.SRCALPHA)
            if selected_block == 1:
                skin1_block = pygame.Surface((190, 190), pygame.SRCALPHA)
                skin1_block.fill((100, 200, 100, 230))
                skin1_block = cut_circle(skin1_block)
            elif selected_block == 2:
                skin2_block = pygame.Surface((190, 190), pygame.SRCALPHA)
                skin2_block.fill((100, 100, 200, 230))
                skin2_block = cut_circle(skin2_block)
            elif selected_block == 3:
                skin3_block = pygame.Surface((190, 190), pygame.SRCALPHA)
                skin3_block.fill((200, 100, 100, 230))
                skin3_block = cut_circle(skin3_block)

            if current_language == "uk":
                button_back = pygame.Rect(20, 20, 100, 40)
            else:
                button_back = pygame.Rect(20, 20, 75, 40)

        block_rect = block_surface.get_rect(center=window.get_rect().center)
        window.blit(block_surface, block_rect)
        window.blit(header_text_surface, header_text_rect)
        window.blit(switch_text, switch_rect)

        if selected_block == 1:
            window.blit(skin1_block, skin1_block_pos)
        elif selected_block == 2:
            window.blit(skin2_block, skin2_block_pos)
        elif selected_block == 3:
            window.blit(skin3_block, skin3_block_pos)
        window.blit(skin1_image, skin1_button_pos)
        window.blit(skin2_image, skin2_button_pos)
        window.blit(skin3_image, skin3_button_pos)

        draw_button(window, button_color, button_back, "Назад", font_back, button_text_color, translations)
        mouse_pos = pygame.mouse.get_pos()
        for button, text in [(button_back, "Назад")]:
            if button.collidepoint(mouse_pos):
                draw_button(window, button_hover_color, button, text, font_back, button_text_color, translations)

        pygame.display.flip()

def setting(main_window):
    global fullscreen_mode, music_paused, sound_paused, current_language
    window_width = 854
    window_height = 480
    background_image_original = pygame.image.load("images/other/bg-menu.png")
    button_color = (50, 50, 50)
    button_hover_color = (125, 125, 125)
    button_text_color = (255, 255, 255)
    button_back = pygame.Rect(20, 20, 200, 50)
    font_path = "files/BERNIERShade-Regular.otf"
    font = pygame.font.Font(font_path, 40)
    header_font = pygame.font.Font(font_path, 40)

    button_top = 120
    radio_button = pygame.Rect(540, button_top, 30, 30)
    music_switch_button = pygame.Rect(540, button_top + 100, 30, 30)
    sound_switch_button = pygame.Rect(540, button_top + 200, 30, 30)
    language_button = pygame.Rect(540, button_top + 300, 30, 30)

    uk_selected_image = pygame.image.load("images/other/eng.png")
    en_selected_image = pygame.image.load("images/other/ua.png")

    def draw_radio_button(surface, rect, language, uk_image, en_image):
        if language == "uk":
            surface.blit(uk_image, (rect.x, rect.y))
        else:
            surface.blit(en_image, (rect.x, rect.y))

    def draw_button(surface, color, rect, button_text, button_font, text_color, translations):
        pygame.draw.rect(surface, color, rect, border_radius=8)
        text_surface = button_font.render(translate_text(button_text, translations), True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if radio_button.collidepoint(event.pos):
                        fullscreen_mode = not fullscreen_mode
                        if fullscreen_mode:
                            main_window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        else:
                            main_window = pygame.display.set_mode((window_width, window_height))
                    if language_button.collidepoint(event.pos):
                        current_language = "uk" if current_language == "en" else "en"
                        game_window.change_language()
                        game_fullscreen.change_language()
                    if music_switch_button.collidepoint(event.pos):
                        if music_paused:
                            pygame.mixer.music.unpause()
                            music_paused = False
                        else:
                            pygame.mixer.music.pause()
                            music_paused = True
                    if sound_switch_button.collidepoint(event.pos):
                        if sound_paused:
                            game_window.enable_sound()
                            game_fullscreen.enable_sound()
                            sound_paused = False
                        else:
                            game_window.disable_sound()
                            game_fullscreen.disable_sound()
                            sound_paused = True
                    if button_back.collidepoint(event.pos):
                        return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        header_text_surface = header_font.render(translate_text("Налаштування", translations), True, (50, 50, 50))
        switch_text = font.render(translate_text("На весь екран", translations), True, (255, 255, 255))
        music_text = font.render(translate_text("Музика", translations), True, (255, 255, 255))
        sound_text = font.render(translate_text("Звуки", translations), True, (255, 255, 255))

        if fullscreen_mode:
            screen_width, screen_height = pygame.display.get_surface().get_size()
            background_image_scaled = pygame.transform.scale(background_image_original, (screen_width, screen_height))
            font_back = pygame.font.Font(font_path, 53)
            font = pygame.font.Font(font_path, 60)
            radio_button = pygame.Rect(960, button_top + 160, 30, 30)
            music_switch_button = pygame.Rect(960, button_top + 310, 30, 30)
            sound_switch_button = pygame.Rect(960, button_top + 460, 30, 30)
            block_surface = pygame.Surface((500, 500), pygame.SRCALPHA)
            pygame.draw.rect(block_surface, (100, 100, 100, 200), block_surface.get_rect(), border_radius=10)
            header_font = pygame.font.Font(font_path, 75)
            header_text_rect = header_text_surface.get_rect(center=(window_width // 2 + 370, 100))
            switch_rect = switch_text.get_rect(center=(window_width - 100, button_top + 175))
            music_rect = music_text.get_rect(center=(window_width - 100, button_top + 325))
            uk_selected_image = pygame.transform.scale(uk_selected_image, (100, 100))
            en_selected_image = pygame.transform.scale(en_selected_image, (100, 100))
            language_button = pygame.Rect(1450, button_top + 650, 100, 100)
            if current_language == "uk":
                button_back = pygame.Rect(50, 50, 200, 75)
                sound_rect = music_text.get_rect(center=(window_width - 85, button_top + 475))
            else:
                button_back = pygame.Rect(50, 50, 170, 75)
                sound_rect = music_text.get_rect(center=(window_width - 110, button_top + 475))
        else:
            background_image_scaled = pygame.transform.scale(background_image_original, (window_width, window_height))
            font_back = pygame.font.Font(font_path, 30)
            font = pygame.font.Font(font_path, 40)
            radio_button = pygame.Rect(540, button_top, 30, 30)
            music_switch_button = pygame.Rect(540, button_top + 100, 30, 30)
            sound_switch_button = pygame.Rect(540, button_top + 200, 30, 30)
            block_surface = pygame.Surface((350, 350), pygame.SRCALPHA)
            pygame.draw.rect(block_surface, (100, 100, 100, 200), block_surface.get_rect(), border_radius=10)
            header_font = pygame.font.Font(font_path, 40)
            header_text_rect = header_text_surface.get_rect(center=(window_width // 2, 30))
            switch_rect = switch_text.get_rect(center=(window_width - 460, button_top + 15))
            music_rect = music_text.get_rect(center=(window_width - 460, button_top + 115))
            uk_selected_image = pygame.transform.scale(uk_selected_image, (50, 50))
            en_selected_image = pygame.transform.scale(en_selected_image, (50, 50))
            language_button = pygame.Rect(775, button_top + 300, 50, 50)
            if current_language == "uk":
                button_back = pygame.Rect(20, 20, 100, 40)
                sound_rect = music_text.get_rect(center=(window_width - 445, button_top + 215))
            else:
                button_back = pygame.Rect(20, 20, 75, 40)
                sound_rect = music_text.get_rect(center=(window_width - 470, button_top + 215))

        main_window.fill((0, 0, 0))
        main_window.blit(background_image_scaled, (0, 0))

        block_rect = block_surface.get_rect(center=main_window.get_rect().center)
        main_window.blit(block_surface, block_rect)
        main_window.blit(header_text_surface, header_text_rect)
        main_window.blit(music_text, music_rect)
        main_window.blit(sound_text, sound_rect)
        main_window.blit(switch_text, switch_rect)

        draw_radio_button(main_window, language_button, current_language, uk_selected_image, en_selected_image)
        draw_button(main_window, button_color, button_back, "Назад", font_back, button_text_color, translations)

        mouse_pos = pygame.mouse.get_pos()
        for button, text in [(button_back, "Назад")]:
            if button.collidepoint(mouse_pos):
                draw_button(main_window, button_hover_color, button, text, font_back, button_text_color, translations)

        if fullscreen_mode:
            pygame.draw.circle(main_window, (0, 255, 0), (radio_button.x + radio_button.width // 2, radio_button.y + radio_button.height // 2), 15)
            if music_paused:
                pygame.draw.circle(main_window, (255, 0, 0), (music_switch_button.x + music_switch_button.width // 2, music_switch_button.y + music_switch_button.height // 2), 15)
            else:
                pygame.draw.circle(main_window, (0, 255, 0), (music_switch_button.x + music_switch_button.width // 2, music_switch_button.y + music_switch_button.height // 2), 15)
            if sound_paused:
                pygame.draw.circle(main_window, (255, 0, 0), (sound_switch_button.x + sound_switch_button.width // 2, sound_switch_button.y + sound_switch_button.height // 2), 15)
            else:
                pygame.draw.circle(main_window, (0, 255, 0), (sound_switch_button.x + sound_switch_button.width // 2, sound_switch_button.y + sound_switch_button.height // 2), 15)
        else:
            pygame.draw.circle(main_window, (255, 0, 0), (radio_button.x + radio_button.width // 2, radio_button.y + radio_button.height // 2), 10)
            if music_paused:
                pygame.draw.circle(main_window, (255, 0, 0), (music_switch_button.x + music_switch_button.width // 2, music_switch_button.y + music_switch_button.height // 2), 10)
            else:
                pygame.draw.circle(main_window, (0, 255, 0), (music_switch_button.x + music_switch_button.width // 2, music_switch_button.y + music_switch_button.height // 2), 10)
            if sound_paused:
                pygame.draw.circle(main_window, (255, 0, 0), (sound_switch_button.x + sound_switch_button.width // 2, sound_switch_button.y + sound_switch_button.height // 2), 10)
            else:
                pygame.draw.circle(main_window, (0, 255, 0), (sound_switch_button.x + sound_switch_button.width // 2, sound_switch_button.y + sound_switch_button.height // 2), 10)

        pygame.display.flip()

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

def delete_selected_skin_file():
    try:
        os.remove("files/selected_skin.pkl")
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    delete_selected_skin_file()
    sound_paused = False
    music_paused = False
    play_music()
    main_game()
