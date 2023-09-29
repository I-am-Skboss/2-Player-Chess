import pygame
pygame.init()
from Constants import *

#draw main board
def draw_board():
    for i in range(32):
        column = i%4
        row = i//4
        if row%2 ==0:
            pygame.draw.rect(screen,'bisque3', [480-(column*160), row*80,80,80])
        else:
            pygame.draw.rect(screen,'bisque3', [560-(column*160), row*80,80,80])
        pygame.draw.rect(screen, 'grey', [0,640, WIDTH, 80])
        pygame.draw.rect(screen, 'gold', [0,640, WIDTH, 80],4)
        pygame.draw.rect(screen, 'gold', [640,0, 160, HEIGHT],4)
        status_text = ["White: Select a valid piece to move!", "White: Select a valid destination!",
                       "Black: Select a valid piece to move!", "Black Select a valid destination!"]
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (16,656))
        for i in range(9):
            pygame.draw.line(screen,"black",(0, 80*i), (640, 80*i), 2)
            pygame.draw.line(screen,"black",(80*i, 0), (80*i, 640), 2)
        screen.blit(big_font.render('FOREFIT', True, 'black'), (648, 665))    
        if white_promote or black_promote:
            pygame.draw.rect(screen, 'grey', [0,640, WIDTH, 80])
            pygame.draw.rect(screen, 'gold', [0,640, WIDTH, 80],4)
            screen.blit(big_font.render('Select peice to promote Pawn', True, 'black'), (16,656))

#draw pieces in board

def def_pieces():
        for i in range(len(white_pieces)):
            index = piece_list.index(white_pieces[i])
            if white_pieces[i] == "pawn":
                screen.blit(white_pawn, (white_locations[i][0]* 80+10, white_locations[i][1] * 80 + 15))
            else:
                screen.blit(white_images[index], (white_locations[i][0]* 80+5, white_locations[i][1] * 80 + 6))
        for i in range(len(black_pieces)):
            index = piece_list.index(black_pieces[i])
            if black_pieces[i] == "pawn":
                screen.blit(black_pawn, (black_locations[i][0]* 80+10, black_locations[i][1] * 80 + 15))
            else:
                screen.blit(black_images[index], (black_locations[i][0]* 80+5, black_locations[i][1] * 80 + 6))
#function to check valid moves
def check_options(pieces,locations,turn):
    global casteling_moves
    moves_list = []
    all_moves_list = []
    casteling_moves = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == "pawn":
            moves_list = check_pawn(location,turn)
        elif piece == "rook":
            moves_list = check_rook(location,turn)
        elif piece == "knight":
            moves_list = check_knight(location,turn)
        elif piece == "bishop":
            moves_list = check_bishop(location,turn)
        elif piece == "queen":
            moves_list = check_queen(location,turn)
        elif piece == "king":
            moves_list, casteling_moves = check_king(location,turn)
        all_moves_list.append(moves_list)
    return all_moves_list

#check valid king moves
def check_king(position,color):
    moves_list = []
    castle_moves = check_casteling()
    if color=="white":
        friends_list = white_locations
    else:
        friends_list = black_locations
    # 8 squares to check for king 1 squares in any direction
    targets = [(1,0), (1,1), (1, -1), (-1, 0), (-1, 1), (-1,-1), (0, 1), (0, -1)]
    for i in range(8): # down, up, right, left
        target = (position[0] + targets[i][0], position[1]+ targets[i][1])
        if target not in friends_list and 0<= target[0] <= 7 and  0<= target[1] <= 7 :
            moves_list.append(target)
    return moves_list, castle_moves

