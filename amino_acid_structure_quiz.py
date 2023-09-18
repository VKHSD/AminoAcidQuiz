from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import random

# Dev Mode (set to True if you want the correct answer to be indicated)
dev_mode = False


def molecule_to_img(mol, width=300, height=300):
    img = Draw.MolToImage(mol, size=(width, height))
    img = ImageTk.PhotoImage(img)
    return img


# Amino acids data
amino_acids = {
    "Alanine": "CC(C(=O)O)N",
    "Arginine": "NC(CCCNC(N)=N)C(O)=O",
    "Asparagine": "NC(C(C(N)=O)=O)C(O)=O",
    "Aspartic Acid": "NC(C(O)=O)C(O)=O",
    "Cysteine": "C(C(C(=O)O)N)S",
    "Glutamic Acid": "C(CC(=O)O)C(C(=O)O)N",
    "Glutamine": "O=C(N)CCC(N)C(=O)O",
    "Glycine": "C(C(=O)O)N",
    "Histidine": "O=C(O)[C@@H](N)Cc1cncn1",
    "Isoleucine": "CC[C@H](C)[C@@H](C(=O)O)N",
    "Leucine": "CC(C)C[C@@H](C(=O)O)N",
    "Lysine": "C(CCN)CC(C(=O)O)N",
    "Methionine": "CSCCC(C(=O)O)N",
    "Phenylalanine": "c1ccc(cc1)C[C@@H](C(=O)O)N",
    "Proline": "C1CC(NC1)C(=O)O",
    "Serine": "C([C@@H](C(=O)O)N)O",
    "Threonine": "C[C@H]([C@@H](C(=O)O)N)O",
    "Tryptophan": "c1ccc2c(c1)c(c[nH]2)C[C@@H](C(=O)O)N",
    "Tyrosine": "N[C@@H](Cc1ccc(O)cc1)C(O)=O",
    "Valine": "CC(C)[C@@H](C(=O)O)N"
}

unasked_questions = list(amino_acids.keys())
correct_count = 0
total_questions = 0
answer_flip_flop = False


def quiz():
    global correct_count, total_questions, unasked_questions, answer_flip_flop
    if len(unasked_questions) == 0:
        unasked_questions = list(amino_acids.keys())

    correct_answer = random.choice(unasked_questions)
    unasked_questions.remove(correct_answer) 

    answer_flip_flop = False

    wrong_answers = random.sample([k for k in amino_acids.keys() if k != correct_answer], 4)
    choices = wrong_answers + [correct_answer]
    random.shuffle(choices)

    mol = Chem.MolFromSmiles(amino_acids[correct_answer])
    img = molecule_to_img(mol)

    lbl.config(image=img)
    lbl.image = img

    for i, choice in enumerate(choices):
        display_text = choice
        if dev_mode and choice == correct_answer:
            display_text += " (+)"
        buttons[i].config(text=display_text, command=lambda choice=choice: check_answer(choice, correct_answer))

    if total_questions > 0:
        percent_correct = (correct_count / total_questions) * 100
        lbl_count.config(text=f"Correct: {correct_count} ({percent_correct:.2f}%)")
    else:
        lbl_count.config(text=f"Correct: {correct_count}")


def check_answer(choice, correct_answer):
    global correct_count, answer_flip_flop, total_questions

    if choice == correct_answer:
        if not answer_flip_flop:
            correct_count += 1
            total_questions += 1  
        # No need to reset answer_flip_flop here, it is reset at the beginning of quiz()
            quiz()
            return
    else:
        answer_flip_flop = True  
        if dev_mode:
            messagebox.showinfo("Wrong!", f"The correct answer is {correct_answer}. Try again.")
        else:
            messagebox.showinfo("Wrong!", "Try again.")
        return 
    total_questions += 1
    quiz()


# GUI
root = tk.Tk()
root.title("Amino Acid Quiz")

lbl = tk.Label(root)
lbl.pack()

lbl_count = tk.Label(root, text=f"Correct: {correct_count}")
lbl_count.pack()

buttons = []
for i in range(5):
    btn = tk.Button(root, text="Choice", width=20)
    btn.pack()
    buttons.append(btn)

quiz()
root.mainloop()
