import tkinter as tk
from tkinter import messagebox
import random

amino_acids = {
    "Alanine": "A",
    "Arginine": "R",
    "Asparagine": "N",
    "Aspartic Acid": "D",
    "Cysteine": "C",
    "Glutamic Acid": "E",
    "Glutamine": "Q",
    "Glycine": "G",
    "Histidine": "H",
    "Isoleucine": "I",
    "Leucine": "L",
    "Lysine": "K",
    "Methionine": "M",
    "Phenylalanine": "F",
    "Proline": "P",
    "Serine": "S",
    "Threonine": "T",
    "Tryptophan": "W",
    "Tyrosine": "Y",
    "Valine": "V"
}

correct_count = 0
total_questions = 0

# Dev Mode
dev_mode = True

unasked_questions = list(amino_acids.values())

answer_flip_flop = False


def quiz():
    global correct_count, total_questions, unasked_questions, answer_flip_flop

    if len(unasked_questions) == 0:
        unasked_questions = list(amino_acids.values())
        answer_flip_flop = False

    correct_answer = random.choice(unasked_questions)
    if not answer_flip_flop:
        unasked_questions.remove(correct_answer)

    wrong_answers = random.sample([v for v in amino_acids.values() if v != correct_answer], 4)

    choices = wrong_answers + [correct_answer]
    random.shuffle(choices)

    label.config(text=f"{correct_answer}", font=("Helvetica", 144))

    for i, choice in enumerate(choices):
        full_name = [k for k, v in amino_acids.items() if v == choice][0]
        display_text = full_name
        if dev_mode and choice == correct_answer:
            display_text += " (+)"
        buttons[i].config(text=display_text, command=lambda choice=choice: check_answer(choice, correct_answer))

    # Display correct count
    if total_questions > 0:
        percent_correct = (correct_count / total_questions) * 100
        lbl_count.config(text=f"Correct: {correct_count} ({percent_correct:.2f}%)")
    else:
        lbl_count.config(text=f"Correct: {correct_count}")


def check_answer(choice, correct_answer):
    global correct_count, total_questions, answer_flip_flop

    if choice == correct_answer:
        if not answer_flip_flop:
            correct_count += 1
            total_questions += 1
        answer_flip_flop = False
    else:
        answer_flip_flop = True

    quiz()


# GUI Setup
root = tk.Tk()
root.title("Amino Acid Quiz")
root.geometry("300x600")  

label = tk.Label(root, text="", width=5, height=2)
label.pack()

lbl_count = tk.Label(root, text=f"Correct: {correct_count}")
lbl_count.pack()

buttons = []
for i in range(5):
    btn = tk.Button(root, text="Choice", width=20)
    btn.pack()
    buttons.append(btn)

quiz()

root.mainloop()
