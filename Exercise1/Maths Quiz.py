# ----------------------------------------------
# Project Title : Maths Quiz
# ----------------------------------------------
# Description:
# This program is a simple interactive Maths Quiz made using the tkinter.
# The user chooses a difficulty level, answers random addition or subtraction problems,
# and gets a final score and grade at the end. 
# ----------------------------------------------
# Source Code References:
# - Random number generation
# - Basic structure inspired by inclass discussions
# ----------------------------------------------

import random
import tkinter as tk
from tkinter import messagebox

# -----------------------------
# Global variables declaration
# -----------------------------
root = None             # Main window for the tkinter GUI
difficulty = 0          # Holds selected difficulty level
score = 0               # Keeps track of player’s score
question_count = 0      # Counts how many questions have been answered
num1 = 0                # First number in the math question
num2 = 0                # Second number in the math question
op = ''                 # Operator symbol (+ or -)
retry = False           # Used to check if user is on second attempt

# -----------------------------
# Function: displayMenu()
# Purpose : Displays difficulty options at the start
# -----------------------------
def displayMenu():
    # Clear previous screen widgets (if any)
    for widget in root.winfo_children():
        widget.destroy()

    # Title label for difficulty screen
    title_label = tk.Label(root, text="DIFFICULTY LEVEL", font=("Arial", 24, "bold"), bg="#1D252D", fg="white")
    title_label.pack(pady=20)

    # Button style dictionary for consistency
    button_style = {"font": ("Arial", 18), "width": 15, "height": 2}

    # Easy level button (yellow)
    easy_btn = tk.Button(root, text="Easy", bg="#FFB347", fg="black", command=lambda: set_difficulty(1), **button_style)
    easy_btn.pack(pady=10)

    # Moderate level button (orange)
    moderate_btn = tk.Button(root, text="Moderate", bg="#FF8C42", fg="black", command=lambda: set_difficulty(2), **button_style)
    moderate_btn.pack(pady=10)

    # Advanced level button (red)
    advanced_btn = tk.Button(root, text="Advanced", bg="#FF6B6B", fg="black", command=lambda: set_difficulty(3), **button_style)
    advanced_btn.pack(pady=10)

# -----------------------------
# Function: set_difficulty()
# Purpose : Saves selected difficulty and starts the quiz
# -----------------------------
def set_difficulty(level):
    global difficulty, score, question_count
    difficulty = level
    score = 0
    question_count = 0
    next_question()  # Load the first question

# -----------------------------
# Function: randomInt()
# Purpose : Generates random numbers based on difficulty
# -----------------------------
def randomInt(difficulty):
    if difficulty == 1:
        return random.randint(0, 9)       # Single digits for easy mode
    elif difficulty == 2:
        return random.randint(10, 99)     # Two-digit numbers for moderate mode
    else:
        return random.randint(1000, 9999) # Four-digit numbers for advanced mode

# -----------------------------
# Function: decideOperation()
# Purpose : Randomly selects '+' or '-'
# -----------------------------
def decideOperation():
    return random.choice(['+', '-'])

# -----------------------------
# Function: displayProblem()
# Purpose : Displays a new math question on screen
# -----------------------------
def displayProblem():
    global num1, num2, op, retry
    # Clear the screen before showing new question
    for widget in root.winfo_children():
        widget.destroy()

    # Generate random question
    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    op = decideOperation()

    # Display the problem text
    problem_label = tk.Label(root, text=f"{num1} {op} {num2} =", font=("Arial", 24), bg="#1D252D", fg="white")
    problem_label.pack(pady=30)

    # Entry widget for user to type answer
    answer_entry = tk.Entry(root, font=("Arial", 18), width=10)
    answer_entry.pack(pady=10)
    answer_entry.focus()  # Cursor auto-focus for convenience

    # Submit button triggers answer checking
    submit_btn = tk.Button(root, text="Submit", font=("Arial", 16), command=lambda: check_answer(answer_entry.get()))
    submit_btn.pack(pady=20)

# -----------------------------
# Function: check_answer()
# Purpose : Verifies if user's answer is correct or not
# -----------------------------
def check_answer(user_input):
    global score, question_count, retry

    # Error handling if user types letters instead of numbers
    try:
        user_answer = int(user_input)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
        return

    # Validate correctness
    if isCorrect(num1, num2, op, user_answer):
        # Give points based on attempt
        if not retry:
            score += 10   # 10 points if correct on first try
        else:
            score += 5    # 5 points if correct on second try
        question_count += 1
        retry = False

        # Continue until 10 questions are done
        if question_count < 10:
            next_question()
        else:
            displayResults()
    else:
        # If wrong, give one more try before moving on
        if not retry:
            retry = True
            messagebox.showinfo("Incorrect", "Try again!")
            displayProblem()
        else:
            retry = False
            question_count += 1
            if question_count < 10:
                next_question()
            else:
                displayResults()

# -----------------------------
# Function: isCorrect()
# Purpose : Checks the actual answer and gives feedback
# -----------------------------
def isCorrect(num1, num2, op, user_answer):
    # Calculate correct answer
    correct = num1 + num2 if op == '+' else num1 - num2

    # Compare and display feedback
    if user_answer == correct:
        messagebox.showinfo("Correct", "Well done!")
        return True
    else:
        messagebox.showerror("Incorrect", f"Wrong! The correct answer is {correct}.")
        return False

# -----------------------------
# Function: displayResults()
# Purpose : Shows final score and grade at end of quiz
# -----------------------------
def displayResults():
    for widget in root.winfo_children():
        widget.destroy()

    # Determine rank based on score
    if score > 90:
        rank = "A+"
    elif score >= 80:
        rank = "A"
    elif score >= 70:
        rank = "B"
    elif score >= 60:
        rank = "C"
    else:
        rank = "D"

    # Display results
    result_label = tk.Label(root, text=f"Final Score: {score}/100\nRank: {rank}", font=("Arial", 20), bg="#1D252D", fg="white")
    result_label.pack(pady=30)

    # Replay or exit options
    play_again_btn = tk.Button(root, text="Play Again", font=("Arial", 16), command=displayMenu)
    play_again_btn.pack(pady=10)

    quit_btn = tk.Button(root, text="Quit", font=("Arial", 16), command=root.quit)
    quit_btn.pack(pady=10)

# -----------------------------
# Function: next_question()
# Purpose : Loads a new problem
# -----------------------------
def next_question():
    displayProblem()

# -----------------------------
# Function: start_game()
# Purpose : Main entry point for program setup
# -----------------------------
def start_game():
    global root
    root = tk.Tk()
    root.title("Maths Quiz")
    root.geometry("500x400")
    root.configure(bg="#1D252D")  # Blackboard-like dark theme
    root.resizable(False, False)
    displayMenu()  # Start with the difficulty menu
    root.mainloop()  # Keeps window running

# -----------------------------
# Program Entry Point
# -----------------------------
if __name__ == "__main__":
    start_game()
