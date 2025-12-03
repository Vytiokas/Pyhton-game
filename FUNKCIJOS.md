# Žaidimo funkcijų aprašymas

## 📋 Privalomi elementai (5 balai)

### 1. Side-scrolling aplinka (0.5 balai) ✅
**Implementacija:**
- Kamera seka žaidėją naudojant `camera_x` kintamąjį
- Pasaulio plotis: 3000 pikselių
- Visi objektai piešiami atsižvelgiant į kameros poziciją: `screen_x = object_x - camera_x`
- Smooth camera following: `target_camera = self.player_x - WIDTH // 3`

**Kodas:** `Game.update()` metodas, eilutės su camera_x skaičiavimais

### 2. Loot scrollinimas (0.5 balai) ✅
**Implementacija:**
- Visi loot objektai turi absoliučias pasaulio koordinates
- Piešiant, pozicija perskaičiuojama: `screen_x = self.x - camera_x`
- Loot juda kartu su pasauliu automatiškai

**Kodas:** `Loot.draw()` metodas

### 3. Lobio (loot) sistema (0.5 balai) ✅
**Implementacija:**
- 3 loot tipai:
  - **Monetos** (coin): +10 score, auksinė spalva
  - **Kristalai** (gem): +25 score, mėlyna spalva
  - **Širdys** (heart): +1 health, raudona spalva
- 20+ loot objektų atsitiktinėse pozicijose
- Animuotas float efektas: `self.float_offset = math.sin(...) * 5`

**Kodas:** `Loot` klasė, `Game.create_level()` loot generavimas

### 4. Collision aptikimas (0.5 balai) ✅
**Implementacija:**
- Pygame Rect collision detection
- Loot collision: `player_rect.colliderect(loot.get_rect())`
- Priešų collision: `player_rect.colliderect(enemy.get_rect())`
- Platformų collision su vertikaliniu ir horizontaliu aptikimu

**Kodas:** `Game.update()` collision sekcijos

### 5. SCORE ir HEALTH rodymas (0.5 balai) ✅
**Implementacija:**
- Grafinis HUD su širdžių ikonėlėmis (ne tekstas)
- Score skaičius ir progress bar
- Real-time atnaujinimas po kiekvieno įvykio
- Pataikius į priešą: +50 score
- Surinkus loot: +10/+25 score arba +1 health

**Kodas:** `Game.draw_hud()` metodas

### 6. Gyvybių sistema (0.5 balai) ✅
**Implementacija:**
- Pradžioje: 5 gyvybės (`self.health = 5`)
- Prarandamos susidūrus su priešu: `-1 health`
- Prarandamos nukritus: `-1 health`
- Invincibility frames: 60 frames po žalos gavimo
- Game over kai health = 0

**Kodas:** `Game.update()` priešų collision ir falling sekcijos

### 7. Metimo mechanika (0.5 balai) ✅
**Implementacija:**
- Šaudymas F mygtuku
- Fireball objektai su `Fireball` klase
- Cooldown sistema: 20 frames tarp šūvių
- Garso efektas šaudant

**Kodas:** `Fireball` klasė, shooting logika `Game.update()`

### 8. Metamo objekto gyvavimo laikas (0.5 balai) ✅
**Implementacija:**
- Kiekvienas fireball turi `lifetime = 90` frames (~1.5 sek)
- Kiekviename frame: `self.lifetime -= 1`
- Kai `lifetime <= 0`: `self.active = False`
- Neaktyvūs fireball'ai pašalinami iš sąrašo

**Kodas:** `Fireball.update()` metodas

### 9. Metimo krypties keitimas (0.5 balai) ✅
**Implementacija:**
- Fireball direction nustatomas pagal žaidėjo kryptį
- `direction = 1 if self.player_facing_right else -1`
- Fireball juda: `self.x += self.speed * self.direction`
- Spawn pozicija priklauso nuo krypties

**Kodas:** Shooting logika `Game.update()`, `Fireball.__init__()`

### 10. Garso efektai (0.5 balai) ✅
**Implementacija:**
- 4 garso efektai:
  - `jump.wav` - šuolio garsas
  - `collect.wav` - loot surinkimo garsas
  - `shoot.wav` - šaudymo garsas
  - `hit.wav` - smūgio garsas
- Try-except blokas, jei failų nėra
- Automatinis failų kūrimas su `create_simple_sounds.py`

**Kodas:** Garso inicializacija pradžioje, sound.play() iškvietimai

### 11. Fono muzika (0.5 balai) ✅
**Implementacija:**
- `pygame.mixer.music.load("sounds/background.mp3")`
- Loop režimas: `pygame.mixer.music.play(-1)`
- Volume kontrolė: `set_volume(0.3)`
- Groja visą žaidimo laiką

**Kodas:** Muzikos inicializacija pradžioje

---

## 🎨 Papildomi kūrybiniai elementai (3+ balai)

### 1. Speciali metimo animacija ✅
**Implementacija:**
- Animuotas trail (pėdsakas) už fireball
- Trail saugomas list'e: `self.trail.append((self.x, self.y))`
- Kiekvienas trail taškas piešiamas su alpha fade
- Gravitacijos efektas: `self.y += GRAVITY * 0.3`
- Spalvų gradientas: nuo šviesaus (255, 200, 0) iki tamsaus (255, 100, 0)

**Kodas:** `Fireball.update()` ir `Fireball.draw()` metodai

