import pygame


def sound_setup(address):
    pygame.mixer.init()
    pygame.mixer.music.load(address)
    return


def play_sound(address=None):
    if address == None:
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.load(address)
        pygame.mixer.music.play()

    return
