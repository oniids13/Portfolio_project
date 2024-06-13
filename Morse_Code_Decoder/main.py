from morse_code import morse, logo
import os
def morse_coding(text):
    end_text = []
    for letter in text:
        if letter in morse:
            code = morse[letter]
            end_text.append(code)
        else:
            print("Please enter valid character")
    print(f"Here's the morse code: \n{end_text}")


def decoding(dictionary, text2):
    entry = text2.split(' ')
    decoded_text = []
    for code in entry:
        for key, val in dictionary.items():
            if val == code:
                decoded_text.append(key)
    print(f"The decoded value is {decoded_text}.")



should_end = False
while not should_end:
    print(logo)
    print("Welcome to my morse code decoder")
    choice = input("Do you want to encode or decode? Type 'e' or 'd':\n")
    if choice == "e":
        text = input("Type the word to convert into morse code: \n")
        morse_coding(text.upper())
    elif not choice:
        print("Error please enter 'D' or 'E' only.")
    else:
        text2 = input("Type the morse code you want to convert into text each character separated by space: \n")
        decoding(morse,text2)

    restart = input("Do you want to convert again? Type 'y' or 'n':\n")
    if restart == "n":
        should_end = True
        print("Goodbye")
    os.system('cls')


