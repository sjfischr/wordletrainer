import os
import json
import streamlit as st
import numpy as np

# Load the list of valid words from a text file
def load_word_list(filename):
    with open(filename, "r") as file:
        words = [line.strip().lower() for line in file.readlines()]
    return words

valid_words = load_word_list("valid_words.txt")

# Load target word from configuration
with open("config.json", "r") as file:
    config = json.load(file)
target_word = config["target_word"].lower()

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

# Function to calculate skill and luck
def calculate_skill_and_luck(guesses, initial_word_count):
    reductions = [initial_word_count]
    for i in range(1, len(guesses)):
        reductions.append(reductions[i-1] - guesses[i-1][2])
    average_reduction = initial_word_count / len(guesses)
    skill = np.mean([guess[2] for guess in guesses]) / average_reduction
    luck = np.std([guess[2] for guess in guesses]) / average_reduction
    return skill, luck

# Streamlit UI
st.title("Wordle Simulator")

if "guesses" not in st.session_state:
    st.session_state.guesses = []
    st.session_state.remaining_words = valid_words.copy()

with st.form(key='guess_form', clear_on_submit=True):
    guess = st.text_input("Enter your guess (5 letters):").lower()
    submit_button = st.form_submit_button(label='Submit Guess')

if submit_button and guess:
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

# Calculate and display skill and luck
if st.session_state.guesses:
    skill, luck = calculate_skill_and_luck(st.session_state.guesses, len(valid_words))
    st.write(f"Skill: {skill:.2f}")
    st.write(f"Luck: {luck:.2f}")
