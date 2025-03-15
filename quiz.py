from tkinter import *
import pygame
import os
from os import sys
from PIL import Image, ImageTk



pygame.mixer.init()
intro_music=pygame.mixer.Sound("audios/a.mp3")
a=pygame.mixer.Sound("audios/dk.mp3")
a.play()
intro_music.play()

all_ques = [
    "What was the first game played in Squid Game?",
    "How many players participated in Squid Game?",
    "What color are the guards' uniforms?",
    "What is the final game played in Squid Game?",
    "What is the prize money for winning Squid Game?",
    "Who is the main character in Squid Game?",
    "What shape is honeycomb in the Dalgona game?"
]

all_answers = [
    ("Red Light, Green Light", "Tug of War", "Marbles", "Glass Bridge"),
    ("456", "324", "500", "1000"),
    ("Red", "Blue", "Pink", "Green"),
    ("Squid Game", "Chess", "Tag", "Hopscotch"),
    ("45.6 billion won", "10 billion won", "100 billion won", "1 billion won"),
    ("Gi-hun", "Sang-woo", "Ali", "Il-nam"),
    ("Star", "Circle", "Triangle", "Umbrella")
]

correct_answers = [
    "Red Light, Green Light", "456", "Pink", "Squid Game",
    "45.6 billion won", "Gi-hun", "Umbrella"
]

image_paths = [
    "images/bg.jpg",
    "images/main.jpg",
    "images/bg.jpg",
    "images/doll-front.jpg",
    "images/prize.jpg",  
    "images/main.jpg", 
    "images/third.jpg"  
]

# Global variables
count = 0
score = 0
selected_answers = [None] * len(all_ques)
correctness = [False] * len(all_ques)

# Functions
def ans_choose(btn):
    global selected_answers, next_button
    selected_answers[count] = btn.cget("text")
    next_button.config(state='normal')  # Enable Next button after selecting an answer

    # Highlight the selected button
    for button in buttons:
        if button.cget("text") == selected_answers[count]:
            button.config(bg="blue")  # Highlight selected button
        else:
            button.config(bg="red")  # Reset other buttons

def next_question():
    global count, score, submit_button, next_button
    # Evaluate the selected answer before moving to the next question
    if selected_answers[count] == correct_answers[count]:
        correctness[count] = True
    else:
        correctness[count] = False

    # Move to the next question
    if count < len(all_ques) - 1:
        count += 1
        update_question()

    # Enable Submit button if all questions are answered
    if all(answer is not None for answer in selected_answers):
        submit_button.config(state='normal')
        next_button.config(state=DISABLED)

def prev_question():
    global count
    if count > 0:
        count -= 1
        update_question()

def update_question():
    global image_label
    question_label.config(text=all_ques[count])
    try:
        img = Image.open(image_paths[count])
        img = img.resize((250, 250))
        img = ImageTk.PhotoImage(img)
        image_label.config(image=img)
        image_label.image = img  # Keep a reference to avoid garbage collection
    except Exception as e:
        print(f"Error loading image: {e}")

    # Update buttons for the current question
    for i in range(4):
        buttons[i].config(text=all_answers[count][i], state='normal', bg="red")

    # Highlight the selected answer (if any) for the current question
    if selected_answers[count] is not None:
        for button in buttons:
            if button.cget("text") == selected_answers[count]:
                button.config(bg="blue")  # Highlight selected button

    # Update navigation buttons
    prev_button.config(state='normal' if count > 0 else DISABLED)
    next_button.config(state=DISABLED if count == len(all_ques) - 1 else 'normal')

def show_score():
    global score
    # Calculate total score based on correctness
    total_score = sum(correctness)
    total_questions = len(all_ques)
    intro_music.stop()
    b=pygame.mixer.Sound("audios/song.mp3")
    b.play()
    # Create a new window for the scorecard
    score_window = Toplevel(root)
    score_window.title("Quiz Completed")
    score_window.geometry("400x400")
    score_window.config(bg="black")

    # Add a fun message based on the score
    if total_score == total_questions:
        message = "🎉 You're a Squid Game Master! 🎉"
        emoji = "🏆"
    elif total_score >= total_questions // 2:
        message = "😊 Well done! You survived the games!"
        emoji = "👍"
    else:
        message = "😢 Better luck next time!"
        emoji = "💔"

    # Display the score and message
    Label(score_window, text="Quiz Results", font=("Arial", 25, "bold"), bg="black", fg="white").pack(pady=10)
    Label(score_window, text=f"{emoji} Your Score: {total_score}/{total_questions}", font=("Arial", 20), bg="black", fg="white").pack(pady=10)
    Label(score_window, text=message, font=("Arial", 15), bg="black", fg="white").pack(pady=10)

    # Add a progress bar (visual representation of the score)
    progress_canvas = Canvas(score_window, width=300, height=20, bg="white")
    progress_canvas.pack(pady=20)
    progress_width = (total_score / total_questions) * 300
    progress_canvas.create_rectangle(0, 0, progress_width, 20, fill="green")

    # Add a close button
    Button(score_window, text="Close", command=score_window.destroy, font=("Arial", 15), bg="red", fg="white").pack(pady=20)

# GUI Setup
root = Tk()
root.title("Squid Game Quiz")
root.geometry("700x800")
root.config(bg="black")

main_canvas = Canvas(root, width=700, height=800, bg="black")
main_canvas.pack()

question_label = Label(text=all_ques[0], font=('Arial', 20, 'bold'), pady=20, padx=20, bg="black", fg="white",bd=5, relief="solid")
main_canvas.create_window(350, 100, window=question_label)

# Image Display
image_label = Label(root, bg="black")
main_canvas.create_window(350, 250, window=image_label)

answer_frame = Frame(main_canvas, bg="black")
main_canvas.create_window(350, 500, window=answer_frame)

buttons = []
for i in range(4):
    button = Button(answer_frame, text=all_answers[0][i], font=('Arial', 15, 'bold'), pady=10, padx=20, bg="red", fg="white")
    button.config(command=lambda btn=button: ans_choose(btn))
    button.grid(row=i//2, column=i%2, padx=20, pady=10)
    buttons.append(button)

# Navigation Buttons
next_button = Button(text="Next", font=("Arial", 15, 'bold'), padx=10, pady=10, command=next_question, state=DISABLED, bg="yellow")
prev_button = Button(text="Prev", font=("Arial", 15, 'bold'), padx=10, pady=10, command=prev_question, state=DISABLED, bg="yellow")
submit_button = Button(text="Submit", font=("Arial", 15, 'bold'), padx=10, pady=10, command=show_score, bg="green", state=DISABLED)

main_canvas.create_window(600, 700, window=next_button)
main_canvas.create_window(100, 700, window=prev_button)
main_canvas.create_window(350, 700, window=submit_button)  # Centered Submit button

update_question()

root.mainloop()