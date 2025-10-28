import random

class Player:
    def __init__(self, name, symbol, is_human=True):
        self.name = name
        self.symbol = symbol
        self.is_human = is_human

class TicTacToe:
    def __init__(self):
        # Set up empty board and keep track of scores
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.players = []
        self.scores = {"X": 0, "O": 0, "Draw": 0}
    
    def show_board(self):
        # Print the board with nice formatting so it looks like a real tic tac toe grid
        print("\n   1   2   3")
        for i in range(3):
            row_label = chr(65 + i)
            row_display = " | ".join(self.board[i])
            print(f"{row_label}  {row_display}")
            if i < 2:
                print("  -----------")
    
    def is_move_valid(self, move):
        if len(move) != 2:
            return False
        
        row_letter = move[0].upper()
        col_number = move[1]
        
        # Check if row is A,B,C and column is 1,2,3
        if row_letter in ["A", "B", "C"] and col_number in ["1", "2", "3"]:
            row_index = ord(row_letter) - 65  # A=0, B=1, C=2
            col_index = int(col_number) - 1   # 1=0, 2=1, 3=2
            
            # Check if spot is empty
            return self.board[row_index][col_index] == " "
        
        return False
    
    def make_move(self, move, symbol):
        # Convert letter+number to actual board coordinates and place the symbol
        row_index = ord(move[0].upper()) - 65
        col_index = int(move[1]) - 1
        self.board[row_index][col_index] = symbol
    
    def check_winner(self, symbol):
        # Check rows - see if any entire row has this symbol
        for row in self.board:
            if all(cell == symbol for cell in row):
                return True
        
        # Check columns - look down each column for three in a row
        for col in range(3):
            if all(self.board[row][col] == symbol for row in range(3)):
                return True
        
        # Check diagonals - both top-left to bottom-right and top-right to bottom-left
        if all(self.board[i][i] == symbol for i in range(3)):
            return True
        if all(self.board[i][2-i] == symbol for i in range(3)):
            return True
        
        return False
    
    def is_board_full(self):
        # If no empty spaces left it's a draw
        for row in self.board:
            if " " in row:
                return False
        return True
    
    def get_empty_spots(self):
        # Make a list of moves like ['A1', 'B2', 'C3']
        empty = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == " ":
                    row_letter = chr(65 + row)
                    col_number = str(col + 1)
                    empty.append(row_letter + col_number)
        return empty
    
    def computer_turn(self, symbol):
        empty_spots = self.get_empty_spots()
        
        # First priority: try to win if possible
        for spot in empty_spots:
            self.make_move(spot, symbol)
            if self.check_winner(symbol):
                self.make_move(spot, " ") 
                return spot
            self.make_move(spot, " ")
        
        # Second priority: block the human player from winning
        player_symbol = "X" if symbol == "O" else "O"
        for spot in empty_spots:
            self.make_move(spot, player_symbol)
            if self.check_winner(player_symbol):
                self.make_move(spot, " ")
                return spot
            self.make_move(spot, " ")
        
        # Third: take the center if it's free
        if "B2" in empty_spots:
            return "B2"
        
        # Fourth: grab any available corner
        corners = ["A1", "A3", "C1", "C3"]
        for corner in corners:
            if corner in empty_spots:
                return corner
        
        # Last resort: pick any random spot
        return random.choice(empty_spots)
    
    def setup_game(self):
        # Let players choose game mode and enter their names
        print("=== Tic Tac Toe ===")
        print("1. Play against friend")
        print("2. Play against computer")
        
        while True:
            choice = input("Choose (1 or 2): ")
            if choice == "1":
                p1_name = input("Player 1 name (X): ")
                p2_name = input("Player 2 name (O): ")
                self.players = [
                    Player(p1_name, "X"),
                    Player(p2_name, "O")
                ]
                break
            elif choice == "2":
                p1_name = input("Your name (X): ")
                self.players = [
                    Player(p1_name, "X"),
                    Player("Computer", "O", False)
                ]
                break
            else:
                print("Please enter 1 or 2")
    
    def play_round(self):
        current_player = self.players[0]
        
        while True:
            self.show_board()
            
            if current_player.is_human:
                # Human player's turn
                while True:
                    move = input(f"\n{current_player.name}'s turn ({current_player.symbol}): ")
                    if self.is_move_valid(move):
                        self.make_move(move, current_player.symbol)
                        break
                    else:
                        print("Invalid move! Try like A1, B2, C3 etc.")
            else:
                # Computer's turn
                print(f"\nComputer's turn...")
                move = self.computer_turn(current_player.symbol)
                self.make_move(move, current_player.symbol)
                print(f"Computer plays {move}")
            
            # Check if the current player just won the game
            if self.check_winner(current_player.symbol):
                self.show_board()
                print(f"\n{current_player.name} wins!")
                self.scores[current_player.symbol] += 1
                break
            
            # If no winner but board is full it's a draw
            if self.is_board_full():
                self.show_board()
                print("\nIt's a draw!")
                self.scores["Draw"] += 1
                break
            
            # Switch to the other player for the next turn
            current_player = self.players[1] if current_player == self.players[0] else self.players[0]
    
    def show_scores(self):
        # Show how many games each player has won so far
        print("\n--- Scores ---")
        print(f"{self.players[0].name} (X): {self.scores['X']}")
        print(f"{self.players[1].name} (O): {self.scores['O']}")
        print(f"Draws: {self.scores['Draw']}")
    
    def reset_board(self):
        # Clear the board for a new game but keep the players and scores
        self.board = [[" " for _ in range(3)] for _ in range(3)]
    
    def play_game(self):
        self.setup_game()
        
        keep_playing = True
        while keep_playing:
            self.reset_board()
            self.play_round()
            self.show_scores()
            
            # Ask if they want to play again
            while True:
                again = input("\nPlay again? (y/n): ").lower()
                if again in ["y", "n"]:
                    keep_playing = (again == "y")
                    break
                else:
                    print("Enter y or n")
        
        print("\nGame over")

if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()