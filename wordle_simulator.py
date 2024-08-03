import os
import json
import streamlit as st
import numpy as np
from collections import defaultdict

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

def provide_feedback(guess, target):
    feedback = ["⬜"] * len(guess)  # Default feedback is gray
    remaining_letters = list(target)
    
    # First pass to assign greens (correct letters in the right position)
    for i in range(len(guess)):
        if guess[i] == target[i]:
            feedback[i] = "🟩"
            remaining_letters[i] = None  # Mark this position as None to ignore in second pass

    # Second pass to assign yellows and confirm gray
    for i in range(len(guess)):
        if feedback[i] == "⬜":  # Only consider letters not already marked green
            if guess[i] in remaining_letters:
                feedback[i] = "🟨"
                # Remove the first occurrence from remaining_letters to avoid double counting
                remaining_letters[remaining_letters.index(guess[i])] = None

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
    
# Function to calculate skill and luck based on feedback patterns and word reductions
def calculate_skill_and_luck(guesses, valid_words):
    skills = []
    lucks = []
    remaining_words = valid_words.copy()
    total_words = len(valid_words)
    
    for guess, feedback, _, remaining in guesses:
        feedback_patterns = defaultdict(int)
        for word in remaining_words:
            pattern = ''.join(provide_feedback(guess, word))
            feedback_patterns[pattern] += 1
        
        # Calculate skill as the number of unique feedback patterns normalized
        unique_patterns = len(feedback_patterns)
        skill = (unique_patterns / total_words) * 100
        
        # Calculate luck as the deviation from the expected reduction
        expected_reduction = np.mean(list(feedback_patterns.values()))
        actual_reduction = total_words - remaining
        luck = ((actual_reduction - expected_reduction) / expected_reduction) * 100 if expected_reduction else 0
        
        skills.append(skill)
        lucks.append(luck)
        
        # Update remaining words for next iteration
        remaining_words = [word for word in remaining_words if ''.join(provide_feedback(guess, word)) == ''.join(feedback)]
    
    return skills, lucks

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
        st.session_state.skills, st.session_state.lucks = calculate_skill_and_luck(st.session_state.guesses, valid_words)
    else:
        st.error("Invalid word. Please try again.")

st.write("## Previous Guesses")
for idx, (guess, feedback, eliminated, remaining) in enumerate(st.session_state.guesses):
    skill = st.session_state.skills[idx]
    luck = st.session_state.lucks[idx]
    st.write(f"Guess: {guess} | Feedback: {''.join(feedback)} | Words eliminated: {eliminated} | Skill: {skill:.2f} | Luck: {luck:.2f}")

if len(st.session_state.guesses) >= 6:
    st.write("Game Over. You've used all your guesses!")
elif target_word in [guess[0] for guess in st.session_state.guesses]:
    st.write("Congratulations! You've guessed the word!")

# Final skill and luck display
if st.session_state.guesses:
    overall_skill, overall_luck = calculate_skill_and_luck(st.session_state.guesses, valid_words)
    st.write(f"Overall Skill: {overall_skill[-1]:.2f}")
    st.write(f"Overall Luck: {overall_luck[-1]:.2f}")