#check valid queen moves
def check_queen(position,color):
    moves_list=check_bishop(position,color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list

#check valid bishop moves
def check_bishop(position,color):
    moves_list=[]
    if color=="white":
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations
    for i in range(4): # up- right, up- left,down- right,down- left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i==1:
            x = -1
            y = -1
        elif i==2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain*x), position[1]+ (chain*y)) not in friends_list and \
                    0<= position[0] + (chain*x) <= 7 and 0<= position[1]+ (chain*y) <= 7:
                moves_list.append((position[0]+ (chain*x), position[1]+ (chain*y)))
                if (position[0]+ (chain*x), position[1]+ (chain*y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False

    return moves_list

# checking rook positions
def check_rook(position, color):
    moves_list=[]
    if color=="white":
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations
    for i in range(4): # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x=0
            y=1
        elif i==1:
            x=0
            y=-1
        elif i==2:
            x=1
            y=0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain*x), position[1]+ (chain*y)) not in friends_list and \
                    0<= position[0] + (chain*x) <= 7 and 0<= position[1]+ (chain*y) <= 7:
                moves_list.append((position[0]+ (chain*x), position[1]+ (chain*y)))
                if (position[0]+ (chain*x), position[1]+ (chain*y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

#check valid pawn moves
def check_pawn(position,color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1]+1) not in white_locations and \
                (position[0], position[1]+1) not in black_locations and position[1]<7:
            moves_list.append((position[0], position[1]+1))
            if (position[0], position[1]+2) not in white_locations and \
                    (position[0], position[1]+2) not in black_locations and position[1] == 1:
                moves_list.append((position[0], position[1]+2))
        if (position[0]+1, position[1]+1) in black_locations:
            moves_list.append((position[0]+1, position[1]+1))
        if (position[0]-1, position[1]+1) in black_locations:
            moves_list.append((position[0]-1, position[1]+1))
        #add enn pessant
        if (position[0]+1, position[1]+1) == black_ep:
            moves_list.append((position[0]+1, position[1]+1))
        if (position[0]-1, position[1]+1) == black_ep:
            moves_list.append((position[0]-1, position[1]+1))
    else:
        if (position[0], position[1]-1) not in white_locations and \
                (position[0], position[1]-1) not in black_locations and position[1]>0:
            moves_list.append((position[0], position[1]-1))
            if (position[0], position[1]-2) not in white_locations and \
                    (position[0], position[1]-2) not in black_locations and position[1] == 6:
                moves_list.append((position[0], position[1]-2))
        if (position[0]+1, position[1]-1) in white_locations:
            moves_list.append((position[0]+1, position[1]-1))
        if (position[0]-1, position[1]-1) in white_locations:
            moves_list.append((position[0]-1, position[1]-1))
        if (position[0]+1, position[1]-1) == white_ep:
            moves_list.append((position[0]+1, position[1]-1))
        if (position[0]-1, position[1]-1) == white_ep:
            moves_list.append((position[0]-1, position[1]-1))
    return moves_list

#check valid knight moves
def check_knight(position,color):
    moves_list = []
    if color=="white":
        friends_list = white_locations
    else:
        friends_list = black_locations
    # 8 squares to check for knight 2 squares in 1 direction and 1 in another
    targets = [(1,2), (1,-2), (2, 1), (2, -1), (-1, 2), (-1,-2), (-2, 1), (-2, -1)]
    for i in range(8): # down, up, right, left
        target = (position[0] + targets[i][0], position[1]+ targets[i][1])
        if target not in friends_list and 0<= target[0] <= 7 and  0<= target[1] <= 7 :
            moves_list.append(target)
    return moves_list

#check valid moves only for selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


#draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 80 + 40, moves[i][1] * 80 + 40), 5)

#draw captured pieces on screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (650, 6+40*i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (725, 6+40*i))

#draw a flashing square around kind if in check
def draw_check():
    global check
    check = False
    if turn_step<2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    check = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'grey', [white_locations[king_index][0]*80+1,
                                                          white_locations[king_index][1]*80+1, 80, 80], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    check = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark green', [black_locations[king_index][0]*80+1,
                                                                black_locations[king_index][1]*80+1, 80, 80], 5)

#define game over
def draw_game_over():
    pygame.draw.rect(screen, 'black', [160, 160, 320, 56])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (166, 166))
    screen.blit(font.render(f'Press ENTER to Restart', True, 'white'), (166, 192))

#enn passant move code
def check_ep(old_coord, new_coord):
    if turn_step<= 1:
        index = white_locations.index(old_coord)
        ep_coords = (new_coord[0], new_coord[1]-1)
        piece = white_pieces[index]
    else:
        index = black_locations.index(old_coord)
        ep_coords = (new_coord[0], new_coord[1]+1)
        piece = black_pieces[index]
    if piece == 'pawn' and abs(old_coord[1]- new_coord[1])>1:
        pass
    else:
        ep_coords = (80,80)
    return ep_coords

