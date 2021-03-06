import os
import math
import random


# Custom Exception to handle wrong input
class InvalidMove(Exception):
    pass


class TicTacToe:
    # Default constructor
    def __init__(self):
        # The playing board in a Dictionary Form
        self.board = {1: '1', 2: '2', 3: '3',
                      4: '4', 5: '5', 6: '6',
                      7: '7', 8: '8', 9: '9'}
        self.player1 = 'X'  # Symbol of First Player
        self.player2 = 'O'  # Symbol of Second Player
        self.gameTime()  # Start the Game
        input("Press any key to exit.")

    # Function Name - isBoardFull
    # Parameters - None
    # Return Type - Boolean
    # Function - Returns True if there are no more moves to play, else Returns False.
    def isBoardFull(self):
        return not any(map(lambda x: x in "123456789", self.board.values()))

    # Function Name - isPositionEmpty
    # Parameters - position (Integer, holds a value within 1-9 representing a position on the board)
    # Return Type - Boolean
    # Function - Returns True if passed position is empty, else Returns False.
    def isPositionEmpty(self, position):
        return self.board[position] in "123456789"

    # Function Name - gameDraw
    # Parameters - None
    # Return Type - None
    # Function - Prints Game drawn statement
    def gameDraw(self):
        os.system("clear") if os.name == "posix" else os.system("cls")
        self.printBoard()
        print("IT'S A DRAW!!\n")

    # Function Name - gameWon
    # Parameters - None
    # Return Type - None
    # Function - Prints Game won message, accordingly if its a PvP match or PvCPU match.
    def gameWon(self, playerID, isCPU):
        os.system("clear") if os.name == "posix" else os.system("cls")
        self.printBoard()
        if isCPU:
            print(f"{playerID} has won. Better luck next time.\n")
        else:
            print(f"Congrats, {playerID} has won.")

    # Function Name - insertAtPosition
    # Parameters - position (Integer, holds a value within 1-9 representing a position on the board)
    #              playerID (Character, holds the character of the current player)
    # Return Type - None
    # Function - Inserts the player symbol to the given position, if possible.
    #            Otherwise, raises InvalidMove exception.
    def insertAtPosition(self, position, playerID):
        if self.isPositionEmpty(position):
            self.board[position] = playerID
        else:
            raise InvalidMove("That square is already occupied. Please enter valid input.")

    # Function Name - playerWon
    # Parameters - PlayerID (Character, holds the symbol of the current player)
    # Return Type - Boolean
    # Function - Checks if current player has won the game. Returns True if yes, else False.
    def playerWon(self, playerID):
        return ((self.board[1] == playerID and self.board[2] == playerID and self.board[3] == playerID) or
                (self.board[4] == playerID and self.board[5] == playerID and self.board[6] == playerID) or
                (self.board[7] == playerID and self.board[8] == playerID and self.board[9] == playerID) or
                (self.board[1] == playerID and self.board[4] == playerID and self.board[7] == playerID) or
                (self.board[2] == playerID and self.board[5] == playerID and self.board[8] == playerID) or
                (self.board[3] == playerID and self.board[6] == playerID and self.board[9] == playerID) or
                (self.board[1] == playerID and self.board[5] == playerID and self.board[9] == playerID) or
                (self.board[3] == playerID and self.board[5] == playerID and self.board[7] == playerID))

    # Function Name - printBoard
    # Parameters - None
    # Return Type - None
    # Function - Prints the current state of the playing board
    def printBoard(self):
        print('  ' + self.board[1] + ' | ' + self.board[2] + ' | ' + self.board[3])
        print("  +---+---+")
        print('  ' + self.board[4] + ' | ' + self.board[5] + ' | ' + self.board[6])
        print("  +---+---+")
        print('  ' + self.board[7] + ' | ' + self.board[8] + ' | ' + self.board[9])
        print("\n")

    # Function Name - playerMove
    # Parameters - PlayerID (Character, holds the symbol of the current player)
    # Return Type - None
    # Function - Accepts input from Current player and inserts their symbol at desired location, if possible.
    #            handles exceptions where the user entered Illegal Character, entered out of bounds or
    #            enters and InvalidMove.
    def playerMove(self, playerID):
        while True:
            self.printBoard()
            position = input(f"Enter Move for {playerID} (1-9): ")
            os.system("clear") if os.name == "posix" else os.system("cls")
            try:    # Check if user entered integer or not
                position = int(position)
            except ValueError:  # If entered character is not integer
                print("\nPlease enter an Integer.\n")
                continue
            if position < 1 or position > 9:    # If entered integer is out of range
                print("\nInteger must be within range 1-9.\n")
                continue
            else:
                try:    # Inserting at position
                    self.insertAtPosition(position, playerID)
                except InvalidMove:  # In case the position is already occupied
                    print("\nThat square is already occupied. Please enter valid input.")
                    continue
                break

    # Function Name - CPU_easy
    # Parameters - None
    # Return Type - None
    # Function - Inserts symbol of the second player in a random empty spot
    def CPU_easy(self):
        options_left = [key for key, value in self.board.items() if value.isdigit()]    # Empty positions available
        self.insertAtPosition(random.choice(options_left), self.player2)    # Randomly choosing an empty position

    # Function Name - CPU_intermediate
    # Parameters - None
    # Return Type - None
    # Function - Checks if there exists any move where player 2 wins. If yes, then it takes it.
    #            Otherwise, checks if there exists a spot where player 1 can win. If yes, then it blocks that move.
    #            If neither are available, it places its symbol in a random grid.
    def CPU_intermediate(self):
        options_left = [key for key, value in self.board.items() if value.isdigit()]    # Empty positions available
        for option in options_left:  # Checking if there is any position where the CPU can place to win
            self.board[option] = self.player2
            if self.playerWon(self.player2):
                return
            self.board[option] = str(option)
        for option in options_left:  # Checking if there is any position where the player can place to win and block it
            self.board[option] = self.player1
            if self.playerWon(self.player1):
                self.board[option] = self.player2
                return
            self.board[option] = str(option)
        self.insertAtPosition(random.choice(options_left), self.player2)    # Randomly choosing an empty position

    # Function Name - miniMax
    # Parameters - depth (Integer, stores the depth of the current recursion tree)
    #              isMaximising (Boolean, store the current state of the mini-max, i.e. either maximising or minimising
    # Return Type - Integer
    # Function - Emulates every move that could be from the current state and returns a value based on the success or
    #            failure of the maximizer or the minimizer in their respective cases. Returns the lowest score
    #            possible if minimising, else returns the highest score possible if maximising, as all the moves
    #            made must be assumed to be optimal.
    def miniMax(self, depth, isMaximising, alpha, beta):
        if self.playerWon(self.player1):    # If the Minimizer won
            return -10 + depth
        if self.playerWon(self.player2):    # If the Maximizer won
            return 10 - depth
        if self.isBoardFull():  # If its a Tie
            return 0
        if isMaximising:    # If it's the Maximizer's turn
            best_score = -math.inf
            for i in range(1, 10):
                if self.isPositionEmpty(i):  # Trying out all the possible moves in a state space tree
                    self.board[i] = self.player2
                    score = self.miniMax(depth + 1, False, alpha, beta)
                    best_score = max(best_score, score)
                    alpha = max(alpha, best_score)
                    self.board[i] = str(i)
                    if beta <= alpha:   # If the maximum score is already found
                        break
            return best_score
        else:   # If it's the Minimizer's turn
            best_score = math.inf
            for i in range(1, 10):
                if self.isPositionEmpty(i):  # Trying out all the possible moves in a state space tree
                    self.board[i] = self.player1
                    score = self.miniMax(depth + 1, True, alpha, beta)
                    best_score = min(best_score, score)
                    beta = min(beta, best_score)
                    self.board[i] = str(i)
                    if beta <= alpha:   # If the minimum score is already found
                        break
            return best_score

    # Function Name - CPU_hardcore
    # Parameters - None
    # Return Type - None
    # Function - Checks all the possible ways the game could play from the current state and calculates
    #            the optimal move based on the mini-max algorithm.
    def CPU_hardcore(self):
        best_move = -1
        high_score = -math.inf
        for i in range(1, 10):
            if self.isPositionEmpty(i):  # Finding the best move to make
                self.board[i] = self.player2
                score = self.miniMax(0, False, -math.inf, math.inf)
                self.board[i] = str(i)
                if score > high_score:
                    best_move = i
                    high_score = score
        self.board[best_move] = self.player2    # Making the best move
        return

    # Function Name - gameTime
    # Parameters - None
    # Return Type - None
    # Function - Takes input from user if they want to play against another player or CPU
    #            and proceeds the game accordingly
    def gameTime(self):
        print("SELECT OPPONENT")
        print("1. 2nd Player")
        print("2. Computer - Easy")
        print("3. Computer - Intermediate")
        print("4. Computer - Hardcore")
        choice = input("Enter Choice : ")
        AI = {'1': 'player', '2': 'easy', '3': 'intermediate', '4': 'hardcore'}
        os.system("clear") if os.name == "posix" else os.system("cls")
        self.startGame(AI[choice])  # Starting the game as per user's preference

    # Function Name - startGame
    # Parameters - level (String, stores the type of opponent the player faces)
    # Return Type - None
    # Function - Emulates the game either with 2-players or a single player against a bot
    #            of varying difficulties. Continues till there is a clear winner or there are
    #            no more moves to play. Displays the result accordingly.
    def startGame(self, level):
        isCPU = (level != 'player')
        while True:  # Infinite Loop to continue the game till a winner is found or game is tied
            if self.isBoardFull():  # Draw Check
                self.gameDraw()
                break
            self.playerMove(self.player1)   # The player's (X) move
            if self.playerWon(self.player1):    # X's win check
                self.gameWon(self.player1, False)
                break
            if self.isBoardFull():  # Draw Check
                self.gameDraw()
                break
            if level == 'player':   # Preparing opponent as per player's preference
                self.playerMove(self.player2)
            elif level == 'easy':
                self.CPU_easy()
            elif level == 'intermediate':
                self.CPU_intermediate()
            elif level == 'hardcore':
                self.CPU_hardcore()
            if self.playerWon(self.player2):    # O's win check
                self.gameWon(self.player2, isCPU)
                break


# Base Function to call the TicTacToe class
if __name__ == '__main__':
    TicTacToe()
