import pygame
import os

class AudioLoop():
    def __init__(self, file_paths):
        pygame.init()
        self.tracks = ['piano', 'bass', 'vocals', 'drums', 'guitar', 'other']
        if set(file_paths.keys()) != set(self.tracks):
            raise ValueError(f"file_paths dictionary must contain exactly these keys: {self.tracks}")
        pygame.mixer.set_num_channels(len(self.tracks))
        self.sounds = {track: self.load_sound(file_paths[track]) for track in self.tracks}
        
    def load_sound(self, file):
        sound = pygame.mixer.Sound(file)
        return sound
    
    def start(self):
        for track in self.tracks:
            self.sounds[track].play(loops=-1)
    
    def adjust_volumes(self, volume_dict):
        for track in self.tracks:
            if track in volume_dict:
                pygame.mixer.Channel(self.tracks.index(track)).set_volume(volume_dict[track])
