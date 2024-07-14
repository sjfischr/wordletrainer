import os
import json
import streamlit as st

# Get the port from the environment variable
port = int(os.environ.get('PORT', 8501))

# Configure Streamlit to use the specified port
st.set_option('server.port', port)

# Load the list of valid words from a text file
def load_word_list(filename):
    with open(filename, "r") as file:
        words = [line.strip() for line in file.readlines()]
    return words

valid_words = load_word_list("valid_words.txt")

# Load target word from configuration
with open("config.json", "r") as file:
    config = json.load(file)
target_word = config["target_word"]

# Function to provide feedback on the guess
def provide_feedback(guess, target):
    feedback = [""] * 5
    remaining_letters = list(target)
    # First pass: check for correct letters in correct positions
    for i in range(5):
        if guess[i] == target[i]:
            feedback[i] = "🟩"
            remaining_letters[i] = None
    # Second pass: check for correct letters in wrong positions
    for i in range(5):
        if feedback[i] == "":
            if guess[i] in remaining_letters:
                feedback[i] = "🟨"
                remaining_letters[remaining_letters.index(guess[i])] = None
            else:
                feedback[i] = "⬜"
    return feedback

# Function to filter remaining words
def filter_remaining_words(guess, feedback, word_list):
    remaining_words = []
    for word in word_list:
        match = True
        for i in range(5):
            if (feedback[i] == "🟩" and guess[i] != word[i]) or \
               (feedback[i] == "🟨" and (guess[i] not in word or guess[i] == word[i])) or \
               (feedback[i] == "⬜" and guess[i] in word):
                match = False
                break
        if match:
            remaining_words.append(word)
    return remaining_words

# Streamlit UI
st.title("Wordle Simulator")

if "guesses" not in st.session_state:
    st.session_state.guesses = []
    st.session_state.remaining_words = valid_words.copy()

guess = st.text_input("Enter your guess (5 letters):")

if st.button("Submit Guess") and len(st.session_state.guesses) < 6:
    if guess in valid_words:
        feedback = provide_feedback(guess, target_word)
        remaining_words = filter_remaining_words(guess, feedback, st.session_state.remaining_words)
        eliminated_count = len(st.session_state.remaining_words) - len(remaining_words)
        st.session_state.guesses.append((guess, feedback, eliminated_count, len(remaining_words)))
        st.session_state.remaining_words = remaining_words
    else:
        st.error("Invalid word. Please try again.")

st.write("## Previous Guesses")
for guess, feedback, eliminated, remaining in st.session_state.guesses:
    percentage_remaining = (remaining / len(valid_words)) * 100
    st.write(f"Guess: {guess} | Feedback: {''.join(feedback)} | Words eliminated: {eliminated} | Words remaining: {remaining} ({percentage_remaining:.2f}%)")

if len(st.session_state.guesses) >= 6:
    st.write("Game Over. You've used all your guesses!")
elif target_word in [guess[0] for guess in st.session_state.guesses]:
    st.write("Congratulations! You've guessed the word!")
