'''
SI 507 Fall 2018 Homework 1
'''

# Create board - Setup the data structure for storing board data

num2symbol = {0:" ",1:"X",2:"O"}
symbol2num = {" ":0,"X":1,"O":2}
location = {"NW":0, "N":1, "NE":2, "W":3, "C":4, "E":5, "SW":6, "S":7, "SE":8}

class BoardData(object):
    def __init__(self):
        self.data = [0,0,0,0,0,0,0,0,0]
    
    def update(self,Xmoves_next,next_move):
        if self.data[location[next_move]] != 0: # if the slot for next move is already occupied
            print("Illegal move!")
        else:
            self.data[location[next_move]] = 1 if Xmoves_next else 2
    
    def terminated(self):
        '''
        return True if the game should be terminated and False otherwise
        '''
        if all([value != 0 for value in self.data]):
            print(board_data)
            print("The game draws!")
            return True
        else:
            if self.data[1] != 0 and self.data[0] == self.data[1] and self.data[1] == self.data[2]:
                print(board_data)
                print(num2symbol[self.data[1]] + " wins!")
                return True
            if self.data[4] != 0 and self.data[3] == self.data[4] and self.data[4] == self.data[5]:
                print(board_data)
                print(num2symbol[self.data[4]] + " wins!")
                return True
            if self.data[7] != 0 and self.data[6] == self.data[7] and self.data[7] == self.data[8]:
                print(board_data)
                print(num2symbol[self.data[7]] + " wins!")
                return True
            if self.data[3] != 0 and self.data[0] == self.data[3] and self.data[3] == self.data[6]:
                print(board_data)
                print(num2symbol[self.data[3]] + " wins!")
                return True
            if self.data[4] != 0 and self.data[1] == self.data[4] and self.data[4] == self.data[7]:
                print(board_data)
                print(num2symbol[self.data[4]] + " wins!")
                return True
            if self.data[5] != 0 and self.data[2] == self.data[5] and self.data[5] == self.data[8]:
                print(board_data)
                print(num2symbol[self.data[5]] + " wins!")
                return True
            if self.data[4] != 0 and self.data[0] == self.data[4] and self.data[4] == self.data[8]:
                print(board_data)
                print(num2symbol[self.data[4]] + " wins!")
                return True
            if self.data[4] != 0 and self.data[2] == self.data[4] and self.data[4] == self.data[6]:
                print(board_data)
                print(num2symbol[self.data[4]] + " wins!")
                return True
            return False
            
    
    def __str__(self):
        return \
        "CURRENT BOARD:\n" +\
        " "+num2symbol[self.data[0]]+" | "+num2symbol[self.data[1]]+" | "+num2symbol[self.data[2]]+"\n" +\
        "-----------\n"+\
        " "+num2symbol[self.data[3]]+" | "+num2symbol[self.data[4]]+" | "+num2symbol[self.data[5]]+"\n" +\
        "-----------\n"+\
        " "+num2symbol[self.data[6]]+" | "+num2symbol[self.data[7]]+" | "+num2symbol[self.data[8]]

board_data = BoardData()


# Loop until game is over
while(True):

    # Step 1: Print board
    '''
    This function will take in current board data and print out the board in the console as shown 
    in the instructions.
    parameter: board_data - a data structure used for holding current moves on the board
    return: None
    '''
    def print_board(board_data):
        print (board_data)
    
    print_board(board_data)

    # Step 2: Determine who is going to have next move
    '''
    This function will take in current board data and decide who is going to have the next move
    (maybe based on the number of X-s and O-s on the board.)
    parameter: board_data - current board data
    return: a bool which is True if X moves next, and False if O moves next.
    '''
    def X_moves_next(board_data):
        Xmoves = board_data.data.count(1)
        Omoves = board_data.data.count(2)
        return True if Xmoves <= Omoves else False
        
    Xmoves_next = X_moves_next(board_data)

    # Step 3: Ask for the next move
    '''
    This function will take in the bool returned by X_moves_next(board_data), and asks for the next move.
    If the bool is True, "X's move > " should be printed out. Otherwise, "O's move > " should be printed out.
    A string chosen from "C","E","W","S","N","NW","NE","SW","SE" meaning the next move is in the 
    center, east, west, south, north, northwest, northeast, southwest, southeast is expected to be input.
    parameter: Xmoves_next - a bool which is True if X moves next, and False if O moves next.
    return: a string chosen from "C","E","W","S","N","NW","NE","SW",and "SE"
    '''
    def nextMove(Xmoves_next):
        symbol = "X" if Xmoves_next else "O" 
        return str(input(symbol + "'s move > "))

    next_move = nextMove(Xmoves_next)

    # Step 4: Check whether the move is illegal and update the board if legal
    '''
    This function will take in the string returned by nextMove(Xmoves_next). Then it will check if the move is valid.
    If it's not valid, the board will not be updated, and this move will be ignored, and the error will be printed out.
    Otherwise, update the board.
    parameter: Xmoves_next - a bool which is True if X moves next, and False if O moves next
               next_move - a string chosen from "C","E","W","S","N","NW","NE","SW",and "SE"
               board_data - current board data
    return: None
    '''
    def update(Xmoves_next,next_move,board_data):
        board_data.update(Xmoves_next,next_move)

    update(Xmoves_next,next_move,board_data)

    # Step 5: Determine if game is over
    '''
    Take in the current board data and determine if one player wins the game or the game draws. If the game is over,
    terminate the loop (and print out who wins or the game draws, and the final board), or continue the loop.
    parameter: board_data - current board data
    return: information about current game status, as a bool which is True if the game is over and False otherwise
    '''

    def determine_over(board_data):
        if board_data.terminated():
            exit()
    
    determine_over(board_data)
