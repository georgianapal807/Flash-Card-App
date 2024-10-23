from tkinter import *
from tkmacosx import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
words_list = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    words_list = original_data.to_dict(orient='records')
else:
    words_list = data.to_dict(orient='records')


# ---------------------------- GENERATE RANDOM WORD ------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(words_list)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_image, image=front_card_image)
    flip_timer = window.after(3000, func=flip_card)


# ---------------------------- FLIP CARD ------------------------------- #
def flip_card():
    global current_card
    canvas.itemconfig(card_image, image=back_card_image)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, fill="white", text=current_card["English"])


# ---------------------------- SAVE PROGRESS ------------------------------- #
def is_known():
    words_list.remove(current_card)
    new_data = pandas.DataFrame(words_list)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flash Card Game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(height=526, width=800)
front_card_image = PhotoImage(file="images/card_front.png")
back_card_image = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=front_card_image)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"), fill='black')
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 60, "bold"), fill='black')
canvas.grid(column=0, row=0, columnspan=2)

wrong_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_image, bg=BACKGROUND_COLOR, highlightthickness=10, borderless=1,
                      command=next_card)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file='images/right.png')
right_button = Button(image=right_image, bg=BACKGROUND_COLOR, highlightthickness=10, borderless=1, command=is_known)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()
