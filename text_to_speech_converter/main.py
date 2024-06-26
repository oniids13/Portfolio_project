import fitz
from gtts import gTTS
import os



# Converting the PDF docs to string
pdf_doc = 'sample.pdf'
doc = fitz.open(pdf_doc)
for page_num in range(doc.page_count):
    page = doc.load_page(page_num)
    text = page.get_text("text")



# Using the gTTS module text-to-speech converter
text_to_convert = text
language = 'en'
my_project = gTTS(text=text_to_convert, lang=language, slow=False)
my_project.save("sample.mp3") # Saves the audio mp3


os.system("start sample.mp3") # opens the mp3

