import pygame
import os

class Sound:
    def __init__(self, path, volume=0.5):
        self.path = path
        try:
            pygame.mixer.init()  # Ensure mixer is initialized
            self.sound = pygame.mixer.Sound(path)
            self.sound.set_volume(volume)
        except Exception as e:
            print(f"Error loading sound {path}: {e}")
            self.sound = None

    def play(self):
        if self.sound:
            pygame.mixer.Sound.play(self.sound)