# check casteling availibility
def check_casteling():
#king must not be in check, rook and king haven't moved previously, nothing between and king doesn't pass through or ends on attacked spot
    castle_moves = [] # store each valid castle moves as [((king_coords), castle_coords)]
    rook_indexes = []
    rook_locations = []
    king_index = 0
    king_pos = (0,0)
    if turn_step > 1:
        for i in range(len(white_pieces)):
            if white_pieces[i] == "rook":
                rook_indexes.append(white_moved[i])
                rook_locations.append(white_locations[i])
            if white_pieces[i] == "king":
                king_index = i
                king_pos = white_locations[i]
        if not white_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True
                if rook_locations[i][0] > king_pos[0]:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                      (king_pos[0] + 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]    
                for j in range(len(empty_squares)):
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or\
                            empty_squares[j] in black_options or rook_indexes[i]:
                        castle= False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    else:
        for i in range(len(black_pieces)):
            if black_pieces[i] == "rook":
                rook_indexes.append(black_moved[i])
                rook_locations.append(black_locations[i])
            if black_pieces[i] == "king":
                king_index = i
                king_pos = black_locations[i]
        if not black_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True
                if rook_locations[i][0] > king_pos[0]:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                      (king_pos[0] + 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]    
                for j in range(len(empty_squares)):
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or\
                            empty_squares[j] in white_options or rook_indexes[i]:
                        castle= False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    return castle_moves

def draw_casteling(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0][0] * 80 + 40, moves[i][0][1] * 80 + 56), 7)
        screen.blit(font.render('king', True, 'black'), (moves[i][0][0] * 80 +24, moves[i][0][1] * 80 + 56))
        pygame.draw.circle(screen, color, (moves[i][1][0] * 80 + 40, moves[i][1][1] * 80 + 56), 7)
        screen.blit(font.render('rook', True, 'black'), (moves[i][1][0] * 80 +24, moves[i][1][1] * 80 + 56))
        pygame.draw.circle(screen, color, (moves[i][0][0] * 80 + 40, moves[i][0][1] * 80 + 56), 2)
                                        
#pawn promotions checking
def check_promotion():
    pawn_indexes = []
    white_promotion = False
    black_promotion = False
    promote_index = 80
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if white_locations[pawn_indexes[i]][1] == 7:
            white_promotion = True
            promote_index = pawn_indexes[i]
    pawn_indexes = []
    for i in range(len(black_pieces)):
        if black_pieces[i] == 'pawn':
            pawn_indexes.append(i)
    for i in range(len(pawn_indexes)):
        if black_locations[pawn_indexes[i]][1] == 0:
            black_promotion = True
            promote_index = pawn_indexes[i]
    return white_promotion, black_promotion, promote_index

def draw_promotion():
    pygame.draw.rect(screen, 'dark grey', [640, 0 , 160, 336])
    if white_promote:
        color = "white"
        for i in range(len(white_promotions)):
            piece = white_promotions[i]
            index = piece_list.index(piece)
            screen.blit(white_images[index], (688, 4 + 80 * i))
    elif black_promote:
        color = "black"
        for i in range(len(black_promotions)):
            piece = black_promotions[i]
            index = piece_list.index(piece)
            screen.blit(black_images[index], (688, 4 + 80 * i))
    pygame.draw.rect(screen, color, [640, 0 , 160, 336], 7)

def check_promo_select():
    mouse_pos= pygame.mouse.get_pos()
    left_click= pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0]//80
    y_pos = mouse_pos[1]//80
    if white_promote and left_click and x_pos > 7 and y_pos < 4 :
        white_pieces[promo_index] = white_promotions[y_pos]
    elif black_promote and left_click and x_pos > 7 and y_pos < 4 :
        black_pieces[promo_index] = black_promotions[y_pos]   

