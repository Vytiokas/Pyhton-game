import pygame
import sys

pygame.init()

# --- Nustatymai (didelis langas) ---
WIDTH, HEIGHT = 1250, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kosminis tyrinėtojas")

clock = pygame.time.Clock()

# --- Fonas ---
background = pygame.image.load("images/background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# --- Platformų tekstūra (Mėnulis) ---
moon_texture = pygame.image.load("images/moon.png").convert_alpha()

# --- Platformos ---
TILE_SIZE = 70
platforms = []
ground_height = 60
ground_y = HEIGHT - ground_height
for tile_x in range(0, WIDTH, TILE_SIZE):
    platforms.append(pygame.Rect(tile_x, ground_y, TILE_SIZE, ground_height))

# Rankomis darytos platformos
platforms.append(pygame.Rect(300, ground_y - 150, 220, 25))
platforms.append(pygame.Rect(650, ground_y - 250, 220, 25))
platforms.append(pygame.Rect(1000, ground_y - 170, 220, 25))

# --- Astronauto animacija ---
astronaut_left = [
    pygame.image.load("images/astronaut11.png"),
    pygame.image.load("images/astronaut12.png"),
    pygame.image.load("images/astronaut13.png"),
    pygame.image.load("images/astronaut14.png"),
    pygame.image.load("images/astronaut15.png"),
]
astronaut_right = [pygame.transform.flip(img, True, False) for img in astronaut_left]

player_width, player_height = astronaut_right[0].get_size()
FOOT_OFFSET = 20

# --- Žaidėjo kintamieji ---
x = 80
y = ground_y - player_height + FOOT_OFFSET
vx = 0
vy = 0
speed = 7
GRAVITY = 1
JUMP_STRENGTH = 20
frame = 0
facing_right = True
lives = 3
invincible_timer = 0

# --- Dvi kometos ---
meteor_bottom = pygame.image.load("images/meteor.png")
meteor_top = pygame.image.load("images/meteor2.png")

meteor_w, meteor_h = meteor_bottom.get_size()

meteor1_x = WIDTH - 150
meteor1_y = ground_y - meteor_h
meteor1_speed = 5
meteor1_dir = -1
meteor1_left = 20
meteor1_right = WIDTH - 20 - meteor_w
meteor1_alive = True

meteor2_x = WIDTH // 2
meteor2_y = 120
meteor2_speed = 4
meteor2_dir = 1
meteor2_left = 100
meteor2_right = WIDTH - 200
meteor2_alive = True

# --- Tekstas ---
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 22)
title_font = pygame.font.SysFont("Arial", 56)
victory_font = pygame.font.SysFont("Arial", 72)

game_over = False
victory = False


def reset_player():
    global x, y, vx, vy
    x = 80
    y = ground_y - player_height + FOOT_OFFSET
    vx = 0
    vy = 0


def reset_game():
    global lives, meteor1_x, meteor1_y, meteor1_dir, meteor1_alive
    global meteor2_x, meteor2_y, meteor2_dir, meteor2_alive
    global invincible_timer, game_over, victory

    lives = 3
    reset_player()

    meteor1_x = WIDTH - 150
    meteor1_y = ground_y - meteor_h
    meteor1_dir = -1
    meteor1_alive = True

    meteor2_x = WIDTH // 2
    meteor2_y = 120
    meteor2_dir = 1
    meteor2_alive = True

    invincible_timer = 0
    game_over = False
    victory = False


def is_on_ground(player_rect):
    test_rect = player_rect.move(0, 1)
    for plat in platforms:
        if test_rect.colliderect(plat):
            return True
    return False


reset_game()