### 2. Priešai su unikalia elgsena ✅
**Implementacija:**
- **Žeminiai priešai** (ground):
  - Juda pirmyn-atgal ant platformų
  - Patrol sistema su `move_range` ir `direction`
  - Raudona spalva (255, 50, 50)
  
- **Skraidantys priešai** (flying):
  - Skraido ore su sinuso bangos judesiu
  - `float_offset = math.sin(...) * 30`
  - Rožinė spalva (255, 100, 255)
  - Patrol sistema ore

- Visi priešai turi:
  - Health bar sistemą (2 HP)
  - Akis, kurios žiūri į judėjimo kryptį
  - AI su automatine krypties keitimo logika

**Kodas:** `Enemy` klasė su `enemy_type` parametru

### 3. Skirtingi loot tipai ✅
**Implementacija:**
- **Monetos** (coin):
  - Auksinė spalva (255, 215, 0)
  - +10 score
  - Dažniausias tipas
  
- **Kristalai** (gem):
  - Mėlyna spalva (0, 255, 255)
  - +25 score
  - Retesnis tipas
  
- **Širdys** (heart):
  - Raudona spalva (255, 0, 100)
  - +1 health (atkuria gyvybes)
  - Specialus piešimas su širdies forma

**Kodas:** `Loot` klasė su `loot_type` parametru

### 4. Dinaminis HUD ✅
**Implementacija:**
- **Gyvybių ikonėlės:**
  - Grafinės širdžių ikonėlės (ne tekstas)
  - Pilnos širdys: raudona spalva (255, 0, 100)
  - Tuščios širdys: pilka spalva (100, 100, 100)
  - Piešiamos su polygon ir circle
  
- **Score juosta:**
  - Progress bar su užpildymu
  - Maksimalus display: 500 taškų
  - Spalvos: auksinė (255, 215, 0)
  
- **Animuotas HUD:**
  - Invincibility mirkčiojimas: `if (self.invincible_timer // 5) % 2 == 0`
  - Priešų health bars virš galvų
  - Real-time atnaujinimas

**Kodas:** `Game.draw_hud()` metodas

### 5. Papildomos lygio detalės ✅
**Implementacija:**
- **Judančios platformos:**
  - 2 judančios platformos su skirtingais greičiais
  - `moving=True, move_range=150, move_speed=2`
  - Automatinis krypties keitimas pasiekus ribą
  - `Platform.update()` metodas
  
- **Statinės platformos:**
  - 15+ platformų skirtinguose aukščiuose
  - Įvairūs plotai (150-220 pikselių)
  - Mėnulio tekstūra
  
- **Interaktyvūs elementai:**
  - Ilgas žaidimo pasaulis (3000 pikselių)
  - Victory zona pabaigoje
  - Skirtingi iššūkių lygiai

**Kodas:** `Platform` klasė, `Game.create_level()` metodas

### 6. Papildomos funkcijos ✅
**Implementacija:**
- **Victory ekranas:**
  - Pilnas ekrano overlay
  - Galutinis score rodymas
  - Restart funkcionalumas
  
- **Game Over ekranas:**
  - Pilnas ekrano overlay
  - Galutinis score rodymas
  - Restart funkcionalumas
  
- **Smooth camera:**
  - Kamera seka žaidėją smooth'iai
  - Ribojimas pasaulio ribose
  
- **Žaidėjo animacija:**
  - 5 frame'ų animacija
  - Skirtingos animacijos kairėn/dešinėn
  - Idle frame kai nejuda
  
- **Priešų AI:**
  - Patrol sistema
  - Automatinis krypties keitimas
  - Health tracking

**Kodas:** Įvairūs `Game` klasės metodai

---

## 📊 Techninė statistika

### Klasės:
- `Game` - pagrindinis žaidimo valdymas
- `Platform` - platformų sistema
- `Loot` - surenkamų objektų sistema
- `Enemy` - priešų sistema
- `Fireball` - metimo sistema

### Kodo eilučių skaičius: ~600 eilučių

### Objektų skaičius žaidime:
- Platformos: 15+ (2 judančios)
- Loot: 20+ objektų
- Priešai: 7 (4 žeminiai, 3 skraidantys)
- Fireballs: dinamiškai kuriami

### FPS: 60
### Ekrano rezoliucija: 1250x800
### Pasaulio dydis: 3000x800

---

## 🎯 Balų skaičiavimas

### Privalomi elementai: 5.5/5 balai ✅
1. Side-scrolling: 0.5 ✅
2. Loot scrolling: 0.5 ✅
3. Loot sistema: 0.5 ✅
4. Collision: 0.5 ✅
5. Score/Health: 0.5 ✅
6. Gyvybės: 0.5 ✅
7. Metimas: 0.5 ✅
8. Lifetime: 0.5 ✅
9. Kryptis: 0.5 ✅
10. Garsai: 0.5 ✅
11. Muzika: 0.5 ✅

### Papildomi elementai: 6/3 balai ✅
1. Metimo animacija ✅
2. Unikalūs priešai ✅
3. Skirtingi loot tipai ✅
4. Dinaminis HUD ✅
5. Lygio detalės ✅
6. Papildomos funkcijos ✅

**VISO: 11.5/8 balai** 🎉

---

## 🚀 Kaip paleisti

```bash
# 1. Įdiekite priklausomybes
pip install pygame

# 2. Sukurkite garso failus
python create_simple_sounds.py

# 3. Paleiskite žaidimą
python main.py
```

## 🎮 Valdymas

- **← → / A D** - Judėjimas
- **SPACE / W / ↑** - Šuolis
- **F** - Šaudyti
- **R** - Restartas
