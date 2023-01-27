import sys
import pygame
from settings import *

class Intromenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('A la découverte de Alter Flughafen')
        self.clock = pygame.time.Clock()

        self.font_big = pygame.font.Font('../font/LycheeSoda.ttf', 70)
        self.font_small = pygame.font.Font('../font/LycheeSoda.ttf', 30)

        self.leave_menu = False

        #status
        self.in_main = True
        self.in_info_rpk = False
        self.in_player = False

    def display_player_sel(self):
        background_rect = pygame.Rect(30, 30, 1220, 660)
        pygame.draw.rect(self.screen, MIDGREEN, background_rect,border_radius = 5)
        pygame.draw.rect(self.screen, 'White', background_rect, width = 5, border_radius=5) #border

        return_menu_surf = self.font_small.render(' Press M to return to the welcome menu ', False, 'Grey')
        return_menu_rect = return_menu_surf.get_rect(center = (640, 640))

        title_txt_surf = self.font_big.render(' Choose your avatar ', False, 'White')
        title_txt_rect = title_txt_surf.get_rect(center = (640, 140))

        #display
        self.screen.blit(return_menu_surf, return_menu_rect) 
        self.screen.blit(title_txt_surf, title_txt_rect)

    def display_info_rpk(self):
        background_rect = pygame.Rect(30, 30, 1220, 660)
        pygame.draw.rect(self.screen, LIGHTGREEN, background_rect,border_radius = 5)
        pygame.draw.rect(self.screen, 'White', background_rect, width = 5, border_radius=5) #border

        return_menu_surf = self.font_small.render(' Press M to return to the welcome menu ', False, 'Grey')
        return_menu_rect = return_menu_surf.get_rect(center = (640, 640))

        title_txt_surf = self.font_big.render(' Visit our website ! ', False, 'White')
        title_txt_rect = title_txt_surf.get_rect(center = (640, 140))

        #QR code
        code_surf = pygame.image.load('../graphics/menu/qr-code.png').convert_alpha()
        code_surf = pygame.transform.rotozoom(code_surf, 0,0.25)
        code_rect = code_surf.get_rect(center = (880,360))

        #link
        link_surf = self.font_small.render(' http://www.alter-flugplatz-karlsruhe.de/ ', False, 'White')
        link_rect = link_surf.get_rect(center =(400, 360))

        #display
        self.screen.blit(return_menu_surf, return_menu_rect)  
        self.screen.blit(title_txt_surf, title_txt_rect)
        self.screen.blit(code_surf, code_rect)
        self.screen.blit(link_surf, link_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if pygame.key.get_pressed()[pygame.K_m]:
                    self.in_main = True
                    self.in_info_rpk = False
                    self.in_player = False
                
                if self.in_info_rpk:
                    self.display_info_rpk()

                if self.in_player:
                    self.display_player_sel()

                if self.in_main:
                    self.screen.fill(DEEPGREEN)
                    
                    #text
                    welcome_txt_surf = self.font_big.render('Welcome to the Alter Flughafen', False, 'White')
                    welcome_txt_rect = welcome_txt_surf.get_rect(center = (640, 200))
            
                    txt_strgs = ['This game lets you explore the Alter Flughafen of Karlsruhe and its species.',
                                    'Your Species Dictionary starts empty and fills up when you discover a new species.',
                                    'Some equipment might be necessary to discover some species ',
                                    'You can find equipment once you have discovered enough species.',
                                    'Click on the tree or press ENTER to start the game. Viel Spaß !']
                    
                    #button tree
                    button_tree_surf = pygame.image.load('../graphics/menu/tree_medium_grey.png').convert_alpha()
                    button_tree_surf = pygame.transform.rotozoom(button_tree_surf, 0,1.3)
                    button_tree_rect = button_tree_surf.get_rect(center = (640,360))

                    #button website
                    logo_bw_surf = pygame.image.load('../graphics/menu/logo_bw_grey.png').convert_alpha()
                    logo_bw_surf = pygame.transform.rotozoom(logo_bw_surf, 0, 0.4)
                    logo_bw_rect = logo_bw_surf.get_rect(center = (900, 360))

                    #button player
                    player_surf = pygame.image.load('../graphics/menu/player_grey.png').convert_alpha()
                    player_surf = pygame.transform.rotozoom(player_surf, 0, 2)
                    player_rect = player_surf.get_rect(center = (390, 360))


                    #display
                    self.screen.blit(welcome_txt_surf, welcome_txt_rect)
                    self.screen.blit(button_tree_surf, button_tree_rect)
                    self.screen.blit(logo_bw_surf, logo_bw_rect)
                    self.screen.blit(player_surf, player_rect)

                    for i in range(0,5):
                        name_i = 'explanation_txt_strg'+str(i)
                        height = 480 + (i+1)*20
                        name_i_surf = self.font_small.render(txt_strgs[i], False, 'Grey')
                        name_i_rect = name_i_surf.get_rect(center =(640, height))
                        self.screen.blit(name_i_surf, name_i_rect)

                    mouse_pos = pygame.mouse.get_pos()
                    if button_tree_rect.collidepoint(mouse_pos):
                        tree_surf = pygame.image.load('../graphics/menu/tree_medium.png').convert_alpha()
                        tree_surf = pygame.transform.rotozoom(tree_surf, 0,1.3)
                        tree_rect = tree_surf.get_rect(center = (640,360))
                        self.screen.blit(tree_surf, tree_rect)
                    
                    if logo_bw_rect.collidepoint(mouse_pos):
                        logo_bw_surf = pygame.image.load('../graphics/menu/logo_bw.png').convert_alpha()
                        logo_bw_surf = pygame.transform.rotozoom(logo_bw_surf, 0, 0.4)
                        logo_bw_rect = logo_bw_surf.get_rect(center = (900, 360))
                        self.screen.blit(logo_bw_surf, logo_bw_rect)

                    if player_rect.collidepoint(mouse_pos):
                        player_surf = pygame.image.load('../graphics/menu/player.png').convert_alpha()
                        player_surf = pygame.transform.rotozoom(player_surf, 0, 2)
                        player_rect = player_surf.get_rect(center = (390, 360))
                        self.screen.blit(player_surf, player_rect)

                    if pygame.key.get_pressed()[pygame.K_RETURN]:
                        self.leave_menu = True
                        return self.leave_menu
                    
                    if event.type == pygame.MOUSEBUTTONDOWN: #mouse click
                            x, y = event.pos
                            if button_tree_rect.collidepoint(x, y):
                                self.leave_menu = True
                                return self.leave_menu
                            
                            if player_rect.collidepoint(x, y):
                                self.in_player = True 
                                self.in_main = False

                            if logo_bw_rect.collidepoint(x, y):
                                self.in_info_rpk = True 
                                self.in_main = False

            pygame.display.update()

             
