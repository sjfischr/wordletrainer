# Wordle Simulator/Trainer

A Python-based Wordle Simulator built using Streamlit that allows users to practice Wordle strategies while measuring Skill and Luck scores for each guess. This app is inspired by Wordle's logic and offers insights into how your guesses influence the game.

## Features
- Interactive Gameplay: Enter guesses interactively and get instant feedback (🟩🟨⬜).
- Skill Measurement: See how effectively your guesses reduce the solution space.
- Luck Measurement: Understand how fortunate your guesses are compared to expected outcomes.
- Solution Space Reduction: Visualize how each guess narrows down possible solutions.
- Score Insights: View detailed scores for each guess and overall performance.

## Installation
To run this project locally, follow these steps:

Clone the repository:

```bash git clone https://github.com/your-username/wordle-simulator.git
cd wordle-simulator

Install the required Python dependencies:

```bash
pip install -r requirements.txt

Run the app:

```bash
streamlit run wordle_simulator.py

Open your web browser and go to http://localhost:8501.

## How to Play

Set the Target Word: Modify the config.json file to set the target word for your game.

{
    "target_word": "scale"
}

### Make Guesses:

Enter a 5-letter word guess in the input field.
Press Enter or click Submit Guess to see the feedback (🟩🟨⬜).
View Feedback:

Green (🟩): Correct letter in the correct position.
Yellow (🟨): Correct letter in the wrong position.
Gray (⬜): Incorrect letter.
Skill and Luck Scores:

- Skill: How strategically sound your guess was (100 = perfect).
- Luck: How lucky your guess was in reducing the solution space (100 = very lucky).

### Solve the Wordle:

Continue guessing until you've found the target word or exhausted 6 attempts.

### Scoring System

#### Skill
Measures how well your guess segments the remaining solutions. A high Skill score indicates that your guess divides the remaining words into many distinct patterns.

#### Luck
Compares the actual reduction in possible words after your guess to the expected reduction. A higher Luck score means your guess was fortunate compared to statistical averages.

## Example Gameplay
Guess	Feedback	Words Eliminated	Words Remaining	Skill	Luck
CRANE	🟨⬜⬜⬜🟩	2189	127	90	95
SCALE	🟩🟩🟩🟩🟩	126	1	100	100

## Project Structure

wordle-simulator/
├── wordle_simulator.py   # Main application script
├── config.json           # Configuration file for target word
├── valid_words.txt       # List of all valid words
├── requirements.txt      # Python dependencies
└── .streamlit/
    └── config.toml       # Streamlit configuration

## Contributions
Contributions are welcome! If you'd like to improve the simulator or fix any bugs, feel free to:

- Fork the repository.
- Create a feature branch.
- Submit a pull request.

## Issues
If you encounter any issues, please open a new issue in the GitHub Issues section.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
Inspired by the popular Wordle game by Josh Wardle.
Developed using Streamlit for an interactive UI.
