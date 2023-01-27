import sys
import pygame
from settings import *

class Stack2:
    def __init__(self):
        self.elements = []

    def push(self, data):
        self.elements.append(data)

    def pop(self):
        if self.is_empty():
            return []

        elif self.get_size() == 1:
            result = self.peek
            self = []
            return result

        else:
            return self.elements.pop()
    
    def peek(self):
        if not self.is_empty():
            return self.elements[-1]
    
    def is_empty(self):
        return len(self.elements) == 0

    def is_here(self, value):
        return (value in self.convert_list())         

    def get_size(self):
        return len(self.elements)

    def print_all(self):
        for element in self.elements:
            print(element+' ')
        print(str(self.get_size()))

    def partition(self, groupsize):
        #returns a list of groupsize lists with the elements from self in the same order
        #doesn't alter self
        result = []
        stack_copy = [element for element in self.elements]

        for i in range(0, len(stack_copy), groupsize):
            result.append(stack_copy[i:i+groupsize])

        return result

    def return_element(self, index):
        list = self.convert_list()
        return list[index]

    def convert_list(self):
        res = []
        for element in self.elements:
            res.append(element)
        return res
        
class DisplayInventory(pygame.sprite.Sprite):
    def __init__(self, wiki):
        pygame.sprite.Sprite.__init__(self)
        self.display_surface = pygame.display.get_surface()
        self.in_inventory_menu = True
        self.hasnt_opened_invent = True
        self.default_slide = 0
        self.sel_species_wiki = None

        self.font_big = pygame.font.Font('../font/LycheeSoda.ttf', 70)
        self.font_small = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.font_smaller = pygame.font.Font('../font/LycheeSoda.ttf', 20)

        self.wiki = wiki

        if self.hasnt_opened_invent:
            self.known_species = Stack2()

    def display_inventory_info(self, nb_known_species, player_xp):
        #text
        title_text_surf = self.font_big.render('Welcome to your species dictionary', False, 'White')
        title_text_rect = title_text_surf.get_rect(center = (640, 120))

        lvl = self.get_player_level(player_xp)
        stats_text_strg = 'You have discovered '+str(nb_known_species)+' species and you are at level '+str(lvl)
        stats_text_surf = self.font_small.render(stats_text_strg, False, 'White')
        stats_text_rect = title_text_surf.get_rect(center = (640, 220))

        exit_text_surf = self.font_small.render('Press Q to exit inventory', False, 'Grey')
        exit_text_rect = exit_text_surf.get_rect(center = (640, 620))        

        #display
        pygame.draw.rect(self.display_surface, MIDGREEN, pygame.Rect(40,40,1200,640))#big background
        pygame.draw.rect(self.display_surface, 'white', pygame.Rect(50,50,1180,620), 5)#white border

        self.display_surface.blit(title_text_surf, title_text_rect)
        self.display_surface.blit(exit_text_surf, exit_text_rect)
        self.display_surface.blit(stats_text_surf, stats_text_rect)

    def format_species_name_string(self, strg):
        res =''
        for char in strg:
            if char == '_':
                res+=' '
            else:
                res+= char
        return(res)
    
    def display_species_slide(self, j, known_species_stack, well_known_species):
        split_stack = known_species_stack.partition(5)
        slide_index = [j for j in range(0, len(split_stack))]

        i = 0
        pygame.draw.rect(self.display_surface, MIDGREEN, pygame.Rect(100, 240, 1090, 320))

        for species in split_stack[j]:
            width_i = 100 + i*220
            pygame.draw.rect(self.display_surface, 'Grey', pygame.Rect(width_i, 240, 200, 320), border_radius=10) #background canvas

            #name of species :
            name_species_i_surf = self.font_smaller.render(self.format_species_name_string(species), False, 'Black')
            name_species_i_rect = name_species_i_surf.get_rect(center = (width_i+100, 530))

            #icon of species
            icon_i = pygame.image.load('../graphics/species/'+species+'.png').convert_alpha()            
            icon_i_rect = icon_i.get_rect(midbottom =(width_i + 100, 400))

            #more info button
            if well_known_species.is_here(species):
                pygame.draw.rect(self.display_surface, 'White', pygame.Rect(width_i + 30, 480, 140, 25), border_radius=10)
                more_info_surf = self.font_smaller.render('read more', False, 'Grey')
                more_info_rect = more_info_surf.get_rect(center = (width_i + 100, 493))                

                #hover animation more info button
                mouse_pos = pygame.mouse.get_pos()
                if pygame.Rect(width_i + 30, 480, 140, 25).collidepoint(mouse_pos):
                    pygame.draw.rect(self.display_surface, 'Grey', pygame.Rect(width_i + 30, 480, 140, 25), border_radius=10)
                    more_info_surf = self.font_smaller.render('read more', False, 'White')
                    more_info_rect = more_info_surf.get_rect(center = (width_i +100, 493))

                self.display_surface.blit(more_info_surf, more_info_rect)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.sel_species_wiki = species
                        self.wiki.in_menu = True

            #display
            self.display_surface.blit(name_species_i_surf, name_species_i_rect)
            self.display_surface.blit(icon_i, icon_i_rect)

            i+=1

        #next slide arrow button
        if not j == slide_index[-1]: #if we're not on the last slide
            pygame.draw.rect(self.display_surface, 'White', pygame.Rect(1190, 400,20, 20), border_radius = 10)
            right_arrow_surf = self.font_small.render(' > ', False, 'Black')
            right_arrow_rect = right_arrow_surf.get_rect(center = (1200,410))
            self.display_surface.blit(right_arrow_surf, right_arrow_rect)

        #hover animation for the next slide button
        if not j == slide_index[-1]: #if we're not on the last slide
            mouse_pos = pygame.mouse.get_pos()
            if pygame.Rect(1200, 410,10, 10).collidepoint(mouse_pos):
                pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(1190, 400,20, 20), border_radius = 15)
                right_arrow_surf = self.font_small.render(' > ', False, 'White')
                right_arrow_rect =right_arrow_surf.get_rect(center = (1200, 410))
                self.display_surface.blit(right_arrow_surf, right_arrow_rect)

        #previous slide arrow button
        if not j == slide_index[0]: #if we're not on the first slide
            pygame.draw.rect(self.display_surface, 'White', pygame.Rect(70, 400,20, 20), border_radius = 10)
            right_arrow_surf = self.font_small.render(' < ', False, 'Black')
            right_arrow_rect = right_arrow_surf.get_rect(center = (80,410))
            self.display_surface.blit(right_arrow_surf, right_arrow_rect)

        #hover animation for the next slide button
        if not j == slide_index[0]: #if we're not on the last slide
            mouse_pos = pygame.mouse.get_pos()
            if pygame.Rect(80, 410,10, 10).collidepoint(mouse_pos):
                pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(70, 400,20, 20), border_radius = 15)
                right_arrow_surf = self.font_small.render(' < ', False, 'White')
                right_arrow_rect =right_arrow_surf.get_rect(center = (80, 410))
                self.display_surface.blit(right_arrow_surf, right_arrow_rect)

        slide_nb_surf = self.font_small.render('You are on slide number ' + str(j+1) + '/'+ str(slide_index[-1]+1), False, 'Grey')
        slide_nb_rect = slide_nb_surf.get_rect(center = (640, 600))

        self.display_surface.blit(slide_nb_surf, slide_nb_rect)

    def display_known_species(self, known_species_stack, well_known_species):      
        if not known_species_stack.is_empty():
            self.display_species_slide(self.default_slide, known_species_stack, well_known_species)               

            #click on arrow slides the caroussel
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(1200, 410,10, 10).collidepoint(mouse_pos):
                        self.default_slide += 1
                        self.display_species_slide(self.default_slide, known_species_stack, well_known_species)
                        
                    if pygame.Rect(80, 410,10, 10).collidepoint(mouse_pos):
                        self.default_slide -= 1
                        self.display_species_slide(self.default_slide, known_species_stack, well_known_species)
                if pygame.key.get_pressed()[pygame.K_q]:
                    self.in_inventory_menu = False

    def display_inventory_menu(self, known_species_stack, well_known_species, player_xp): #when i key is pressed
        self.hasnt_opened_invent = False
        size = known_species_stack.get_size()
        self.default_slide = 0
        while self.in_inventory_menu:
            if not self.wiki.in_menu:
                self.display_inventory_info(size, player_xp)
                self.display_known_species(known_species_stack, well_known_species)
                for event in pygame.event.get():
                    if pygame.key.get_pressed()[pygame.K_q]:
                            self.in_inventory_menu = False
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            else:
                self.wiki.display_wiki(self.sel_species_wiki)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()               
            
            pygame.display.update()

    def get_player_level(self, xp):
        if 0<=xp<100:
            return 0
        elif 100<=xp<200:
            return 1
        else:
            return 2

