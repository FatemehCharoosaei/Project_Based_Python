import streamlit as st
import random
from collections import defaultdict
import os
st.set_page_config(
   page_title="Wordle Game",
   page_icon="🔠",
   layout="centered"
)
st.markdown("""
<style>
   .cell {
       width: 60px;
       height: 60px;
       border: 2px solid #d3d6da;
       display: inline-flex;
       justify-content: center;
       align-items: center;
       font-size: 24px;
       font-weight: bold;
       margin: 3px;
       border-radius: 5px;
   }
   .correct { background-color: #6aaa64; color: white; border-color: #6aaa64; }
   .present { background-color: #c9b458; color: white; border-color: #c9b458; }
   .absent { background-color: #787c7e; color: white; border-color: #787c7e; }
   .empty { background-color: #ffffff; color: black; }
   .key { padding: 12px 15px; margin: 3px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; min-width: 40px; }
   .container { max-width: 500px; margin: 0 auto; }
   .current-guess {
       font-size: 20px;
       font-weight: bold;
       letter-spacing: 8px;
       text-align: center;
       margin: 20px 0;
       padding: 10px;
       border: 2px solid #d3d6da;
       border-radius: 5px;
       background-color: #f8f9fa;
   }
   .celebration {
       animation: celebrate 2s ease-in-out;
   }
   @keyframes celebrate {
       0% { transform: scale(1); }
       50% { transform: scale(1.1); }
       100% { transform: scale(1); }
   }
</style>
""", unsafe_allow_html=True)
class WordleGame:
   def __init__(self):
       self.word_length = 5
       self.max_attempts = 6
       self.words = self.load_words_from_file()
       self.initialize_game()
   
   def load_words_from_file(self):
       try:
           words = []
           file_path = 'src/data/words_frequency.txt'
           
           if not os.path.exists(file_path):
               file_path = 'data/words_frequency.txt'
           if not os.path.exists(file_path):
               file_path = 'words_frequency.txt'
           
           if os.path.exists(file_path):
               with open(file_path, 'r', encoding='utf-8') as f:
                   for line in f:
                       if ', ' in line:
                           word, freq = line.strip().split(', ', 1)
                           if len(word) == self.word_length:
                               words.append(word.upper())
           else:
               words = self.get_default_words()
           
           return words
           
       except Exception as e:
           st.error(f"Error loading words: {e}")
           return self.get_default_words()
   
   def get_default_words(self):
       base_words = [
           'APPLE', 'BRAIN', 'CRANE', 'DRAMA', 'EAGLE', 'FLAME', 'GRAPE',
           'HOUSE', 'IDEAL', 'JOLLY', 'KNIFE', 'LIGHT', 'MAGIC', 'NIGHT',
           'OCEAN', 'PIANO', 'QUEEN', 'RADIO', 'SMILE', 'TIGER', 'ULTRA',
           'VITAL', 'WORLD', 'YOUTH', 'ZEBRA', 'BREAD', 'CLOUD', 'DANCE',
           'EARTH', 'FAITH', 'GLASS', 'HEART', 'IMAGE', 'JEWEL', 'LUCKY'
       ]
       return [word.upper() for word in base_words]
   
   def initialize_game(self):
       if 'target' not in st.session_state:
           if self.words:
               st.session_state.target = random.choice(self.words)
           else:
               st.session_state.target = "APPLE"
       
       if 'guesses' not in st.session_state:
           st.session_state.guesses = []
       
       if 'current' not in st.session_state:
           st.session_state.current = ""
       
       if 'ended' not in st.session_state:
           st.session_state.ended = False
       
       if 'won' not in st.session_state:
           st.session_state.won = False
       
       if 'letters' not in st.session_state:
           st.session_state.letters = defaultdict(str)
       
       if 'show_balloons' not in st.session_state:
           st.session_state.show_balloons = False
   
   def evaluate_guess(self, guess):
       target_word = st.session_state.target
       evaluation = []
       
       for position in range(self.word_length):
           if guess[position] == target_word[position]:
               evaluation.append(('correct', guess[position]))
               st.session_state.letters[guess[position]] = 'correct'
           elif guess[position] in target_word:
               evaluation.append(('present', guess[position]))
               if st.session_state.letters[guess[position]] != 'correct':
                   st.session_state.letters[guess[position]] = 'present'
           else:
               evaluation.append(('absent', guess[position]))
               if guess[position] not in st.session_state.letters:
                   st.session_state.letters[guess[position]] = 'absent'
       
       return evaluation
   
   def submit_guess(self):
       guess_attempt = st.session_state.current.upper().strip()
       
       if len(guess_attempt) != self.word_length:
           st.error(f"Word must be {self.word_length} letters!")
           return
       
       if not any(word.upper() == guess_attempt for word in self.words):
           st.error("Word not in dictionary!")
           return
       
       result = self.evaluate_guess(guess_attempt)
       st.session_state.guesses.append((guess_attempt, result))
       st.session_state.current = ""
       
       if guess_attempt == st.session_state.target:
           st.session_state.ended = True
           st.session_state.won = True
           st.session_state.show_balloons = True
       elif len(st.session_state.guesses) >= self.max_attempts:
           st.session_state.ended = True
       
       st.rerun()
   
   def render_board(self):
       st.markdown("<div class='container'>", unsafe_allow_html=True)
       
       st.title("🎯 Wordle Game")
       st.subheader(f"Guess the {self.word_length}-letter word")
       
       for attempt_num in range(self.max_attempts):
           cols = st.columns(self.word_length)
           if attempt_num < len(st.session_state.guesses):
               guess_word, guess_result = st.session_state.guesses[attempt_num]
               for col, (status, letter) in zip(cols, guess_result):
                   with col:
                       st.markdown(
                           f'<div class="cell {status}">{letter}</div>',
                           unsafe_allow_html=True
                       )
           else:
               for col in cols:
                   with col:
                       st.markdown('<div class="cell empty"></div>', unsafe_allow_html=True)
       
       st.markdown("</div>", unsafe_allow_html=True)
   
   def render_current_guess(self):
       st.markdown("<div class='container'>", unsafe_allow_html=True)
       
       current_display = st.session_state.current.ljust(self.word_length, ' ')
       st.markdown(f'<div class="current-guess">{current_display}</div>', unsafe_allow_html=True)
       
       col1, col2 = st.columns([1, 1])
       with col1:
           if st.button("📤 Submit Guess", use_container_width=True,
                       disabled=st.session_state.ended or len(st.session_state.current) != self.word_length,
                       type="primary"):
               self.submit_guess()
       with col2:
           if st.button("⌫ Clear", use_container_width=True,
                       disabled=st.session_state.ended or len(st.session_state.current) == 0):
               st.session_state.current = ""
               st.rerun()
       
       st.markdown("</div>", unsafe_allow_html=True)
   
   def render_keyboard_input(self):
       st.markdown("<div class='container'>", unsafe_allow_html=True)
       
       st.write("**Type your guess below:**")
       
       new_input = st.text_input(
           "Enter your word:",
           value=st.session_state.current,
           max_chars=self.word_length,
           key="keyboard_input",
           placeholder="Start typing...",
           label_visibility="collapsed"
       ).upper()
       
       if new_input != st.session_state.current:
           st.session_state.current = new_input
           st.rerun()
       
       st.markdown("</div>", unsafe_allow_html=True)
   
   def render_virtual_keyboard(self):
       keyboard_rows = [
           ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
           ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
           ['Z', 'X', 'C', 'V', 'B', 'N', 'M']
       ]
       
       st.markdown("<div class='container'>", unsafe_allow_html=True)
       st.write("**Or use virtual keyboard:**")
       
       for row in keyboard_rows:
           cols = st.columns(len(row))
           for col, key in zip(cols, row):
               with col:
                   if st.button(key, use_container_width=True,
                              disabled=st.session_state.ended):
                       if len(st.session_state.current) < self.word_length:
                           st.session_state.current += key
                           st.rerun()
       
       st.markdown("</div>", unsafe_allow_html=True)
   
   def get_key_color(self, status):
       colors = {
           'correct': '#6aaa64',
           'present': '#c9b458',
           'absent': '#787c7e'
       }
       return colors.get(status, '#d3d6da')
   
   def render_game_info(self):
       col1, col2, col3 = st.columns(3)
       
       with col1:
           remaining = self.max_attempts - len(st.session_state.guesses)
           st.metric("Attempts Left", remaining)
       
       with col2:
           st.metric("Guesses Made", len(st.session_state.guesses))
       
       with col3:
           if st.session_state.ended:
               status = "🎉 You Won!" if st.session_state.won else "💔 Game Over"
               st.metric("Status", status)
           else:
               st.metric("Status", "Playing")
       
       if st.session_state.ended:
           if st.button("🔄 Start New Game", use_container_width=True, type="secondary"):
               self.reset_game()
   
   def reset_game(self):
       st.session_state.target = random.choice(self.words)
       st.session_state.guesses = []
       st.session_state.current = ""
       st.session_state.ended = False
       st.session_state.won = False
       st.session_state.letters = defaultdict(str)
       st.session_state.show_balloons = False
       st.rerun()
