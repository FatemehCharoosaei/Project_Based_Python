import random  # Import the random module to allow the computer to make random choices
class RockPaperScissors:
   def __init__(self):
       # Define the valid choices for the game
       self.choices = ['rock', 'paper', 'scissors']
   def get_user_choice(self):
       # Continuously prompt the user until a valid choice is made or they quit
       while True:
           user_choice = input("Enter your Choice? (rock, paper, scissors) or 'q' to quit: ").strip().lower()
           # If user wants to quit the game
           if user_choice == 'q':
               print("Thanks for playing!")
               return None  # Exit the loop and signal quitting
           # If user enters a valid choice
           if user_choice in self.choices:
               return user_choice
           # If user enters an invalid choice
           else:
               print("Invalid choice. Please make sure your choice is in 'rock', 'paper' or 'scissors'.")
               continue  # Ask again
   def get_computer_choice(self):
       # Randomly select one of the valid choices for the computer
       return random.choice(self.choices)
   def decide_winner(self, user_choice, computer_choice):
       # Convert both choices to lowercase for comparison
       user = user_choice
       computer = computer_choice
       # If both choices are the same, it's a tie
       if user == computer:
           return "It's a tie!"
       # Check all winning conditions for the user
       elif (user == 'rock' and computer == 'scissors') or \
            (user == 'scissors' and computer == 'paper') or \
            (user == 'paper' and computer == 'rock'):
           return "Congratulations, you won!"
       # If none of the above, the computer wins
       else:
           return "Oh no, the computer won!"
   def play(self):
       """Main method to play Rock, Paper, Scissors"""
       user_choice = self.get_user_choice()
       # If user chose to quit, exit the game
       if user_choice is None:
           exit()
       # Get computer's choice and display the result
       computer_choice = self.get_computer_choice()
       print('Computer chose: ', computer_choice)
       print(self.decide_winner(user_choice, computer_choice))
# Run the game in a loop until the user quits
if __name__ == '__main__':
   game = RockPaperScissors()
   while True:
       game.play()