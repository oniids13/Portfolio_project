from tkinter import *
from PIL import ImageTk, Image
import random
from words import random_words

BACKGROUND = "#F6E6CB"
timer = None
check_word = ""
random_word = ""
score = 0
error = 0
def count_down(count):
    count_sec = count
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    timer_count.config(text=f"{count_sec}")
    running = True

    if running and count > 0:
        global timer
        timer = window.after(1000, count_down, count -1)
        start_button.config(state=DISABLED)
    else:
        typing_area.delete(0, END)
        typing_area.config(state=DISABLED)
        typing_area.unbind("<Return>")
        random_words_sample.config(text="Time's up!")
        global score, error
        correct_entry = score - error
        accuracy = round(correct_entry / score * 100, 2)
        final_score.config(text=f"Final Score is: {score}wpm\nAccuracy is: {accuracy}%")


def start_timer():
    time = 60
    count_down(time)
    typing_area.config(state=NORMAL, justify="center")
    typing_area.bind("<Return>", store_word)
    rand_words()

def reset_app():
    global score, error
    window.after_cancel(timer)
    timer_count.config(text="60")
    start_button.config(state=NORMAL)
    typing_area.delete(0, END)
    typing_area.config(state=DISABLED)
    random_words_sample.config(text="")
    word_count.config(text="")
    score = 0
    error = 0
    final_score.config(text="")


def rand_words():
    global random_word
    random_word = random.choice(random_words)
    random_words_sample.config(text=random_word)

def scoring():
    global score, error
    if random_word == check_word:
        score += 1
    else:
        score += 1
        error += 1

    word_count.config(text=score)


def store_word(event):
    global check_word, score, random_word, error
    word = typing_area.get()
    check_word = word
    print(random_word)
    scoring()
    if word:
        typing_area.delete(0, END)
        rand_words()
        print(score)
        print(check_word)
        print(error)






window = Tk()
window.title("Typing Test")
window.config(width=800, height=600, padx=10, pady=10, bg=BACKGROUND)


#Column 0

words_label = Label(text="Word Count", font=('Arial', 25), bg=BACKGROUND)
words_label.grid(column=0, row=1, padx=5, pady=5)

word_count = Label(window, font=('Arial', 25), bg=BACKGROUND)
word_count.grid(column=0, row=2, padx=5, pady=5)

start_button = Button(text="Start", width=20, command=start_timer)
start_button.grid(column=0, row=4, padx=5, pady=5)

#Column 1

canvas = Canvas(width=220, height=224,bg=BACKGROUND, highlightthickness=0)
speed_img = ImageTk.PhotoImage(Image.open("speed.png"))
canvas.create_image(115, 110, image=speed_img)
canvas.grid(column=1, row=1, rowspan=2)

title_label = Label(text="Welcome to typing test!", font=('Arial', 40), bg=BACKGROUND)
title_label.grid(column=1,row=0, padx=5, pady=5)

random_words_sample = Label(window, font=('Arial', 25, 'bold'), bg=BACKGROUND)
random_words_sample.grid(column=1, row=3, padx=5, pady=5)

typing_area = Entry(width=20, font=('Arial', 25), state=DISABLED)
typing_area.grid(column=1, row=4, padx=5, pady=5)
typing_area.bind("<Return>", store_word)

instructions = Label(text="Type the word above and hit ENTER", font=('Arial', 25), bg=BACKGROUND)
instructions.grid(column=1, row=5, padx=5, pady=5)

final_score = Label(window, font=('Arial', 25), bg=BACKGROUND)
final_score.grid(column=1, row=6, padx=5, pady=5)

# Column 2


timer_label = Label(text="TIMER", font=('Arial', 25), bg=BACKGROUND)
timer_label.grid(column=2, row=1, padx=5, pady=5)

timer_count = Label(window, font=('Arial', 25), bg=BACKGROUND)
timer_count.grid(column=2, row=2, padx=5, pady=5)

reset_button = Button(text="Reset", width=20, command=reset_app)
reset_button.grid(column=2, row=4, padx=5, pady=5)




window.mainloop()