def main():
   game = WordleGame()
   
   with st.sidebar:
       st.header("🎯 How to Play")
       st.markdown("""
       **Keyboard Controls:**
       - **Type directly** in the text field
       - **Enter** in text field to submit
       - Or use **virtual keyboard**
       - **Submit** button to check your guess
       **Colors Meaning:**
       🟩 **Green** = Correct letter, correct position  
       🟨 **Yellow** = Correct letter, wrong position  
       ⬜ **Gray** = Letter not in word
       **You have 6 attempts to win!**
       """)
       
       st.header("📊 Game Stats")
       if st.session_state.ended:
           if st.session_state.won:
               st.success(f"🎉 Won in {len(st.session_state.guesses)} attempts!")
           else:
               st.error(f"The word was: **{st.session_state.target}**")
       
       st.divider()
       st.write(f"**Words in dictionary:** {len(game.words)}")
   
   game.render_game_info()
   game.render_board()
   
   # Show balloons immediately when won
   if st.session_state.show_balloons:
       st.balloons()
       st.session_state.show_balloons = False
   
   game.render_current_guess()
   game.render_keyboard_input()
   game.render_virtual_keyboard()
   
   if st.session_state.ended:
       st.divider()
       if st.session_state.won:
           st.success(f"🎊 **Victory!** You guessed **{st.session_state.target}**!")
       else:
           st.error(f"😔 **Game Over!** The word was **{st.session_state.target}**")
if __name__ == "__main__":
   main()
 