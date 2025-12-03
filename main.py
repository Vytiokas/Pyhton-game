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

# --- Meteorų tekstūros ---
meteor_img = pygame.image.load("images/meteor.png").convert_alpha()
meteor2_img = pygame.image.load("images/meteor2.png").convert_alpha()

# --- Astronauto animacija ---
# Užkrauname visus astronaut failus
astronaut_images = []
temp_images = []
for i in range(1, 16):
    img = pygame.image.load(f"images/astronaut{i}.png")
    temp_images.append(img)

# Naudojame PIRMĄ nuotrauką (astronaut1) kaip bazinį dydį
base_img = temp_images[0]
base_width = base_img.get_width()
base_height = base_img.get_height()

# Scale factor
scale_factor = 0.6

# Bazinis dydis po scale
target_base_width = int(base_width * scale_factor)
target_base_height = int(base_height * scale_factor)

# Dabar scale'iname nuotraukas išlaikant aspect ratio
for i, img in enumerate(temp_images):
    # Skaičiuojame aspect ratio
    aspect_ratio = img.get_width() / img.get_height()
    
    # Scale'iname pagal aukštį, plotis prisitaiko
    new_height = target_base_height
    new_width = int(new_height * aspect_ratio)
    
    img_scaled = pygame.transform.scale(img, (new_width, new_height))
    astronaut_images.append(img_scaled)

# Animacijos grupės pagal jūsų aprašymą:
# 1-5: Stovėjimo animacija
# 6-10: Šuolis/ore/leidimasis
# 11-15: Ėjimas į šoną

# Idle (stovi) - 1-5 nuotraukos
astronaut_idle_right = [
    astronaut_images[0],  # astronaut1
    astronaut_images[1],  # astronaut2
    astronaut_images[2],  # astronaut3
    astronaut_images[3],  # astronaut4
    astronaut_images[4],  # astronaut5
]
astronaut_idle_left = [pygame.transform.flip(img, True, False) for img in astronaut_idle_right]

# Šuolis/Ore/Leidimasis - 6-10 nuotraukos
astronaut_jump_right = [
    astronaut_images[5],  # astronaut6
    astronaut_images[6],  # astronaut7
    astronaut_images[7],  # astronaut8
]
astronaut_jump_left = [pygame.transform.flip(img, True, False) for img in astronaut_jump_right]

astronaut_fall_right = [
    astronaut_images[7],  # astronaut8
    astronaut_images[8],  # astronaut9
    astronaut_images[9],  # astronaut10
]
astronaut_fall_left = [pygame.transform.flip(img, True, False) for img in astronaut_fall_right]

# Ėjimas/Bėgimas - 11-15 nuotraukos
# Jei nuotraukos žiūri į kairę, naudojame jas kaip left
astronaut_run_left = [
    astronaut_images[10],  # astronaut11
    astronaut_images[11],  # astronaut12
    astronaut_images[12],  # astronaut13
    astronaut_images[13],  # astronaut14
    astronaut_images[14],  # astronaut15
]
# Flip'iname į dešinę
astronaut_run_right = [pygame.transform.flip(img, True, False) for img in astronaut_run_left]

# Šaudymas - naudojame paskutines bėgimo nuotraukas
astronaut_shoot_right = [astronaut_images[13], astronaut_images[14]]
astronaut_shoot_left = [pygame.transform.flip(img, True, False) for img in astronaut_shoot_right]

player_width, player_height = astronaut_idle_right[0].get_size()
FOOT_OFFSET = 15

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
WORLD_WIDTH = 6000  # Ilgesnis žaidimas

# --- Tekstai - šiuolaikiškas dizainas ---
font = pygame.font.SysFont("Segoe UI", 24)
small_font = pygame.font.SysFont("Segoe UI", 18)
title_font = pygame.font.SysFont("Segoe UI", 64, bold=True)
hud_font = pygame.font.SysFont("Segoe UI", 28, bold=True)
tiny_font = pygame.font.SysFont("Segoe UI", 16)

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
        # Piešiame su mėnulio tekstūra
        try:
            tex = pygame.transform.scale(moon_texture, (self.rect.width, self.rect.height))
            surface.blit(tex, (screen_x, self.rect.y))
        except:
            # Jei tekstūra neveikia, piešiame pilką
            pygame.draw.rect(surface, (150, 150, 150), 
                           (screen_x, self.rect.y, self.rect.width, self.rect.height))
        
        if self.rect.y < HEIGHT - 100:
            pygame.draw.rect(surface, (255, 255, 255), 
                           (screen_x, self.rect.y, self.rect.width, self.rect.height), 
                           width=2, border_radius=18)


