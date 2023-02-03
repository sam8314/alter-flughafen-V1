from pygame.math import Vector2
# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

#colours
MIDGREEN =(43.1, 58.8, 48.6)
DEEPGREEN =(37.3, 47.8, 47.5)
LIGHTGREEN =(76.1, 87.8, 60.4)

def FORMAT(strg):
	#fix pair OF red/purple mushroom
	res =''
	for char in strg:
		if char == '_':
			res+=' '
		else:
			res+= char
	return(res)

SPECIES = ['small_tree',
			'large_tree',
			'bush',
			'sunflower',
			'pink_flower',
			'blue_flower',
			'single_purple_mushroom',
			'pair_purple_mushroom',
			'single_red_mushroom',
			'pair_red_mushroom']

SPECIES_TILES = ['Small', 
				'Large', 
				'Bush', 
				'Sunflower', 
				'Pink_flower', 
				'Blue_flower', 
				'One_purple_mushroom',
				'Two_purple_mushrooms',
				'One_red_mushroom',
				'Two_red_mushrooms']

# overlay positions 
OVERLAY_POSITIONS = {
	'tool' : (40, SCREEN_HEIGHT - 15)
	}

PLAYER_TOOL_OFFSET = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}

LAYERS = {
	'water': 0,
	'ground': 1,
	'soil': 2,
	'soil water': 3,
	'rain floor': 4,
	'house bottom': 5,
	'ground plant': 6,
	'main': 7,
	'house top': 8,
	'fruit': 9,
	'rain drops': 10
}

TOOLS = ['glass', 'binoculars']

'''
APPLE_POS = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

GROW_SPEED = {
	'corn': 1,
	'tomato': 0.7
}

SALE_PRICES = {
	'wood': 4,
	#'apple': 2,
	'corn': 10,
	'tomato': 20
}
PURCHASE_PRICES = {
	'corn': 4,
	'tomato': 5
}'''