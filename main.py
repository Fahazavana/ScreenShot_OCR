import tkinter as tk
from PIL import Image, ImageTk
import cv2
import os
import pytesseract

def perform_ocr():
    """
    Perform OCR using Tesseract on the captured screenshot image.
    
    Returns:
        str: Extracted text from the image.
    """
    image = Image.open("/tmp/_ocr_screen.png")
    return pytesseract.image_to_string(image)


def capture_screenshot_maim():
    """
    Capture the screenshot using maim and save it to a temporary file.
    
    Returns:
        bool: True if the screenshot capture was successful, False otherwise.
    """
    os.system("maim -s -u | xclip -selection clipboard -t image/png; xclip -selection clipboard -t image/png -o> /tmp/_ocr_screen.png")
    return True


def preprocess_image():
    """
    Preprocess the captured screenshot image to enhance OCR quality.
    """
    print("* Preprocessing...")
    image = cv2.imread("/tmp/_ocr_screen.png")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    filtered = cv2.bilateralFilter(gray, 3, 75, 75)
    denoised = cv2.fastNlMeansDenoising(filtered)
    cv2.imwrite("/tmp/_ocr_screen.png", denoised)
    print("* Preprocessing done")


def perform_ocr_and_display():
    """
    Perform text extraction using OCR and display the results in the Tkinter window.
    """
    try:
        print("* Extracting text...")
        result = perform_ocr()
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)
        print("* Task done, waiting for next task!!")
    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Error: " + str(e))


def take_screenshot_and_process_ocr():
    """
    Capture a screenshot, preprocess the image, and perform OCR to extract text.
    """
    try:
        print("* Taking a screenshot")
        capt = capture_screenshot_maim()
        if capt:
            preprocess_image()
            perform_ocr_and_display()
        else:
            print("* No captured image")
            raise ValueError("No captured image")
    except Exception as e:
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Error: " + str(e))


def change_font_size(event=None):
    """
    Change the font size of the extracted text based on the selected value in the font size combobox.
    """
    font_size = font_size_slider.get()
    output_text.configure(font=("JetBrainsMono Nerd Font Mono", font_size))


window = tk.Tk()
window.title("Screenshot OCR")

label_font = ("Arial", 10)
label_bg = "light gray"

button_font = ("Arial", 10, "bold")
button_bg = "light gray"
button_fg = "black"

capture_button = tk.Button(window, text="Capture Screenshot", font=button_font, command=take_screenshot_and_process_ocr,
                           bg=button_bg, fg=button_fg)
capture_button.grid(row=1, column=0, pady=(5,0))

frame = tk.Frame(window)
frame.grid(row=2, column=0, padx=5, pady=5)

output_label = tk.Label(frame, text="Extracted Text", font=label_font, bg=label_bg)
output_label.grid(row=0, column=0, padx=(2, 0), pady=5)

output_text = tk.Text(frame, font=("JetBrainsMono Nerd Font Mono", 12), width=40, height=12)
output_text.grid(row=1, column=0, padx=(2, 0), sticky="nsew")

# Create a slider for font size selection

font_size_slider = tk.Scale(frame, from_=10, to=18, orient=tk.HORIZONTAL, length=200, font=label_font)
font_size_slider.set(14)  # Set the default font size
font_size_slider.grid(row=2, column=0, padx=5, pady=2)
font_size_slider.bind("<ButtonRelease-1>", change_font_size)



frame.columnconfigure(1, weight=1)
frame.rowconfigure(0, weight=1)

window.mainloop()