class EquipmentInventory(pygame.sprite.Sprite):
    def __init__(self, available_tools, possessed_tools):
        pygame.sprite.Sprite.__init__(self)
        self.display_surface = pygame.display.get_surface()
        self.in_inventory_menu = True
        self.hasnt_opened_invent = True
        self.possessed_tools = possessed_tools
        self.available_tools = available_tools

        self.nb_tools = self.possessed_tools.get_size()

        self.font_big = pygame.font.Font('../font/LycheeSoda.ttf', 70)
        self.font_small = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.font_smaller = pygame.font.Font('../font/LycheeSoda.ttf', 20)

        if self.hasnt_opened_invent:
            self.tools_inventory = Stack2()

    def display_inventory_info(self, nb_possessed_tools):
        #text
        title_text_surf = self.font_big.render('These are your tools', False, 'White')
        title_text_rect = title_text_surf.get_rect(center = (640, 120))

        stats_text_strg = 'You have '+str(nb_possessed_tools)+' tools'
        if nb_possessed_tools == 1:
            stats_text_strg = 'You have 1 tool'
        stats_text_surf = self.font_small.render(stats_text_strg, False, 'White')
        stats_text_rect = title_text_surf.get_rect(center = (640, 220))

        exit_text_surf = self.font_small.render('Press Q to exit inventory', False, 'Grey')
        exit_text_rect = exit_text_surf.get_rect(center = (640, 620))

        #display
        pygame.draw.rect(self.display_surface, LIGHTGREEN, pygame.Rect(40,40,1200,640))#big background
        pygame.draw.rect(self.display_surface, 'white', pygame.Rect(50,50,1180,620), 5)#white border

        self.display_surface.blit(title_text_surf, title_text_rect)
        self.display_surface.blit(exit_text_surf, exit_text_rect)
        self.display_surface.blit(stats_text_surf, stats_text_rect)
    
    def format_tool_name_string(self, strg):
        res =''
        for char in strg:
            if char == '_':
                res+=' '
            else:
                res+= char
        return(res)
    
    def display_inventory_menu(self, nb_possessed_tools): #when t key is pressed
        self.hasnt_opened_invent = False
        while self.in_inventory_menu:
            self.display_inventory_info(nb_possessed_tools)
            self.display_tools()
            
            for event in pygame.event.get():
                if pygame.key.get_pressed()[pygame.K_q]:
                        self.in_inventory_menu = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

    def display_tools(self):
        
        #glass
        pygame.draw.rect(self.display_surface, 'Grey', pygame.Rect(435, 240, 200, 320), border_radius=10) #background canvas

        #name of tool :
        name_tool_surf = self.font_smaller.render('glass', False, 'azure4')
        name_tool_rect = name_tool_surf.get_rect(center = (535, 530))

        #icon of tool
        icon_i = pygame.image.load('../graphics/tools/glass_grey.png').convert_alpha()   
        icon_i = pygame.transform.rotozoom(icon_i,0,1.2)         
        icon_i_rect = icon_i.get_rect(center =(535, 400))

        question_mark = pygame.image.load('../graphics/tools/question.png').convert_alpha()
        question_mark_rect = question_mark.get_rect(midbottom = (535, 420))

        if not self.available_tools.is_here('glass') and not self.possessed_tools.is_here('glass'):
            explanation_surf1 = self.font_smaller.render('you need level 1', False, 'azure4')
            explanation_rect1 = explanation_surf1.get_rect(center = (535, 260))
            explanation_surf2 = self.font_smaller.render('to unlock it', False, 'azure4')
            explanation_rect2 = explanation_surf2.get_rect(center = (535, 275))

            self.display_surface.blit(name_tool_surf, name_tool_rect)
            self.display_surface.blit(explanation_surf1, explanation_rect1)
            self.display_surface.blit(explanation_surf2, explanation_rect2)
            self.display_surface.blit(question_mark, question_mark_rect)

        elif self.available_tools.is_here('glass') and not self.possessed_tools.is_here('glass'):
            pygame.draw.rect(self.display_surface, 'White', pygame.Rect(465, 480, 140, 25), border_radius=10)
            available_surf = self.font_smaller.render('available', False, 'Grey')
            available_rect = available_surf.get_rect(center = (535, 493))                

            #hover animation more info button
            mouse_pos = pygame.mouse.get_pos()
            if pygame.Rect(465, 480, 140, 25).collidepoint(mouse_pos):
                pygame.draw.rect(self.display_surface, 'Grey', pygame.Rect(465, 480, 140, 25), border_radius=10)
                more_info_surf1 = self.font_smaller.render('go find it', False, 'White')
                more_info_rect1 = more_info_surf1.get_rect(center = (535, 478))
                more_info_surf2 = self.font_smaller.render('at the board', False, 'White')
                more_info_rect2 = more_info_surf2.get_rect(center = (535, 493))

                self.display_surface.blit(more_info_surf1, more_info_rect1)
                self.display_surface.blit(more_info_surf2, more_info_rect2)

            else:
                self.display_surface.blit(available_surf, available_rect)

            self.display_surface.blit(name_tool_surf, name_tool_rect)
            self.display_surface.blit(icon_i, icon_i_rect)

        elif self.possessed_tools.is_here('glass'):
            icon_i = pygame.image.load('../graphics/tools/glass.png').convert_alpha()   
            icon_i = pygame.transform.rotozoom(icon_i,0,1.2)                     

            #hover animation more info button
            mouse_pos = pygame.mouse.get_pos()
            if pygame.Rect(465, 480, 140, 25).collidepoint(mouse_pos):
                #pygame.draw.rect(self.display_surface, 'chartreuse3', pygame.Rect(465, 480, 140, 25), border_radius=10)
                more_info_surf = self.font_smaller.render('press SPACE to use it', False, 'White')
                more_info_rect = more_info_surf.get_rect(center = (535, 493))

            else:
                pygame.draw.rect(self.display_surface, 'White', pygame.Rect(465, 480, 140, 25), border_radius=10)
                more_info_surf = self.font_smaller.render('acquired', False, 'chartreuse3')
                more_info_rect = more_info_surf.get_rect(center = (535, 493))    

            self.display_surface.blit(more_info_surf, more_info_rect)
            self.display_surface.blit(name_tool_surf, name_tool_rect)
            self.display_surface.blit(icon_i, icon_i_rect)
        

        #binoculars
        pygame.draw.rect(self.display_surface, 'Grey', pygame.Rect(655, 240, 200, 320), border_radius=10) #background canvas

        #name of tool :
        name_tool_surf = self.font_smaller.render('binoculars', False, 'azure4')
        name_tool_rect = name_tool_surf.get_rect(center = (755, 530))

        #icon of tool
        icon_i = pygame.image.load('../graphics/tools/binoculars_grey.png').convert_alpha()  
        icon_i = pygame.transform.rotozoom(icon_i, 0, 1.3)          
        icon_i_rect = icon_i.get_rect(midbottom =(755, 440))

        question_mark = pygame.image.load('../graphics/tools/question.png').convert_alpha()
        question_mark_rect = question_mark.get_rect(midbottom = (755, 420))

        if not self.available_tools.is_here('binoculars') and not self.possessed_tools.is_here('binoculars'):
            explanation_surf1 = self.font_smaller.render('you need level 2', False, 'azure4')
            explanation_rect1 = explanation_surf1.get_rect(center = (755, 260))
            explanation_surf2 = self.font_smaller.render('to unlock it', False, 'azure4')
            explanation_rect2 = explanation_surf2.get_rect(center = (755, 275))

            self.display_surface.blit(name_tool_surf, name_tool_rect)
            self.display_surface.blit(explanation_surf1, explanation_rect1)
            self.display_surface.blit(explanation_surf2, explanation_rect2)
            self.display_surface.blit(question_mark, question_mark_rect)

        elif self.available_tools.is_here('binoculars') and not self.possessed_tools.is_here('binoculars'):
            pygame.draw.rect(self.display_surface, 'White', pygame.Rect(685, 480, 140, 25), border_radius=10)
            available_surf = self.font_smaller.render('available', False, 'Grey')
            available_rect = available_surf.get_rect(center = (755, 493))                

            #hover animation go find it button
            mouse_pos = pygame.mouse.get_pos()
            if pygame.Rect(685, 480, 140, 25).collidepoint(mouse_pos):
                pygame.draw.rect(self.display_surface, 'Grey', pygame.Rect(685, 480, 140, 25), border_radius=10)
                more_info_surf1 = self.font_smaller.render('go find it', False, 'White')
                more_info_rect1 = more_info_surf1.get_rect(center = (755, 478))
                more_info_surf2 = self.font_smaller.render('at the board', False, 'White')
                more_info_rect2 = more_info_surf2.get_rect(center = (755, 493))

                self.display_surface.blit(more_info_surf1, more_info_rect1)
                self.display_surface.blit(more_info_surf2, more_info_rect2)

            else:
                self.display_surface.blit(available_surf, available_rect)
            
            self.display_surface.blit(name_tool_surf, name_tool_rect)
            self.display_surface.blit(icon_i, icon_i_rect)

        elif self.possessed_tools.is_here('binoculars'):
            icon_i = pygame.image.load('../graphics/tools/binoculars.png').convert_alpha() 
            icon_i = pygame.transform.rotozoom(icon_i, 0, 1.3)  
            available_surf = self.font_smaller.render('acquired', False, 'chartreuse3')
            available_rect = available_surf.get_rect(center = (755, 493))                

            #hover animation more info button
            mouse_pos = pygame.mouse.get_pos()
            if pygame.Rect(685, 480, 140, 25).collidepoint(mouse_pos):
                #pygame.draw.rect(self.display_surface, 'chartreuse3', pygame.Rect(685, 480, 140, 25), border_radius=10)
                more_info_surf1 = self.font_smaller.render('Press SPACE', False, 'White')
                more_info_rect1 = more_info_surf1.get_rect(center = (755, 478))
                more_info_surf2 = self.font_smaller.render('to use them', False, 'White')
                more_info_rect2 = more_info_surf2.get_rect(center = (755, 493))

                self.display_surface.blit(more_info_surf1, more_info_rect1)
                self.display_surface.blit(more_info_surf2, more_info_rect2)

            else:
                pygame.draw.rect(self.display_surface, 'White', pygame.Rect(685, 480, 140, 25), border_radius=10)
                self.display_surface.blit(available_surf, available_rect)
            self.display_surface.blit(name_tool_surf, name_tool_rect)
            self.display_surface.blit(icon_i, icon_i_rect)




