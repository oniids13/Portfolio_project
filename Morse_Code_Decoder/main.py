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
    return end_text

def decoding(dictionary, text):
    decoded_text = []
    for code in text:
        for key, val in dictionary.items():
            if val == code:
                decoded_text.append(key)
    print(f"The decoded value is {decoded_text}.")



should_end = False
while not should_end:
    print(logo)
    print("Welcome to my morse code decoder")
    text = input("Type the word to convert into morse code: \n")
    decoded_text = morse_coding(text.upper())

    decode = input("Do you want to decode your message? Type 'y' or 'n' \n")
    if decode == "y":
        decoding(morse, decoded_text)
    restart = input("Type 'yes' if you want to convert again, otherwise type 'no'.\n")
    if restart == "no":
        should_end = True
        print("Goodbye")
    os.system('cls')