#main game loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter +=1
    else:
        counter = 0
    screen.fill('chocolate4')
    draw_board()
    def_pieces()
    draw_captured()
    draw_check()
    if not game_over:
        white_promote, black_promote, promo_index = check_promotion()
        if white_promote or black_promote:
            draw_promotion()
            check_promo_select()
    if selection!=80:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
        if selected_piece == "king":
            draw_casteling(casteling_moves)
    #event handeling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1 and not game_over:
            x_coord = event.pos[0] //80
            y_coord = event.pos[1] //80
            click_coord = (x_coord, y_coord)
            if turn_step <= 1:
                if click_coord == (8,8) or click_coord == (9,8):
                    winner = 'black'
                if click_coord in white_locations:
                    selection = white_locations.index(click_coord)
                    # if selected piece is king or rook casteling opTion enables
                    selected_piece = white_pieces[selection]
                    if turn_step == 0:
                        turn_step = 1
                if click_coord in valid_moves and selection != 80:
                    white_ep = check_ep(white_locations[selection], click_coord)
                    white_locations[selection] = click_coord
                    white_moved[selection] = True
                    if click_coord in black_locations:
                        black_piece = black_locations.index(click_coord)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                        black_moved.pop(black_piece)
                    if click_coord == black_ep:
                        black_piece = black_locations.index((black_ep[0], black_ep[1]-1))
                        captured_pieces_white.append(black_pieces[black_piece])
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                        black_moved.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 80
                    valid_moves = []
                # add an option to castle
                elif selection != 80 and selected_piece == 'king':
                    for q in range(len(casteling_moves)):
                        if click_coord == casteling_moves[q][0]:
                            white_locations[selection] = click_coord
                            white_moved[selection] = True
                            if click_coord == (1,0):
                                rook_coords = (0,0)
                            else:
                                rook_coords = (7,0)
                            rook_index = white_locations.index(rook_coords)
                            white_locations[rook_index] = casteling_moves[q][1]
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            turn_step = 2
                            selection = 80
                            valid_moves = []
            if turn_step > 1:
                if click_coord == (8,8) or click_coord == (9,8):
                    winner = 'white'
                if click_coord in black_locations:
                    selection = black_locations.index(click_coord)
                    # if selected piece is king or rook casteling opTion enables
                    selected_piece = black_pieces[selection]
                    if turn_step == 2:
                        turn_step = 3
                if click_coord in valid_moves and selection != 80:
                    black_ep = check_ep(black_locations[selection], click_coord)
                    black_locations[selection] = click_coord
                    black_moved[selection] = True
                    if click_coord in white_locations:
                        white_piece = white_locations.index(click_coord)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                        white_moved.pop(white_piece)
                    if click_coord == white_ep:
                        white_piece = white_locations.index((white_ep[0], white_ep[1]+1))
                        captured_pieces_black.append(white_pieces[white_piece])
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                        white_moved.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 80
                    valid_moves = []
                # add an option to castle
                elif selection != 80 and selected_piece == 'king':
                    for q in range(len(casteling_moves)):
                        if click_coord == casteling_moves[q][0]:
                            black_locations[selection] = click_coord
                            black_moved[selection] = True
                            if click_coord == (1,7):
                                rook_coords = (0,7)
                            else:
                                rook_coords = (7,7)
                            rook_index = black_locations.index(rook_coords)
                            black_locations[rook_index] = casteling_moves[q][1]
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            turn_step = 0
                            selection = 80
                            valid_moves = []
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces= ["rook","knight","bishop","king","queen","bishop","knight","rook",
                               "pawn","pawn","pawn","pawn","pawn","pawn","pawn","pawn"]
                white_locations = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),
                                   (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1)]
                white_moved = [False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False]

                black_pieces= ["rook","knight","bishop","king","queen","bishop","knight","rook",
                            "pawn","pawn","pawn","pawn","pawn","pawn","pawn","pawn"]
                black_locations = [(0,7),(1,7),(2,7),(3,7),(4,7),(5,7),(6,7),(7,7),
                                   (0,6),(1,6),(2,6),(3,6),(4,6),(5,6),(6,6),(7,6)]
                black_moved = [False, False, False, False, False, False, False, False,
                               False, False, False, False, False, False, False, False]

                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 80
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
    
    if winner!= '':
        game_over = True
        draw_game_over()
    pygame.display.flip()
pygame.quit()

