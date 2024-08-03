import pygame
import os
import time
from AudioLoop import AudioLoop
from OBDHandler import OBDHandler

SIMULATE_INPUTS = True

# Set up file paths for audio tracks
path = "./wavs/"
file_paths = {
    'piano': './wavs/piano.mp3',
    'bass': './wavs/bass.mp3',
    'vocals': './wavs/vocals.mp3',
    'drums': './wavs/drums.mp3',
    'guitar': './wavs/guitar.mp3',
    'other': './wavs/other.mp3'
}

# Initialize AudioLoop
loop = AudioLoop(file_paths)
loop.start()
initial_volumes = {
    'piano': 0.5,
    'bass': 0.7,
    'vocals': 0.8,
    'drums': 0.6,
    'guitar': 0.9,
    'other': 0.4
}
loop.adjust_volumes(initial_volumes)

# Initialize OBDHandler
handler = OBDHandler(SIMULATE_INPUTS)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("OBD Signal Simulator")
font = pygame.font.Font(None, 36)

def draw_text(text, pos):
    label = font.render(text, 1, (255, 255, 255))
    screen.blit(label, pos)

def draw_volume_curve():
    volumes = handler.get_volumes()
    y = 50
    for key, value in volumes.items():
        draw_text(f"{key}: {value:.2f}", (50, y))
        pygame.draw.line(screen, (0, 255, 0), (200, y + 15), (200 + value * 400, y + 15), 5)
        y += 50

def main():
    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        handler.simulate_accelerator(100)
                    elif event.key == pygame.K_DOWN:
                        handler.simulate_brake(100)
                    elif event.key == pygame.K_LEFT:
                        handler.simulate_steering('left', 100)
                    elif event.key == pygame.K_RIGHT:
                        handler.simulate_steering('right', 100)

            time.sleep(0.1)
            handler.refresh()
            volume_list = handler.get_volumes()
            loop.adjust_volumes(volume_list)

            screen.fill((0, 0, 0))
            draw_volume_curve()

            rpm_text = font.render(f'RPM: {handler.get_rpm()}', True, (255, 255, 255))
            speed_text = font.render(f'Speed: {handler.get_speed()}', True, (255, 255, 255))

            screen.blit(rpm_text, (50, 400))
            screen.blit(speed_text, (50, 450))

            pygame.display.flip()

    except KeyboardInterrupt:
        pygame.mixer.stop()
        pygame.quit()

if __name__ == "__main__":
    main()
