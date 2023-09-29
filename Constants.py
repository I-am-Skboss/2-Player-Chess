import pygame
pygame.init()
WIDTH = 800
HEIGHT = 720
screen = pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption("2 player chess")
font = pygame.font.Font("freesansbold.ttf",16)
big_font = pygame.font.Font("freesansbold.ttf",34)
timer = pygame.time.Clock()
fps = 60
#game variables and images are ahead
white_pieces= ["rook","knight","bishop","king","queen","bishop","knight","rook",
               "pawn","pawn","pawn","pawn","pawn","pawn","pawn","pawn"]
white_locations = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
                   (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]

black_pieces= ["rook","knight","bishop","king","queen","bishop","knight","rook",
               "pawn","pawn","pawn","pawn","pawn","pawn","pawn","pawn"]
black_locations = [(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),
                   (0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)]

captured_pieces_white = []
captured_pieces_black = []
'''0=white turn no selection
1=white turn piece selected
2=black turn no selection
3=black turn piece selected
'''
turn_step = 0
selection = 80
valid_moves = []

#loaded in game pieces
black_queen = pygame.image.load("Images/black king.png")
black_queen = pygame.transform.scale(black_queen,(70,70))
black_small_queen = pygame.transform.scale(black_queen,(35,35))
black_king = pygame.image.load("Images/black queen.png")
black_king = pygame.transform.scale(black_king,(70,70))
black_small_king = pygame.transform.scale(black_king,(35,35))
black_rook = pygame.image.load("Images//black rook.png")
black_rook = pygame.transform.scale(black_rook,(70,70))
black_small_rook = pygame.transform.scale(black_rook,(35,35))
black_bishop = pygame.image.load("Images/black bishop.png")
black_bishop = pygame.transform.scale(black_bishop,(70,70))
black_small_bishop = pygame.transform.scale(black_bishop,(35,35))
black_knight = pygame.image.load("Images/black knight.png")
black_knight = pygame.transform.scale(black_knight,(70,70))
black_small_knight = pygame.transform.scale(black_knight,(35,35))
black_pawn = pygame.image.load("Images/black pawn.png")
black_pawn = pygame.transform.scale(black_pawn,(58,58))
black_small_pawn = pygame.transform.scale(black_pawn,(28,28))

white_queen = pygame.image.load("Images/white king.png")
white_queen = pygame.transform.scale(white_queen,(70,70))
white_small_queen = pygame.transform.scale(white_queen,(35,35))
white_king = pygame.image.load("Images/white queen.png")
white_king = pygame.transform.scale(white_king,(70,70))
white_small_king = pygame.transform.scale(white_king,(35,35))
white_rook = pygame.image.load("Images/white rook.png")
white_rook = pygame.transform.scale(white_rook,(70,70))
white_small_rook = pygame.transform.scale(white_rook,(35,35))
white_bishop = pygame.image.load("Images/white bishop.png")
white_bishop = pygame.transform.scale(white_bishop,(70,70))
white_small_bishop = pygame.transform.scale(white_bishop,(35,35))
white_knight = pygame.image.load("Images/white knight.png")
white_knight = pygame.transform.scale(white_knight,(70,70))
white_small_knight = pygame.transform.scale(white_knight,(35,35))
white_pawn = pygame.image.load("Images/white pawn.png")
white_pawn = pygame.transform.scale(white_pawn,(58,58))
white_small_pawn = pygame.transform.scale(white_pawn,(28,28))


white_images = [white_pawn, white_queen, white_king, white_knight,  white_rook, white_bishop]
white_promotions = ['bishop', 'knight', 'rook', 'queen']
white_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]
small_white_images = [white_small_pawn, white_small_queen, white_small_king, white_small_knight, 
                      white_small_rook, white_small_bishop]

black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
black_promotions = ['bishop', 'knight', 'rook', 'queen']
black_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]
small_black_images = [black_small_pawn, black_small_queen, black_small_king, black_small_knight, 
                      black_small_rook, black_small_bishop]
piece_list = ["pawn","king","queen","knight","rook","bishop"]
#check variables / flashing counter
counter = 0
winner = ''
game_over = False
white_ep = (80,80)
black_ep = (80,80)
white_promote = False
black_promote = False
promo_index = 80
check = False
casteling_moves = []