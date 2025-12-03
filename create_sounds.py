"""
Paprastas skriptas garso failų sukūrimui.
Paleiskite šį skriptą, kad sukurtumėte pagrindinius garso efektus.
"""
import pygame
import numpy as np
import os

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

def create_sound(frequency, duration, volume=0.5):
    """Sukuria paprastą sinuso bangos garsą"""
    sample_rate = 22050
    n_samples = int(duration * sample_rate)
    
    # Sukuriame sinuso bangą
    t = np.linspace(0, duration, n_samples, False)
    wave = np.sin(frequency * t * 2 * np.pi)
    
    # Pridedame fade out
    fade_samples = int(0.1 * sample_rate)
    fade = np.ones(n_samples)
    fade[-fade_samples:] = np.linspace(1, 0, fade_samples)
    wave = wave * fade
    
    # Konvertuojame į 16-bit
    wave = (wave * volume * 32767).astype(np.int16)
    
    # Stereo
    stereo_wave = np.column_stack((wave, wave))
    
    return pygame.sndarray.make_sound(stereo_wave)

def create_jump_sound():
    """Šuolio garsas - kylanti tonacija"""
    sample_rate = 22050
    duration = 0.2
    n_samples = int(duration * sample_rate)
    
    t = np.linspace(0, duration, n_samples, False)
    freq = np.linspace(200, 600, n_samples)
    wave = np.sin(2 * np.pi * freq * t / sample_rate)
    
    # Fade out
    fade = np.linspace(1, 0, n_samples)
    wave = wave * fade * 0.3
    
    wave = (wave * 32767).astype(np.int16)
    stereo_wave = np.column_stack((wave, wave))
    
    return pygame.sndarray.make_sound(stereo_wave)

def create_collect_sound():
    """Surinkimo garsas - trumpas aukštas tonas"""
    sample_rate = 22050
    duration = 0.15
    n_samples = int(duration * sample_rate)
    
    t = np.linspace(0, duration, n_samples, False)
    wave = np.sin(2 * np.pi * 800 * t) + 0.5 * np.sin(2 * np.pi * 1200 * t)
    
    fade = np.linspace(1, 0, n_samples)
    wave = wave * fade * 0.25
    
    wave = (wave * 32767).astype(np.int16)
    stereo_wave = np.column_stack((wave, wave))
    
    return pygame.sndarray.make_sound(stereo_wave)

def create_shoot_sound():
    """Šaudymo garsas - žemas sprogimas"""
    sample_rate = 22050
    duration = 0.25
    n_samples = int(duration * sample_rate)
    
    t = np.linspace(0, duration, n_samples, False)
    freq = np.linspace(400, 100, n_samples)
    wave = np.sin(2 * np.pi * freq * t / sample_rate)
    
    # Pridedame triukšmą
    noise = np.random.normal(0, 0.1, n_samples)
    wave = wave * 0.7 + noise * 0.3
    
    fade = np.linspace(1, 0, n_samples)
    wave = wave * fade * 0.3
    
    wave = (wave * 32767).astype(np.int16)
    stereo_wave = np.column_stack((wave, wave))
    
    return pygame.sndarray.make_sound(stereo_wave)

def create_hit_sound():
    """Smūgio garsas - žemas dūžis"""
    sample_rate = 22050
    duration = 0.2
    n_samples = int(duration * sample_rate)
    
    t = np.linspace(0, duration, n_samples, False)
    wave = np.sin(2 * np.pi * 150 * t) + 0.5 * np.sin(2 * np.pi * 80 * t)
    
    # Triukšmas
    noise = np.random.normal(0, 0.2, n_samples)
    wave = wave * 0.6 + noise * 0.4
    
    fade = np.linspace(1, 0, n_samples)
    wave = wave * fade * 0.35
    
    wave = (wave * 32767).astype(np.int16)
    stereo_wave = np.column_stack((wave, wave))
    
    return pygame.sndarray.make_sound(stereo_wave)

def create_background_music():
    """Paprasta foninė muzika"""
    sample_rate = 22050
    duration = 10  # 10 sekundžių loop
    n_samples = int(duration * sample_rate)
    
    t = np.linspace(0, duration, n_samples, False)
    
    # Kelios harmonijos
    wave = (np.sin(2 * np.pi * 220 * t) * 0.2 +  # A
            np.sin(2 * np.pi * 277 * t) * 0.15 +  # C#
            np.sin(2 * np.pi * 330 * t) * 0.15 +  # E
            np.sin(2 * np.pi * 110 * t) * 0.1)    # Bass A
    
    # Pridedame lėtą moduliaciją
    modulation = np.sin(2 * np.pi * 0.5 * t) * 0.3 + 0.7
    wave = wave * modulation * 0.15
    
    wave = (wave * 32767).astype(np.int16)
    stereo_wave = np.column_stack((wave, wave))
    
    return pygame.sndarray.make_sound(stereo_wave)

# Sukuriame sounds katalogą jei jo nėra
if not os.path.exists('sounds'):
    os.makedirs('sounds')

print("Kuriami garso failai...")

# Sukuriame garsus
jump = create_jump_sound()
collect = create_collect_sound()
shoot = create_shoot_sound()
hit = create_hit_sound()
background = create_background_music()

# Išsaugome
pygame.mixer.Sound.play(jump)
pygame.time.wait(300)
pygame.mixer.Sound(buffer=jump.get_raw()).play()
pygame.mixer.Sound(buffer=jump.get_raw()).play()

try:
    # Bandome išsaugoti kaip WAV
    import wave
    import struct
    
    def save_sound(sound, filename):
        """Išsaugo pygame Sound kaip WAV failą"""
        raw = pygame.sndarray.array(sound)
        sample_rate = 22050
        
        with wave.open(filename, 'w') as wav_file:
            wav_file.setnchannels(2)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            
            for frame in raw:
                wav_file.writeframes(struct.pack('<hh', int(frame[0]), int(frame[1])))
    
    save_sound(jump, 'sounds/jump.wav')
    save_sound(collect, 'sounds/collect.wav')
    save_sound(shoot, 'sounds/shoot.wav')
    save_sound(hit, 'sounds/hit.wav')
    
    # Background music kaip MP3 (tiesiog išsaugome kaip WAV)
    save_sound(background, 'sounds/background.wav')
    
    # Pervadiname į mp3 (arba tiesiog naudosime wav)
    import shutil
    shutil.copy('sounds/background.wav', 'sounds/background.mp3')
    
    print("✓ Garso failai sukurti sėkmingai!")
    print("  - sounds/jump.wav")
    print("  - sounds/collect.wav")
    print("  - sounds/shoot.wav")
    print("  - sounds/hit.wav")
    print("  - sounds/background.mp3")
    
except Exception as e:
    print(f"Klaida kuriant failus: {e}")
    print("Bandykite įdiegti numpy: pip install numpy")

pygame.quit()