class Loot:
    def __init__(self, x, y, loot_type="star"):
        self.x = x
        self.y = y
        self.loot_type = loot_type
        self.size = 25
        self.collected = False
        self.angle = 0
        
        # Visi loot - baltos žvaigždės
        self.color = (255, 255, 255)
        if loot_type == "star":
            self.score_value = 10
            self.health_value = 0
        elif loot_type == "big_star":
            self.score_value = 25
            self.health_value = 0
            self.size = 35
        elif loot_type == "heart":
            self.score_value = 0
            self.health_value = 1
            self.color = (255, 100, 150)
    
    def update(self):
        # Rotacija
        self.angle += 2
    
    def draw(self, surface, camera_x):
        if not self.collected:
            screen_x = self.x - camera_x
            draw_y = self.y
            
            if self.loot_type == "heart":
                # Širdis
                pygame.draw.circle(surface, self.color, (int(screen_x), int(draw_y)), 12)
                pygame.draw.circle(surface, (255, 255, 255), (int(screen_x), int(draw_y)), 12, 2)
            else:
                # Žvaigždė
                self.draw_star(surface, screen_x, draw_y, self.size // 2, self.color)
    
    def draw_star(self, surface, x, y, size, color):
        # Piešia 5-kampę žvaigždę
        points = []
        for i in range(10):
            angle = math.radians(self.angle + i * 36)
            radius = size if i % 2 == 0 else size // 2
            px = x + radius * math.cos(angle - math.pi / 2)
            py = y + radius * math.sin(angle - math.pi / 2)
            points.append((px, py))
        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, (200, 200, 200), points, 2)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)


