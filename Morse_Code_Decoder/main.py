from morse_code import morse

def morse_coding(text):
    end_text = []
    for letter in text:
        if letter in morse:
            code = morse[letter]
            end_text.append(code)
        else:
            print("Please enter valid character")
    print(f"Here's the morse code: \n{end_text}")

should_end = False
while not should_end:
    text = input("Type the word to convert into morse code: \n")
    morse_coding(text.upper())

    restart = input("Type 'yes' if you want to code again, otherwise type 'no'.\n")
    if restart == "no":
        should_end =  True
        print("Goodbye")


# text = "DINO"
# print(morse_coding(text))


