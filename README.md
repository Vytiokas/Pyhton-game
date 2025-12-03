# Kosminis Tyrinėtojas 🚀

Pilnavertis side-scrolling nuotykių žaidimas, sukurtas su Python ir Pygame.

## Apie žaidimą

Valdyk astronautą kosmose, šok per platformas, rink loot, kovok su priešais ir pasiekt žaidimo pabaigą!

## Žaidimo mechanikos

### ✨ Pagrindinės funkcijos:
- **Side-scrolling aplinka** - pasaulis juda kartu su žaidėju
- **Loot sistema** - rink monetas, kristalus ir širdeles
- **Priešai** - žeminiai ir skraidantys priešai su unikalia elgsena
- **Metimo mechanika** - šaudyk ugnies kamuolius
- **Health ir Score sistema** - sekite savo pažangą
- **Animuotas HUD** - grafinės gyvybių ikonėlės ir score juosta
- **Ruchomės platformos** - dinaminis žaidimo pasaulis

### 🎮 Valdymas:
- **← → arba A D** - Judėjimas į kairę/dešinę
- **SPACE arba W arba ↑** - Šuolis
- **F** - Šaudyti ugnies kamuolį
- **R** - Restartas

## Žaidimo elementai

### 🪙 Loot tipai:
- **Monetos** (auksinės) - +10 score
- **Kristalai** (mėlyni) - +25 score
- **Širdys** (raudonos) - +1 health

### 👾 Priešai:
- **Žeminiai priešai** - juda pirmyn-atgal ant platformų
- **Skraidantys priešai** - skraido ore su bangavimo judesiu
- Priešai turi 2 health taškus
- Sunaikinus priešą gaunate +50 score

### 🔥 Metimo sistema:
- Šaudykite ugnies kamuolius mygtuku F
- Kamuoliai juda ta kryptimi, kur žiūri žaidėjas
- Kamuoliai turi gyvavimo laiką ir animuotą pėdsaką
- Pataikius į priešą, jis gauna žalą

## Žaidimo tikslas

Pasiekti žaidimo pabaigą (2700+ pikselių), surinkti kuo daugiau taškų ir išvengti priešų!

## Įdiegimas

1. Įsitikinkite, kad turite įdiegtą Python 3.x
2. Įdiekite reikalingas bibliotekas:
```bash
pip install -r requirements.txt
```

3. Sukurkite garso failus (jei jų nėra):
```bash
python create_simple_sounds.py
```

## Kaip paleisti

```bash
python main.py
```

**Pastaba:** Žaidimas veiks ir be garso failų, bet rekomenduojama juos sukurti.

## Reikalavimai

- Python 3.x
- Pygame

## Struktūra

```
.
├── main.py           # Pagrindinis žaidimo failas
├── images/           # Žaidimo grafika
│   ├── astronaut*.png
│   ├── background.jpg
│   ├── meteor.png
│   ├── meteor2.png
│   └── moon.png
└── README.md
```

## Autorius

Vytiokas


## Įgyvendintos funkcijos

### ✅ Privalomi elementai (5 balai):

1. **Side-scrolling aplinka** (0.5 balai)
   - Žaidimo pasaulis juda kartu su žaidėju
   - Kamera seka žaidėją
   - Pasaulio plotis: 3000 pikselių

2. **Loot scrollinimas** (0.5 balai)
   - Visi surenkami objektai juda kartu su pasauliu
   - Loot pozicijos perskaičiuojamos pagal kamerą

3. **Lobio (loot) sistema** (0.5 balai)
   - 3 tipai loot: monetos (+10 score), kristalai (+25 score), širdys (+1 health)
   - 20+ loot objektų žaidime
   - Animuotas float efektas

4. **Collision aptikimas** (0.5 balai)
   - Tikslus collision detection su loot objektais
   - Collision su priešais
   - Collision su platformomis

5. **SCORE ir HEALTH rodymas** (0.5 balai)
   - Grafinis HUD su širdžių ikonėlėmis
   - Score skaičius ir progress bar
   - Real-time atnaujinimas

6. **Gyvybių sistema** (0.5 balai)
   - 5 gyvybės pradžioje
   - Prarandamos susidūrus su priešu
   - Invincibility frames po žalos gavimo

7. **Metimo mechanika** (0.5 balai)
   - Šaudymas ugnies kamuoliais (F mygtukas)
   - Cooldown sistema tarp šūvių

8. **Metamo objekto gyvavimo laikas** (0.5 balai)
   - Fireball gyvena 90 frames (~1.5 sekundės)
   - Automatiškai išnyksta

9. **Metimo krypties keitimas** (0.5 balai)
   - Fireball juda ta kryptimi, kur žiūri žaidėjas
   - Dinaminis direction tracking

10. **Garso efektai** (0.5 balai)
    - 4 garso efektai: šuolis, surinkimas, šaudymas, smūgis
    - Automatinis garso failų kūrimas

11. **Fono muzika** (0.5 balai)
    - Nuolat grojanti fono muzika
    - Loop režimas

### ✅ Papildomi kūrybiniai elementai (3+ balai):

1. **Speciali metimo animacija**
   - Fireball turi animuotą pėdsaką (trail effect)
   - Gravitacijos efektas fireball'ui
   - Spalvų gradientas

2. **Priešai su unikalia elgsena**
   - Žeminiai priešai: juda pirmyn-atgal ant platformų
   - Skraidantys priešai: skraido ore su sinuso bangos judesiu
   - Priešai turi health bar sistemą (2 HP)
   - Skirtingi priešų tipai su skirtingomis spalvomis

3. **Skirtingi loot tipai**
   - Monetos: +10 score
   - Kristalai: +25 score (reti)
   - Širdys: +1 health (atkuria gyvybes)

4. **Dinaminis HUD**
   - Grafinės širdžių ikonėlės vietoj teksto
   - Animuotas score progress bar
   - Invincibility mirkčiojimas
   - Priešų health bars

5. **Papildomos lygio detalės**
   - Judančios platformos (2 tipai su skirtingais greičiais)
   - Statinės platformos skirtinguose aukščiuose
   - Ilgas žaidimo pasaulis su įvairiais iššūkiais

6. **Papildomos funkcijos**
   - Victory ekranas su galutiniais rezultatais
   - Game Over ekranas
   - Restart funkcionalumas
   - Smooth camera following
   - Žaidėjo animacija (5 frame'ai)
   - Priešų AI su patrol sistema

## Techniniai detaliai

- **Kalba:** Python 3.x
- **Framework:** Pygame
- **Ekrano rezoliucija:** 1250x800
- **FPS:** 60
- **Pasaulio dydis:** 3000x800 pikselių
- **Objektų skaičius:** 20+ loot, 7 priešai, 15+ platformų

## Žaidimo statistika

- **Maksimalus score:** Neribojamas
- **Priešų tipai:** 2 (žeminiai, skraidantys)
- **Loot tipai:** 3 (monetos, kristalai, širdys)
- **Platformų tipai:** 2 (statinės, judančios)
- **Gyvybės:** 5 (max)