class Enemy:
    def __init__(self, x, y, enemy_type="ground", size_variant="normal"):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.alive = True
        self.speed = 2
        self.direction = -1
        self.move_range = 200
        self.start_x = x
        self.stun_timer = 0  # Subliūkčiojimo laikas
        
        # Skirtingi dydžiai
        if size_variant == "small":
            base_size = 35
            self.health = 3
            self.speed = 3
        elif size_variant == "large":
            base_size = 60
            self.health = 5
            self.speed = 1.5
        else:  # normal
            base_size = 45
            self.health = 4
        
        # Літаючий ворог
        if enemy_type == "flying":
            self.float_offset = 0
            self.img = pygame.transform.scale(meteor2_img, (base_size, base_size))
            self.size = base_size
        else:
            self.img = pygame.transform.scale(meteor_img, (base_size, base_size))
            self.size = base_size
    
    def update(self):
        if not self.alive:
            return
        
        # Subliūkčiojimas
        if self.stun_timer > 0:
            self.stun_timer -= 1
            return
            
        self.x += self.speed * self.direction
        if abs(self.x - self.start_x) > self.move_range:
            self.direction *= -1
    
    def draw(self, surface, camera_x):
        if self.alive:
            screen_x = self.x - camera_x
            draw_y = self.y + (self.float_offset if self.enemy_type == "flying" else 0)
            
            # Subliūkčiojimo efektas
            if self.stun_timer > 0 and (self.stun_timer // 3) % 2 == 0:
                # Mirksi
                return
            
            # Piešiame meteor tekstūrą
            img_rect = self.img.get_rect(center=(int(screen_x), int(draw_y)))
            surface.blit(self.img, img_rect)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
    
    def take_damage(self):
        self.health -= 1
        self.stun_timer = 30  # 0.5 sekundės subliūkčiojimas
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
    
    def draw(self, surface, camera_x):
        if self.active:
            # Простий fireball без trail
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
        self.animation_counter = 0  # Для smooth анімації
        self.player_state = "idle"  # idle, run, jump, fall, shoot
        
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
        for tile_x in range(0, WORLD_WIDTH, TILE_SIZE):
            self.platforms.append(Platform(tile_x, ground_y, TILE_SIZE, 60))
        
        # === SEKCIJA 1: Pradžia (0-800) ===
        # Paprastos platformos mokytis (pirmą pašalinome)
        self.platforms.append(Platform(650, ground_y - 180, 120, 25))
        
        # === SEKCIJA 2: Priešų zona (800-1600) ===
        # Viršutinė platforma su priešu ir loot
        self.platforms.append(Platform(900, ground_y - 250, 300, 25))
        # Žemesnė platforma pabėgimui
        self.platforms.append(Platform(1100, ground_y - 100, 150, 25))
        
        # === SEKCIJA 3: Šuolių iššūkis (1600-2400) ===
        self.platforms.append(Platform(1700, ground_y - 150, 120, 25))
        self.platforms.append(Platform(1900, ground_y - 220, 120, 25))
        self.platforms.append(Platform(2100, ground_y - 280, 150, 25))
        self.platforms.append(Platform(2350, ground_y - 200, 120, 25))
        
        # === SEKCIJA 4: Priešų koridorius (2400-3200) ===
        # Viršutinė platforma su priešais
        self.platforms.append(Platform(2500, ground_y - 200, 400, 25))
        # Apatinė platforma - saugus kelias
        self.platforms.append(Platform(2600, ground_y - 80, 200, 25))
        
        # === SEKCIJA 5: Judančios platformos (3200-4000) ===
        self.platforms.append(Platform(3300, ground_y - 180, 150, 25, moving=True, move_range=150, move_speed=2))
        self.platforms.append(Platform(3600, ground_y - 250, 120, 25, moving=True, move_range=100, move_speed=3))
        self.platforms.append(Platform(3900, ground_y - 200, 150, 25))
        
        # === SEKCIJA 6: Aukštas bokštas (4000-4800) ===
        self.platforms.append(Platform(4100, ground_y - 120, 150, 25))
        self.platforms.append(Platform(4300, ground_y - 200, 150, 25))
        self.platforms.append(Platform(4500, ground_y - 280, 150, 25))
        self.platforms.append(Platform(4700, ground_y - 350, 200, 25))
        
        # === SEKCIJA 7: Finalinis iššūkis (4800-5800) ===
        self.platforms.append(Platform(4900, ground_y - 250, 250, 25))
        self.platforms.append(Platform(5200, ground_y - 180, 150, 25))
        self.platforms.append(Platform(5400, ground_y - 250, 200, 25, moving=True, move_range=120, move_speed=2))
        self.platforms.append(Platform(5650, ground_y - 200, 150, 25))
        
        # === LOOT - strategiškai išdėstytas ===
        self.loots = []
        
        # Sekcija 1 - lengvi
        for x in [450, 500, 550, 700]:
            self.loots.append(Loot(x, ground_y - 150, "star"))
        
        # Sekcija 2 - ant viršutinės platformos
        for x in range(950, 1150, 50):
            self.loots.append(Loot(x, ground_y - 290, "star"))
        self.loots.append(Loot(1050, ground_y - 320, "big_star"))
        
        # Sekcija 3 - šuolių kelyje
        self.loots.append(Loot(1750, ground_y - 180, "star"))
        self.loots.append(Loot(1950, ground_y - 250, "star"))
        self.loots.append(Loot(2150, ground_y - 320, "big_star"))
        self.loots.append(Loot(2400, ground_y - 230, "star"))
        
        # Sekcija 4 - priešų zonoje
        for x in range(2550, 2850, 60):
            self.loots.append(Loot(x, ground_y - 240, "star"))
        self.loots.append(Loot(2700, ground_y - 270, "big_star"))
        
        # Sekcija 5 - judančiose platformose
        self.loots.append(Loot(3350, ground_y - 220, "star"))
        self.loots.append(Loot(3650, ground_y - 290, "big_star"))
        
        # Sekcija 6 - bokšte
        self.loots.append(Loot(4150, ground_y - 160, "star"))
        self.loots.append(Loot(4350, ground_y - 240, "star"))
        self.loots.append(Loot(4550, ground_y - 320, "big_star"))
        self.loots.append(Loot(4750, ground_y - 390, "heart"))
        
        # Sekcija 7 - finale
        for x in range(4950, 5100, 50):
            self.loots.append(Loot(x, ground_y - 290, "star"))
        self.loots.append(Loot(5250, ground_y - 220, "big_star"))
        self.loots.append(Loot(5450, ground_y - 290, "star"))
        self.loots.append(Loot(5700, ground_y - 240, "heart"))
        
        # Papildomi loot ant žemės
        for i in range(15):
            x = random.randint(300, WORLD_WIDTH - 300)
            self.loots.append(Loot(x, ground_y - 50, "star"))
        
        # === PRIEŠAI - strategiškai išdėstyti ===
        self.enemies = []
        
        # Sekcija 1 - lengvi priešai
        self.enemies.append(Enemy(600, ground_y - 40, "ground", "small"))
        
        # Sekcija 2 - priešai ant viršutinės platformos
        self.enemies.append(Enemy(1000, ground_y - 275, "ground", "normal"))
        self.enemies.append(Enemy(1150, ground_y - 275, "ground", "normal"))
        self.enemies.append(Enemy(900, 300, "flying", "small"))
        
        # Sekcija 3 - skraidantys priešai
        self.enemies.append(Enemy(1800, 350, "flying", "normal"))
        self.enemies.append(Enemy(2200, 300, "flying", "small"))
        
        # Sekcija 4 - priešų koridorius (viršuje)
        self.enemies.append(Enemy(2600, ground_y - 225, "ground", "large"))
        self.enemies.append(Enemy(2750, ground_y - 225, "ground", "normal"))
        self.enemies.append(Enemy(2850, ground_y - 225, "ground", "small"))
        
        # Sekcija 5 - skraidantys priešai
        self.enemies.append(Enemy(3400, 280, "flying", "normal"))
        self.enemies.append(Enemy(3700, 320, "flying", "large"))
        
        # Sekcija 6 - bokšto apsauga
        self.enemies.append(Enemy(4200, ground_y - 145, "ground", "normal"))
        self.enemies.append(Enemy(4400, ground_y - 225, "ground", "small"))
        self.enemies.append(Enemy(4600, ground_y - 305, "ground", "normal"))
        
        # Sekcija 7 - finaliniai priešai
        self.enemies.append(Enemy(5000, ground_y - 275, "ground", "large"))
        self.enemies.append(Enemy(5100, ground_y - 275, "ground", "large"))
        self.enemies.append(Enemy(5300, 250, "flying", "large"))
        self.enemies.append(Enemy(5500, ground_y - 275, "ground", "normal"))
        
        # Papildomi žeminiai priešai
        for x in [1400, 3000, 3800, 5600]:
            self.enemies.append(Enemy(x, ground_y - 40, "ground", "normal"))
        
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
        # Спочатку визначаємо поточний стан
        temp_img = astronaut_idle_right[0]
        player_rect = temp_img.get_rect(topleft=(self.player_x, self.player_y))
        
        on_ground = self.is_on_ground(player_rect)
        
        # Рух
        self.player_vx = 0
        is_moving = False
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_vx = PLAYER_SPEED
            self.player_facing_right = True
            is_moving = True
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_vx = -PLAYER_SPEED
            self.player_facing_right = False
            is_moving = True
        
        self.player_x += self.player_vx
        
        # Визначаємо стан анімації
        old_state = self.player_state
        
        if self.shoot_cooldown > 15:  # Тільки що стріляв
            self.player_state = "shoot"
        elif not on_ground:
            if self.player_vy < 0:
                self.player_state = "jump"
            else:
                self.player_state = "fall"
        elif is_moving:
            self.player_state = "run"
        else:
            self.player_state = "idle"
        
        # Якщо стан змінився, скидаємо frame
        if old_state != self.player_state:
            self.player_frame = 0
        
        # Оновлюємо анімацію
        self.animation_counter += 1
        
        if self.player_state == "idle":
            current_anim = astronaut_idle_right if self.player_facing_right else astronaut_idle_left
            if self.animation_counter % 10 == 0:
                self.player_frame = (self.player_frame + 1) % len(current_anim)
        elif self.player_state == "run":
            current_anim = astronaut_run_right if self.player_facing_right else astronaut_run_left
            if self.animation_counter % 6 == 0:  # Lėtesnė animacija, kad nebūtų glitchy
                self.player_frame = (self.player_frame + 1) % len(current_anim)
        elif self.player_state == "jump":
            current_anim = astronaut_jump_right if self.player_facing_right else astronaut_jump_left
            if self.animation_counter % 8 == 0:
                self.player_frame = (self.player_frame + 1) % len(current_anim)
        elif self.player_state == "fall":
            current_anim = astronaut_fall_right if self.player_facing_right else astronaut_fall_left
            if self.animation_counter % 8 == 0:
                self.player_frame = (self.player_frame + 1) % len(current_anim)
        elif self.player_state == "shoot":
            current_anim = astronaut_shoot_right if self.player_facing_right else astronaut_shoot_left
            if self.animation_counter % 6 == 0:
                self.player_frame = (self.player_frame + 1) % len(current_anim)
        
        # Отримуємо поточне зображення
        current_img = current_anim[self.player_frame % len(current_anim)]
        
        # Камера слідкує за гравцем
        target_camera = self.player_x - WIDTH // 3
        self.camera_x = max(0, min(target_camera, WORLD_WIDTH - WIDTH))
        
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
            if enemy.alive:
                if player_rect.colliderect(enemy.get_rect()):
                    # Patikrinti ar šoka ant priešo
                    if self.player_vy > 0 and player_rect.bottom <= enemy.get_rect().centery:
                        # Šoka ant priešo - sunaikina jį
                        if enemy.take_damage():
                            self.score += 50
                        self.player_vy = -JUMP_STRENGTH // 2  # Atšoka
                        if SOUNDS_ENABLED:
                            hit_sound.play()
                    elif self.invincible_timer == 0:
                        # Susiduria iš šono - gauna žalą
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
        if self.player_x > WORLD_WIDTH - 300:
            self.victory = True
    
    def draw(self, surface):
        # Фон - paprastas statinis fonas
        surface.blit(background, (0, 0))
        
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
            # Вибираємо правильну анімацію
            if self.player_state == "idle":
                current_anim = astronaut_idle_right if self.player_facing_right else astronaut_idle_left
            elif self.player_state == "run":
                current_anim = astronaut_run_right if self.player_facing_right else astronaut_run_left
            elif self.player_state == "jump":
                current_anim = astronaut_jump_right if self.player_facing_right else astronaut_jump_left
            elif self.player_state == "fall":
                current_anim = astronaut_fall_right if self.player_facing_right else astronaut_fall_left
            elif self.player_state == "shoot":
                current_anim = astronaut_shoot_right if self.player_facing_right else astronaut_shoot_left
            else:
                current_anim = astronaut_idle_right if self.player_facing_right else astronaut_idle_left
            
            current_img = current_anim[self.player_frame % len(current_anim)]
            screen_x = self.player_x - self.camera_x
            surface.blit(current_img, (screen_x, self.player_y))
        
        # HUD
        self.draw_hud(surface)
        
        # Pavadinimas - šiuolaikiškas su šešėliu
        title_text = title_font.render("KOSMINIS TYRINĖTOJAS", True, (255, 255, 100))
        # Šešėlis
        shadow_text = title_font.render("KOSMINIS TYRINĖTOJAS", True, (50, 50, 0))
        title_x = WIDTH // 2 - title_text.get_width() // 2
        surface.blit(shadow_text, (title_x + 3, 23))
        surface.blit(title_text, (title_x, 20))
        
        # Instrukcijos - šiuolaikiškas dizainas
        # Pusiau permatoma juosta apačioje
        info_panel = pygame.Surface((WIDTH, 50))
        info_panel.set_alpha(180)
        info_panel.fill((20, 20, 40))
        surface.blit(info_panel, (0, HEIGHT - 50))
        
        # Instrukcijos su ikonėlėmis
        controls = [
            ("← → / A D", "Judėjimas"),
            ("SPACE / W", "Šuolis"),
            ("F", "Šaudyti"),
            ("R", "Restartas")
        ]
        
        x_offset = 20
        for key, action in controls:
            # Klavišas
            key_text = small_font.render(key, True, (255, 215, 0))
            surface.blit(key_text, (x_offset, HEIGHT - 40))
            
            # Veiksmas
            action_text = tiny_font.render(action, True, (200, 200, 220))
            surface.blit(action_text, (x_offset, HEIGHT - 20))
            
            x_offset += 200
        
        # Game Over - šiuolaikiškas dizainas
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((10, 10, 20))
            surface.blit(overlay, (0, 0))
            
            # Panelė
            panel_width = 600
            panel_height = 300
            panel = pygame.Surface((panel_width, panel_height))
            panel.set_alpha(240)
            panel.fill((30, 30, 50))
            panel_x = WIDTH // 2 - panel_width // 2
            panel_y = HEIGHT // 2 - panel_height // 2
            surface.blit(panel, (panel_x, panel_y))
            pygame.draw.rect(surface, (255, 50, 50), (panel_x, panel_y, panel_width, panel_height), 3, border_radius=15)
            
            # Tekstai
            game_over_text = title_font.render("ŽAIDIMAS BAIGTAS", True, (255, 100, 100))
            score_label = font.render("GALUTINIS REZULTATAS", True, (200, 200, 220))
            score_text = title_font.render(f"{self.score}", True, (255, 215, 0))
            press_r_text = small_font.render("Spausk R norėdamas pradėti iš naujo", True, (180, 180, 200))
            
            surface.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 120))
            surface.blit(score_label, (WIDTH // 2 - score_label.get_width() // 2, HEIGHT // 2 - 30))
            surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
            surface.blit(press_r_text, (WIDTH // 2 - press_r_text.get_width() // 2, HEIGHT // 2 + 90))
        
        # Victory - šiuolaikiškas dizainas
        if self.victory:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((10, 20, 10))
            surface.blit(overlay, (0, 0))
            
            # Panelė
            panel_width = 600
            panel_height = 300
            panel = pygame.Surface((panel_width, panel_height))
            panel.set_alpha(240)
            panel.fill((30, 50, 30))
            panel_x = WIDTH // 2 - panel_width // 2
            panel_y = HEIGHT // 2 - panel_height // 2
            surface.blit(panel, (panel_x, panel_y))
            pygame.draw.rect(surface, (100, 255, 100), (panel_x, panel_y, panel_width, panel_height), 3, border_radius=15)
            
            # Tekstai
            victory_text = title_font.render("PERGALĖ!", True, (100, 255, 100))
            score_label = font.render("GALUTINIS REZULTATAS", True, (200, 220, 200))
            score_text = title_font.render(f"{self.score}", True, (255, 215, 0))
            press_r_text = small_font.render("Spausk R norėdamas žaisti dar kartą", True, (180, 200, 180))
            
            surface.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - 120))
            surface.blit(score_label, (WIDTH // 2 - score_label.get_width() // 2, HEIGHT // 2 - 30))
            surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
            surface.blit(press_r_text, (WIDTH // 2 - press_r_text.get_width() // 2, HEIGHT // 2 + 90))
    
    def draw_hud(self, surface):
        # === ŠIUOLAIKIŠKAS HUD DIZAINAS ===
        
        # Pusiau permatomos HUD panelės
        hud_panel = pygame.Surface((280, 120))
        hud_panel.set_alpha(180)
        hud_panel.fill((20, 20, 40))
        surface.blit(hud_panel, (10, 10))
        
        # Health - kompaktiškos širdys
        heart_size = 20
        heart_spacing = 28
        start_x = 25
        start_y = 30
        
        # Health label
        health_label = tiny_font.render("HEALTH", True, (150, 150, 200))
        surface.blit(health_label, (20, 15))
        
        for i in range(self.max_health):
            x = start_x + i * heart_spacing
            y = start_y
            
            if i < self.health:
                color = (255, 50, 100)
                outline_color = (255, 150, 180)
            else:
                color = (60, 60, 80)
                outline_color = (100, 100, 120)
            
            # Gražesnės širdys
            pygame.draw.circle(surface, color, (x - 5, y), 7)
            pygame.draw.circle(surface, color, (x + 5, y), 7)
            points = [(x, y + 5), (x - 10, y - 3), (x + 10, y - 3)]
            pygame.draw.polygon(surface, color, points)
            points_bottom = [(x, y + 15), (x - 10, y + 1), (x + 10, y + 1)]
            pygame.draw.polygon(surface, color, points_bottom)
            
            # Outline
            pygame.draw.circle(surface, outline_color, (x - 5, y), 7, 2)
            pygame.draw.circle(surface, outline_color, (x + 5, y), 7, 2)
        
        # Score su ikonėle
        score_label = tiny_font.render("SCORE", True, (150, 150, 200))
        surface.blit(score_label, (20, 65))
        
        score_text = hud_font.render(f"{self.score}", True, (255, 215, 0))
        surface.blit(score_text, (25, 85))
        
        # Score progress bar - šiuolaikiškas
        bar_x = 120
        bar_y = 95
        bar_width = 150
        bar_height = 18
        max_score_display = 500
        progress = min(self.score / max_score_display, 1.0)
        
        # Background
        pygame.draw.rect(surface, (40, 40, 60), (bar_x, bar_y, bar_width, bar_height), border_radius=9)
        # Progress
        if progress > 0:
            pygame.draw.rect(surface, (255, 215, 0), (bar_x + 2, bar_y + 2, (bar_width - 4) * progress, bar_height - 4), border_radius=7)
        # Outline
        pygame.draw.rect(surface, (200, 200, 220), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=9)
        
        # Progress text
        progress_text = tiny_font.render(f"{int(progress * 100)}%", True, (200, 200, 220))
        surface.blit(progress_text, (bar_x + bar_width + 10, bar_y + 2))


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
