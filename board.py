import sys
import pygame 
from timer import Timer
from settings import *

class Board(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.display_surface = pygame.display.get_surface()
        self.in_board = True 
        self.hasnt_been_board = True
        self.player = player

        self.font_big = pygame.font.Font('../font/LycheeSoda.ttf', 70)
        self.font_small = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.font_smaller = pygame.font.Font('../font/LycheeSoda.ttf', 20)

    def run(self):
        self.hasnt_been_board = False
        timer = Timer(1300, activefunc = self.display_board)
        timer.activate()
        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                self.player.status = 'up_idle'
                self.player.sleep = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def display_board(self):
        #text
        explanation_text_surf = self.font_small.render(' Press ENTER to start a new day ', False, 'Black')
        explanation_text_rect = explanation_text_surf.get_rect(topleft = (30, 35))

        #display
        pygame.draw.rect(self.display_surface, 'White', explanation_text_rect)
        self.display_surface.blit(explanation_text_surf, explanation_text_rect)