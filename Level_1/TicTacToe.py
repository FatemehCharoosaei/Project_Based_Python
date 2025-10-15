import random
class TicTacToe:
   def __init__(self, human_player):
       self.board = [" " for _ in range(9)]
       self.human = human_player
       self.computer = "O" if human_player == "X" else "X"
       self.current_player = random.choice([self.human, self.computer])
   def make_move(self, position, player):
       if self.board[position] == " ":
           self.board[position] = player
           return True
       return False
   def switch_player(self):
       self.current_player = self.computer if self.current_player == self.human else self.human
   def check_winner(self):
       wins = [
           (0,1,2),(3,4,5),(6,7,8),
           (0,3,6),(1,4,7),(2,5,8),
           (0,4,8),(2,4,6)
       ]
       for a,b,c in wins:
           if self.board[a] == self.board[b] == self.board[c] != " ":
               return self.board[a]
       return None
   def get_computer_move(self):
       empty = [i for i, val in enumerate(self.board) if val == " "]
       return random.choice(empty) if empty else None
   def print_board(self):
       print("\n")
       for i in range(0, 9, 3):
           print(f"{self.board[i]} | {self.board[i+1]} | {self.board[i+2]}")
       print("\n")
# === Run the game ===
if __name__ == "__main__":
   player = input("Choose your symbol (X or O): ").strip().upper()
   game = TicTacToe(player)
   while True:
       game.print_board()
       if game.current_player == game.human:
           try:
               pos = int(input("Enter your move (0-8): "))
               if not game.make_move(pos, game.human):
                   print("Invalid move. Try again.")
                   continue
           except:
               print("Please enter a number between 0 and 8.")
               continue
       else:
           pos = game.get_computer_move()
           game.make_move(pos, game.computer)
           print(f"Computer played at position {pos}")
       winner = game.check_winner()
       if winner:
           game.print_board()
           print(f"{winner} wins!")
           break
       elif " " not in game.board:
           game.print_board()
           print("It's a tie!")
           break
       game.switch_player()
   
