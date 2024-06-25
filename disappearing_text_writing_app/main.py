from tkinter import *
from tkinter import font

timer = None
typing_stop_countdown = 3000
line_height = 25
max_width = 800
margin = 10


def key_press(event):
    global text, timer
    if event.keysym == "BackSpace":
        text = text[:-1]
    else:
        text += event.char

    render_text()

    if timer is not None:
        window.after_cancel(timer)
    timer = window.after(typing_stop_countdown, typing_stopped)

def typing_stopped():
    global text
    canvas.delete("all")
    text = ""
    canvas.bind("<Key>", key_press)



def render_text():
    canvas.delete("all")
    x, y = 10, 10

    for word in text.split(' '):
        word_width = text_font.measure(word)
        if x + word_width > max_width - margin:
            x = margin
            y += line_height
        canvas.create_text(x, y, text=word, font=text_font, anchor='nw')
        x += word_width + text_font.measure(' ')






window = Tk()
window.title("Disappearing Text Editor")
window.config(width=1000, height=800, padx=10, pady=10,)

canvas = Canvas(window, bg='white', width=800, height=600)
canvas.pack()


text = ""
text_id = canvas.create_text(10, 10, anchor='nw', text=text, font=("Helvetica", 16), fill="black")
text_font = font.Font(family="Helvetica", size=16)

canvas.bind("<Key>", key_press)
canvas.focus_set()


window.mainloop()