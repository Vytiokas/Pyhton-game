import pygame
import sys
import random
import math

pygame.init()
pygame.mixer.init()

# --- Nustatymai ---
WIDTH, HEIGHT = 1250, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kosminis Tyrinėtojas - Nuotykių Žaidimas")

clock = pygame.time.Clock()

# --- Fonas ---
background = pygame.image.load("images/background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# --- Platformų tekstūra ---
moon_texture = pygame.image.load("images/moon.png").convert_alpha()

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

# --- Garso efektai (su try-except, jei failų nėra) ---
try:
    jump_sound = pygame.mixer.Sound("sounds/jump.wav")
    collect_sound = pygame.mixer.Sound("sounds/collect.wav")
    shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
    hit_sound = pygame.mixer.Sound("sounds/hit.wav")
    pygame.mixer.music.load("sounds/background.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    SOUNDS_ENABLED = True
except:
    SOUNDS_ENABLED = False
    print("Garso failai nerasti. Žaidimas veiks be garso.")

# --- Konstantos ---
TILE_SIZE = 70
GRAVITY = 1
JUMP_STRENGTH = 20
PLAYER_SPEED = 7
SCROLL_SPEED = 5
FIREBALL_SPEED = 12
FIREBALL_LIFETIME = 90  # frames

# --- Tekstai ---
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 22)
title_font = pygame.font.SysFont("Arial", 56)
hud_font = pygame.font.SysFont("Arial", 32, bold=True)

# --- Klasės ---

class Platform:
    def __init__(self, x, y, width, height, moving=False, move_range=0, move_speed=2):
        self.rect = pygame.Rect(x, y, width, height)
        self.moving = moving
        self.move_range = move_range
        self.move_speed = move_speed
        self.start_x = x
        self.direction = 1
        
    def update(self, camera_x):
        if self.moving:
            self.rect.x += self.move_speed * self.direction
            if abs(self.rect.x - self.start_x) > self.move_range:
                self.direction *= -1
    
    def draw(self, surface, camera_x):
        screen_x = self.rect.x - camera_x
        tex = pygame.transform.scale(moon_texture, (self.rect.width, self.rect.height))
        surface.blit(tex, (screen_x, self.rect.y))
        if self.rect.y < HEIGHT - 100:
            pygame.draw.rect(surface, (255, 255, 255), 
                           (screen_x, self.rect.y, self.rect.width, self.rect.height), 
                           width=2, border_radius=18)


class Loot:
    def __init__(self, x, y, loot_type="coin"):
        self.x = x
        self.y = y
        self.loot_type = loot_type
        self.size = 30
        self.collected = False
        self.float_offset = 0
        self.float_speed = 0.1
        
        # Різні типи loot
        if loot_type == "coin":
            self.color = (255, 215, 0)  # Золотий
            self.score_value = 10
            self.health_value = 0
        elif loot_type == "gem":
            self.color = (0, 255, 255)  # Блакитний
            self.score_value = 25
            self.health_value = 0
        elif loot_type == "heart":
            self.color = (255, 0, 100)  # Червоний
            self.score_value = 0
            self.health_value = 1
    
    def update(self):
        self.float_offset = math.sin(pygame.time.get_ticks() * self.float_speed * 0.01) * 5
    
    def draw(self, surface, camera_x):
        if not self.collected:
            screen_x = self.x - camera_x
            draw_y = self.y + self.float_offset
            
            if self.loot_type == "heart":
                # Малюємо серце
                pygame.draw.circle(surface, self.color, (int(screen_x - 7), int(draw_y)), 8)
                pygame.draw.circle(surface, self.color, (int(screen_x + 7), int(draw_y)), 8)
                points = [(screen_x, draw_y + 5), (screen_x - 15, draw_y - 5), (screen_x + 15, draw_y - 5)]
                pygame.draw.polygon(surface, self.color, points)
                points_bottom = [(screen_x, draw_y + 18), (screen_x - 15, draw_y), (screen_x + 15, draw_y)]
                pygame.draw.polygon(surface, self.color, points_bottom)
            else:
                # Малюємо монету/кристал
                pygame.draw.circle(surface, self.color, (int(screen_x), int(draw_y)), self.size // 2)
                pygame.draw.circle(surface, (255, 255, 255), (int(screen_x), int(draw_y)), self.size // 2, 3)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)


class Enemy:
    def __init__(self, x, y, enemy_type="ground"):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.size = 40
        self.alive = True
        self.health = 2
        self.speed = 2
        self.direction = -1
        self.move_range = 200
        self.start_x = x
        
        # Літаючий ворог
        if enemy_type == "flying":
            self.color = (255, 100, 255)
            self.float_offset = 0
            self.float_speed = 0.05
        else:
            self.color = (255, 50, 50)
    
    def update(self):
        if not self.alive:
            return
            
        if self.enemy_type == "flying":
            self.float_offset = math.sin(pygame.time.get_ticks() * self.float_speed) * 30
            self.x += self.speed * self.direction
            if abs(self.x - self.start_x) > self.move_range:
                self.direction *= -1
        else:
            self.x += self.speed * self.direction
            if abs(self.x - self.start_x) > self.move_range:
                self.direction *= -1
    
    def draw(self, surface, camera_x):
        if self.alive:
            screen_x = self.x - camera_x
            draw_y = self.y + (self.float_offset if self.enemy_type == "flying" else 0)
            
            # Тіло ворога
            pygame.draw.circle(surface, self.color, (int(screen_x), int(draw_y)), self.size // 2)
            # Очі
            eye_offset = 8 if self.direction == 1 else -8
            pygame.draw.circle(surface, (255, 255, 255), (int(screen_x + eye_offset), int(draw_y - 5)), 5)
            pygame.draw.circle(surface, (0, 0, 0), (int(screen_x + eye_offset), int(draw_y - 5)), 3)
            
            # Health bar
            bar_width = self.size
            bar_height = 5
            health_percent = self.health / 2
            pygame.draw.rect(surface, (255, 0, 0), 
                           (screen_x - bar_width // 2, draw_y - self.size // 2 - 10, bar_width, bar_height))
            pygame.draw.rect(surface, (0, 255, 0), 
                           (screen_x - bar_width // 2, draw_y - self.size // 2 - 10, 
                            bar_width * health_percent, bar_height))
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
    
    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.alive = False
            return True
        return False


class Fireball:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = FIREBALL_SPEED
        self.size = 15
        self.lifetime = FIREBALL_LIFETIME
        self.active = True
        self.trail = []
        
    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.active = False
            return
        
        self.x += self.speed * self.direction
        self.y += GRAVITY * 0.3  # Легке падіння
        
        # Додаємо слід
        self.trail.append((self.x, self.y))
        if len(self.trail) > 5:
            self.trail.pop(0)
    
    def draw(self, surface, camera_x):
        if self.active:
            # Малюємо слід
            for i, (tx, ty) in enumerate(self.trail):
                screen_x = tx - camera_x
                alpha = int(255 * (i / len(self.trail)))
                size = self.size * (i / len(self.trail))
                pygame.draw.circle(surface, (255, 150, 0, alpha), (int(screen_x), int(ty)), int(size))
            
            # Основний fireball
            screen_x = self.x - camera_x
            pygame.draw.circle(surface, (255, 200, 0), (int(screen_x), int(self.y)), self.size)
            pygame.draw.circle(surface, (255, 100, 0), (int(screen_x), int(self.y)), self.size // 2)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)


class Game:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.camera_x = 0
        self.score = 0
        self.health = 5
        self.max_health = 5
        
        # Гравець
        self.player_x = 100
        self.player_y = HEIGHT - 200
        self.player_vx = 0
        self.player_vy = 0
        self.player_frame = 0
        self.player_facing_right = True
        self.invincible_timer = 0
        
        # Стрільба
        self.fireballs = []
        self.shoot_cooldown = 0
        
        # Рівень
        self.create_level()
        
        self.game_over = False
        self.victory = False
        
    def create_level(self):
        # Платформи
        self.platforms = []
        ground_y = HEIGHT - 60
        
        # Земля
        for tile_x in range(0, 3000, TILE_SIZE):
            self.platforms.append(Platform(tile_x, ground_y, TILE_SIZE, 60))
        
        # Статичні платформи
        self.platforms.append(Platform(300, ground_y - 150, 220, 25))
        self.platforms.append(Platform(650, ground_y - 250, 220, 25))
        self.platforms.append(Platform(1000, ground_y - 170, 220, 25))
        self.platforms.append(Platform(1400, ground_y - 200, 180, 25))
        self.platforms.append(Platform(1700, ground_y - 280, 200, 25))
        
        # Рухомі платформи
        self.platforms.append(Platform(2000, ground_y - 200, 150, 25, moving=True, move_range=150, move_speed=2))
        self.platforms.append(Platform(2400, ground_y - 300, 150, 25, moving=True, move_range=100, move_speed=3))
        
        # Loot
        self.loots = []
        for i in range(20):
            x = random.randint(200, 2800)
            y = random.randint(200, ground_y - 100)
            loot_type = random.choice(["coin", "coin", "coin", "gem", "heart"])
            self.loots.append(Loot(x, y, loot_type))
        
        # Вороги
        self.enemies = []
        self.enemies.append(Enemy(500, ground_y - 40, "ground"))
        self.enemies.append(Enemy(900, ground_y - 40, "ground"))
        self.enemies.append(Enemy(1300, ground_y - 40, "ground"))
        self.enemies.append(Enemy(800, 300, "flying"))
        self.enemies.append(Enemy(1500, 250, "flying"))
        self.enemies.append(Enemy(2000, 350, "flying"))
        self.enemies.append(Enemy(2200, ground_y - 40, "ground"))
        
    def is_on_ground(self, player_rect):
        test_rect = player_rect.move(0, 1)
        for plat in self.platforms:
            if test_rect.colliderect(plat.rect):
                return True
        return False
    
    def update(self, keys):
        if self.game_over or self.victory:
            if keys[pygame.K_r]:
                self.reset()
            return
        
        # Оновлення платформ
        for plat in self.platforms:
            plat.update(self.camera_x)
        
        # Оновлення loot
        for loot in self.loots:
            loot.update()
        
        # Оновлення ворогів
        for enemy in self.enemies:
            enemy.update()
        
        # Оновлення fireballs
        for fireball in self.fireballs[:]:
            fireball.update()
            if not fireball.active:
                self.fireballs.remove(fireball)
        
        # Рух гравця
        current_img = astronaut_right[self.player_frame] if self.player_facing_right else astronaut_left[self.player_frame]
        player_rect = current_img.get_rect(topleft=(self.player_x, self.player_y))
        
        on_ground = self.is_on_ground(player_rect)
        
        self.player_vx = 0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_vx = PLAYER_SPEED
            self.player_facing_right = True
            self.player_frame = (self.player_frame + 1) % len(astronaut_right)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_vx = -PLAYER_SPEED
            self.player_facing_right = False
            self.player_frame = (self.player_frame + 1) % len(astronaut_left)
        else:
            self.player_frame = 0
        
        self.player_x += self.player_vx
        
        # Камера слідкує за гравцем
        target_camera = self.player_x - WIDTH // 3
        self.camera_x = max(0, min(target_camera, 3000 - WIDTH))
        
        # Шуоліс
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and on_ground:
            self.player_vy = -JUMP_STRENGTH
            if SOUNDS_ENABLED:
                jump_sound.play()
        
        # Стрільба
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
        if keys[pygame.K_f] and self.shoot_cooldown == 0:
            direction = 1 if self.player_facing_right else -1
            fireball_x = self.player_x + (player_width if self.player_facing_right else 0)
            fireball_y = self.player_y + player_height // 2
            self.fireballs.append(Fireball(fireball_x, fireball_y, direction))
            self.shoot_cooldown = 20
            if SOUNDS_ENABLED:
                shoot_sound.play()
        
        # Гравітація
        self.player_vy += GRAVITY
        self.player_y += self.player_vy
        
        # Колізії з платформами
        player_rect = current_img.get_rect(topleft=(self.player_x, self.player_y))
        for plat in self.platforms:
            if player_rect.colliderect(plat.rect):
                if self.player_vy > 0 and player_rect.bottom >= plat.rect.top and player_rect.centery < plat.rect.centery:
                    self.player_y = plat.rect.top - player_height + FOOT_OFFSET
                    self.player_vy = 0
                elif self.player_vy < 0 and player_rect.top <= plat.rect.bottom and player_rect.centery > plat.rect.centery:
                    self.player_y = plat.rect.bottom
                    self.player_vy = 0
        
        # Падіння
        if self.player_y > HEIGHT + 300:
            self.health -= 1
            if self.health > 0:
                self.player_x = 100
                self.player_y = HEIGHT - 200
                self.player_vx = 0
                self.player_vy = 0
                self.invincible_timer = 60
            else:
                self.game_over = True
        
        # Колізії з loot
        for loot in self.loots:
            if not loot.collected and player_rect.colliderect(loot.get_rect()):
                loot.collected = True
                self.score += loot.score_value
                self.health = min(self.health + loot.health_value, self.max_health)
                if SOUNDS_ENABLED:
                    collect_sound.play()
        
        # Невразливість
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        
        # Колізії з ворогами
        for enemy in self.enemies:
            if enemy.alive and self.invincible_timer == 0:
                if player_rect.colliderect(enemy.get_rect()):
                    self.health -= 1
                    self.invincible_timer = 60
                    if SOUNDS_ENABLED:
                        hit_sound.play()
                    if self.health <= 0:
                        self.game_over = True
        
        # Fireball колізії з ворогами
        for fireball in self.fireballs[:]:
            for enemy in self.enemies:
                if enemy.alive and fireball.active:
                    if fireball.get_rect().colliderect(enemy.get_rect()):
                        if enemy.take_damage():
                            self.score += 50
                        fireball.active = False
                        if SOUNDS_ENABLED:
                            hit_sound.play()
                        break
        
        # Перемога
        if self.player_x > 2700:
            self.victory = True
    
    def draw(self, surface):
        # Фон
        surface.blit(background, (-self.camera_x % WIDTH, 0))
        if self.camera_x > 0:
            surface.blit(background, (-self.camera_x % WIDTH + WIDTH, 0))
        
        # Платформи
        for plat in self.platforms:
            plat.draw(surface, self.camera_x)
        
        # Loot
        for loot in self.loots:
            loot.draw(surface, self.camera_x)
        
        # Вороги
        for enemy in self.enemies:
            enemy.draw(surface, self.camera_x)
        
        # Fireballs
        for fireball in self.fireballs:
            fireball.draw(surface, self.camera_x)
        
        # Гравець (з миготінням при невразливості)
        if self.invincible_timer == 0 or (self.invincible_timer // 5) % 2 == 0:
            current_img = astronaut_right[self.player_frame] if self.player_facing_right else astronaut_left[self.player_frame]
            screen_x = self.player_x - self.camera_x
            surface.blit(current_img, (screen_x, self.player_y))
        
        # HUD
        self.draw_hud(surface)
        
        # Заголовок
        title_text = title_font.render("Kosminis Tyrinėtojas", True, (255, 255, 0))
        surface.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
        
        # Інструкції
        info_text = small_font.render("← → / A D рух | SPACE / W шуоліс | F стрільба | R рестарт", True, (255, 255, 0))
        surface.blit(info_text, (10, HEIGHT - 30))
        
        # Game Over
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
            
            game_over_text = title_font.render("GAME OVER", True, (255, 0, 0))
            score_text = hud_font.render(f"Galutinis Score: {self.score}", True, (255, 255, 255))
            press_r_text = font.render("Spausk R, kad pradėtum iš naujo", True, (255, 255, 255))
            
            surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
            surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
            surface.blit(press_r_text, (WIDTH // 2 - press_r_text.get_width() // 2, HEIGHT // 2 + 40))
        
        # Victory
        if self.victory:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
            
            victory_text = title_font.render("VICTORY ROYALE!", True, (0, 255, 0))
            score_text = hud_font.render(f"Galutinis Score: {self.score}", True, (255, 255, 255))
            press_r_text = font.render("Spausk R, kad žaistum dar kartą", True, (255, 255, 255))
            
            surface.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - 100))
            surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 20))
            surface.blit(press_r_text, (WIDTH // 2 - press_r_text.get_width() // 2, HEIGHT // 2 + 40))
    
    def draw_hud(self, surface):
        # Health - серця
        heart_size = 35
        heart_spacing = 40
        start_x = 10
        start_y = 80
        
        for i in range(self.max_health):
            x = start_x + i * heart_spacing
            y = start_y
            
            if i < self.health:
                color = (255, 0, 100)
            else:
                color = (100, 100, 100)
            
            # Малюємо серце
            pygame.draw.circle(surface, color, (x - 7, y), 10)
            pygame.draw.circle(surface, color, (x + 7, y), 10)
            points = [(x, y + 7), (x - 15, y - 5), (x + 15, y - 5)]
            pygame.draw.polygon(surface, color, points)
            points_bottom = [(x, y + 22), (x - 15, y + 2), (x + 15, y + 2)]
            pygame.draw.polygon(surface, color, points_bottom)
        
        # Score bar
        score_text = hud_font.render(f"SCORE: {self.score}", True, (255, 215, 0))
        surface.blit(score_text, (10, 130))
        
        # Score progress bar
        bar_width = 200
        bar_height = 20
        max_score_display = 500
        progress = min(self.score / max_score_display, 1.0)
        
        pygame.draw.rect(surface, (50, 50, 50), (10, 170, bar_width, bar_height))
        pygame.draw.rect(surface, (255, 215, 0), (10, 170, bar_width * progress, bar_height))
        pygame.draw.rect(surface, (255, 255, 255), (10, 170, bar_width, bar_height), 2)


# --- Головний цикл ---
game = Game()
running = True

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    game.update(keys)
    game.draw(win)
    
    pygame.display.update()

pygame.quit()
sys.exit()