# --- Pagrindinis ciklas ---
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # --- GAME OVER ---
    if game_over:
        if keys[pygame.K_r]:
            reset_game()
        win.blit(background, (0, 0))
        game_over_text = title_font.render("GAME OVER", True, (255, 0, 0))
        press_r_text = font.render("Spausk R, kad pradėtum iš naujo", True, (255, 255, 255))
        win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 80))
        win.blit(press_r_text, (WIDTH // 2 - press_r_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        continue

    # --- VICTORY ---
    if victory:
        if keys[pygame.K_r]:
            reset_game()
        win.blit(background, (0, 0))
        victory_text = victory_font.render("VICTORY ROYALE!", True, (0, 255, 0))
        press_r_text = font.render("Spausk R, kad žaistum dar kartą", True, (255, 255, 255))
        win.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - 80))
        win.blit(press_r_text, (WIDTH // 2 - press_r_text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        continue

    # --- ŽAIDIMO LOGIKA ---
    current_img = astronaut_right[frame] if facing_right else astronaut_left[frame]
    player_rect = current_img.get_rect(topleft=(x, y))

    on_ground = is_on_ground(player_rect)

    vx = 0
    if keys[pygame.K_RIGHT]:
        vx += speed
    if keys[pygame.K_LEFT]:
        vx -= speed

    if vx != 0:
        x += vx
        facing_right = vx > 0
        frame = (frame + 1) % len(astronaut_right)
    else:
        frame = 0

    # JEI PASIEKIA DEŠINĘ PUSĘ – VICTORY ROYALE
    if x >= WIDTH - player_width - 10:
        victory = True

    if x < 0:
        x = 0
    if x > WIDTH - player_width:
        x = WIDTH - player_width

    # Šuolis
    if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and on_ground:
        vy = -JUMP_STRENGTH

    vy += GRAVITY
    y += vy

    # Vertikalūs susidūrimai
    player_rect = current_img.get_rect(topleft=(x, y))
    for plat in platforms:
        if player_rect.colliderect(plat):
            if vy > 0 and player_rect.bottom >= plat.top and player_rect.centery < plat.centery:
                y = plat.top - player_height + FOOT_OFFSET
                vy = 0
            elif vy < 0 and player_rect.top <= plat.bottom and player_rect.centery > plat.centery:
                y = plat.bottom
                vy = 0

    # Nukritimas
    if y > HEIGHT + 300:
        lives -= 1
        if lives > 0:
            reset_player()
            invincible_timer = 60
        else:
            game_over = True

    # --- Kometų judėjimas ---
    if meteor1_alive:
        meteor1_x += meteor1_speed * meteor1_dir
        if meteor1_x < meteor1_left or meteor1_x > meteor1_right:
            meteor1_dir *= -1

    if meteor2_alive:
        meteor2_x += meteor2_speed * meteor2_dir
        if meteor2_x < meteor2_left or meteor2_x > meteor2_right:
            meteor2_dir *= -1

    # --- Susidūrimai su kometomis ---
    if invincible_timer > 0:
        invincible_timer -= 1

    def check_collision(mx, my, alive_flag_name):
        """Tikrina susidūrimą su kometa."""
        global lives, game_over, invincible_timer, vy
        meteor_rect = pygame.Rect(mx, my, meteor_w, meteor_h)
        alive = globals()[alive_flag_name]
        if alive and player_rect.colliderect(meteor_rect):
            if vy > 0 and player_rect.bottom <= meteor_rect.top + 10:
                globals()[alive_flag_name] = False
                vy = -JUMP_STRENGTH // 2
            else:
                if lives > 1:
                    lives -= 1
                    reset_player()
                    invincible_timer = 60
                else:
                    lives = 0
                    game_over = True

    check_collision(meteor1_x, meteor1_y, "meteor1_alive")
    check_collision(meteor2_x, meteor2_y, "meteor2_alive")

    # --- PIEŠIMAS ---
    win.blit(background, (0, 0))

    # Pavadinimas
    title_text = title_font.render("Kosminis tyrinėtojas", True, (255, 255, 0))
    win.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

    # Platformos
    # Platformos – tekstūra + apvalintas kontūras
    # Platformos – Mėnulio tekstūra + apvalintos tik viršutinės
    for plat in platforms:
        tex = pygame.transform.scale(moon_texture, (plat.width, plat.height))
        win.blit(tex, (plat.x, plat.y))

    # Apvalinam tik tas, kurios nėra grindys
        if plat.y < ground_y:
            pygame.draw.rect(win, (255, 255, 255), plat, width=2, border_radius=18)



    # Kometos
    if meteor1_alive:
        win.blit(meteor_bottom, (meteor1_x, meteor1_y))
    if meteor2_alive:
        win.blit(meteor_top, (meteor2_x, meteor2_y))

    # Žaidėjas
    win.blit(current_img, (x, y))

    # Tekstas
    lives_text = font.render(f"Gyvybės: {lives}", True, (255, 255, 255))
    info_text = small_font.render("← → judėjimas | SPACE/↑ šuolis | R – restartas", True, (255, 255, 0))
    win.blit(lives_text, (10, 10))
    win.blit(info_text, (10, 40))

    pygame.display.update()

pygame.quit()
sys.exit()
