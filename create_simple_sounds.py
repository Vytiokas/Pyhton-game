"""
Paprastas būdas sukurti garso failus be numpy.
Sukuria tuščius placeholder failus, kad žaidimas veiktų be klaidų.
"""
import os
import wave
import struct
import math

def create_simple_wav(filename, frequency, duration, sample_rate=22050):
    """Sukuria paprastą WAV failą su sinuso banga"""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        num_samples = int(sample_rate * duration)
        
        for i in range(num_samples):
            # Sinuso banga
            value = int(32767 * 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate))
            # Fade out
            if i > num_samples * 0.7:
                fade = 1 - (i - num_samples * 0.7) / (num_samples * 0.3)
                value = int(value * fade)
            wav_file.writeframes(struct.pack('<h', value))

# Sukuriame sounds katalogą
if not os.path.exists('sounds'):
    os.makedirs('sounds')

print("Kuriami garso failai...")

# Sukuriame paprastus garsus
create_simple_wav('sounds/jump.wav', 440, 0.2)  # A note
create_simple_wav('sounds/collect.wav', 880, 0.15)  # High A
create_simple_wav('sounds/shoot.wav', 220, 0.25)  # Low A
create_simple_wav('sounds/hit.wav', 110, 0.2)  # Very low A
create_simple_wav('sounds/background.mp3', 330, 5.0)  # E note (ilgesnis)

print("✓ Garso failai sukurti!")
print("  - sounds/jump.wav")
print("  - sounds/collect.wav")
print("  - sounds/shoot.wav")
print("  - sounds/hit.wav")
print("  - sounds/background.mp3")
print("\nDabar galite paleisti žaidimą: python main.py")
