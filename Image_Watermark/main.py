import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

YELLOW = "#f7f5dd"
IMG_PATH = ""

def water_mark_image():
    global IMG_PATH

    if not IMG_PATH:
        return

    with Image.open(IMG_PATH).convert("RGBA") as im:
        width, height = im.size
        draw = ImageDraw.Draw(im)
        txt = Image.new("RGBA", im.size, (255,255,255,0))
        font = ImageFont.truetype('arial.ttf', 36)
        text = f"Photo by: {watermark_input.get()}"
        watermark_entry.set("")
        margin = 10
        bbox = draw.textbbox((0, 0), text=text, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = width - text_width - margin
        y = height - text_height - margin

        draw.text((x, y), text, font=font, fill="black")
        pic = Image.alpha_composite(im, txt)
        out = Image.alpha_composite(im, txt)
        out.thumbnail((600, 600))
        image_tk = ImageTk.PhotoImage(out.convert("RGB"))
        watermarked_image_label.config(image=image_tk)
        watermarked_image_label.image = image_tk
        watermark_label_output.config(text="Output")
        return pic



def get_image_path():
    file_path = filedialog.askopenfilename(
        title="Select an image.",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )

    if file_path:
        if os.path.isabs(file_path):
            relative_path = file_path
        else:
            relative_path = os.path.relpath(file_path)

        print("Relative Path:", relative_path)
        load_and_display_image(relative_path)
        preview_label.config(text="Preview: ")
        global IMG_PATH
        IMG_PATH = relative_path
        return IMG_PATH
    else:
        print("No file selected")
        return None

def load_and_display_image(image_path):
    image = Image.open(image_path)
    image.thumbnail((400,300))
    image_tk = ImageTk.PhotoImage(image)
    image_label.config(image=image_tk)
    image_label.image = image_tk

def save_pic():
    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
        title="Save Watermarked Image"
    )
    if save_path:

        current_image = water_mark_image()
        if current_image:
            # Save the image to the selected path
            current_image.save(save_path)
            print(f"Image saved successfully at {save_path}")
        else:
            print("No watermarked image to save")
    else:
        print("Save operation cancelled")

def clear_app():
    global IMG_PATH
    IMG_PATH = ""
    watermark_input.delete(0, tk.END)
    image_label.config(image="")
    watermarked_image_label.config(image="")
    preview_label.config(text="")
    watermark_label_output.config(text="")


window = tk.Tk()
window.title("Image Watermarking App")
window.config(padx=10, pady=5, bg=YELLOW,)

window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(3, weight=1)


# Canvas
canvas = tk.Canvas(window, width=800, height=400, bg=YELLOW, highlightthickness=0)
canvas.grid(column=1, row=1)

welcome_label = tk.Label(text="Welcome to image watermarking App!")
welcome_label.config(font=("Arial", 20))
welcome_label.config(bg=YELLOW)
welcome_label.grid(column=1, row=0, columnspan=3)

watermark_entry = tk.StringVar()
watermark_input = tk.Entry(window, textvariable=watermark_entry ,width=25)
watermark_input.grid(column=1, row=5)

watermark_label = tk.Label(text="Please enter the name you want to watermark:")
watermark_label.config(bg=YELLOW)
watermark_label.grid(column=1, row=4)

img_button = tk.Button(window,text="Select Image", command=get_image_path)
img_button.grid(column=0, row=2, padx=5, pady=5)

image_label = tk.Label(window)
image_label.grid(column=1, row=1)

preview_label = tk.Label(window)
preview_label.config(bg=YELLOW)
preview_label.grid(column=0, row=1)

watermark_label_output = tk.Label(window)
watermark_label_output.config(bg=YELLOW)
watermark_label_output.grid(column=2, row=2, padx=5, pady=5)

watermark_button = tk.Button(window,text="Insert Watermark", command=water_mark_image)
watermark_button.grid(column=1, row=6, padx=5, pady=5)

watermarked_image_label =tk.Label(window)
watermarked_image_label.grid(column=2, row=1, padx=5, pady=5)

save_button = tk.Button(window, text="Save Image", command=save_pic)
save_button.grid(column=2, row=3)


clear_button = tk.Button(window, text="Clear", command=clear_app)
clear_button.grid(column=0, row=3, padx=5, pady=5)


window.mainloop()