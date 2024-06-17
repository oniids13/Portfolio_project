board = ['-','-','-',
         '-','-','-',
         '-','-','-']

game_on = True
current_player = ""
def set_up_board():
    print(board[0] + '|' + board[1] + "|" + board[2] + '| -' + "[1|2|3]")
    print(board[3] + '|' + board[4] + '|' + board[5] + '| -' + "[4|5|6]")
    print(board[6] + '|' + board[7] + '|' + board[8] + '| -' + "[7|8|9]")

def select_player():
    global current_player
    current_player = input("Please choose: X or O \n")
    if current_player == "X":
        p1 = "X"
        p2 = "O"
        print(f"Player 1 is {p1} and Player 2 is {p2}")
    elif current_player == "O":
        p1 = "O"
        p2 = "X"
        print(f"Player 1 is {p1} and Player 2 is {p2}")
    else:
        print("Please select either 'X' or 'O' only.")
        play_game()



def check_position():
    global current_player
    print(f"Current Player is: {current_player}.")
    valid = False
    while not valid:
        move = int(input("Please enter a number on the grid(1-9): \n"))
        if move in range(1, 10):
            position = move - 1
            if "-" in board[position]:
                board[position] = current_player
                valid = True
            else:
                print("Already taken, please choose another grid.")
        else:
            print("Please select from 1-9 only.")

    set_up_board()



def play_game():
    print("Play tic-tac-toe!")
    set_up_board()
    select_player()

    while game_on:
        check_position()

        def check_to_win():
            global game_on
            if board[0] == board[1] == board[2] != "-":
                print(f"The winner is {board[0]}")
                game_on = False
            elif board[3] == board[4] == board[5] != "-":
                print(f"The winner is {board[3]}")
                game_on = False
            elif board[6] == board[7] == board[8] != "-":
                print(f"The winner is {board[6]}")
                game_on = False
            elif board[0] == board[3] == board[6] != "-":
                print(f"The winner is {board[0]}")
                game_on = False
            elif board[1] == board[4] == board[7] != "-":
                print(f"The winner is {board[1]}")
                game_on = False
            elif board[2] == board[5] == board[8] != "-":
                print(f"The winner is {board[2]}")
                game_on = False
            elif board[0] == board[4] == board[8] != "-":
                print(f"The winner is {board[0]}")
                game_on = False
            elif board[2] == board[4] == board[6] != "-":
                print(f"The winner is {board[2]}")
                game_on = False
            elif "-" not in board:
                print("It's a tie. Play again")
                game_on = False


        def flip_player():
            global current_player
            if current_player == "X":
                current_player = "O"
            else:
                current_player = "X"

        check_to_win()
        flip_player()
play_game()