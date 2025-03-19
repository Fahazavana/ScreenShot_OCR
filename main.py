import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import os
import pytesseract
import subprocess
import platform

class ScreenshotOCRApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Screenshot OCR")

        self.label_font = ("Arial", 10)
        self.button_font = ("Arial", 10, "bold")

        self.create_widgets()

    def create_widgets(self):
        # Capture Button
        self.capture_button = tk.Button(self.window, text="Capture Screenshot", font=self.button_font, command=self.take_screenshot_and_process_ocr)
        self.capture_button.grid(row=0, column=0, pady=(5, 0))

        # Screenshot Method Selection
        self.method_label = tk.Label(self.window, text="Screenshot Method:", font=self.label_font)
        self.method_label.grid(row=1, column=0, pady=(5, 0))
        self.method_var = tk.StringVar(self.window)
        self.method_var.set("maim")  # Default method
        self.method_dropdown = ttk.Combobox(self.window, textvariable=self.method_var, values=["maim", "mss", "pyscreenshot"])
        self.method_dropdown.grid(row=2, column=0, pady=(2, 0))

        # Text Output Frame
        self.frame = tk.Frame(self.window)
        self.frame.grid(row=3, column=0, padx=5, pady=5)

        self.output_label = tk.Label(self.frame, text="Extracted Text", font=self.label_font)
        self.output_label.grid(row=0, column=0, padx=(2, 0), pady=5)

        self.output_text = tk.Text(self.frame, font=("JetBrainsMono Nerd Font Mono", 12), width=40, height=12)
        self.output_text.grid(row=1, column=0, padx=(2, 0), sticky="nsew")

        # Font Size Slider
        self.font_size_slider = tk.Scale(self.frame, from_=10, to=18, orient=tk.HORIZONTAL, length=200, font=self.label_font)
        self.font_size_slider.set(14)
        self.font_size_slider.grid(row=2, column=0, padx=5, pady=2)
        self.font_size_slider.bind("<ButtonRelease-1>", self.change_font_size)

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

    def capture_screenshot_maim(self):
        try:
            temp_file = "/tmp/_ocr_screen.png"
            subprocess.run(["maim", "-s", "-u", temp_file], check=True)
            return True
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to capture screenshot with maim: {e}")
            return False

    def capture_screenshot_mss(self):
        try:
            import mss
            with mss.mss() as sct:
                sct.shot(output="/tmp/_ocr_screen.png")
            return True
        except ImportError:
            messagebox.showerror("Error", "mss library not found. Please install it.")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture screenshot with mss: {e}")
            return False

    def capture_screenshot_pyscreenshot(self):
        try:
            import pyscreenshot as ImageGrab
            ImageGrab.grab().save("/tmp/_ocr_screen.png")
            return True
        except ImportError:
            messagebox.showerror("Error", "pyscreenshot library not found. Please install it.")
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Failed to capture screenshot with pyscreenshot: {e}")
            return False

    def preprocess_image(self):
        try:
            image = cv2.imread("/tmp/_ocr_screen.png")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            filtered = cv2.bilateralFilter(gray, 3, 75, 75)
            denoised = cv2.fastNlMeansDenoising(filtered)
            cv2.imwrite("/tmp/_ocr_screen.png", denoised)
        except Exception as e:
            messagebox.showerror("Error", f"Image preprocessing failed: {e}")

    def perform_ocr(self):
        try:
            image = Image.open("/tmp/_ocr_screen.png")
            return pytesseract.image_to_string(image)
        except Exception as e:
            messagebox.showerror("Error", f"OCR failed: {e}")
            return ""

    def perform_ocr_and_display(self):
        try:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "Extracting text...")
            self.window.update_idletasks()
            result = self.perform_ocr()
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)
        except Exception as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Error: {e}")

    def take_screenshot_and_process_ocr(self):
        method = self.method_var.get()
        if method == "maim":
            success = self.capture_screenshot_maim()
        elif method == "mss":
            success = self.capture_screenshot_mss()
        elif method == "pyscreenshot":
            success = self.capture_screenshot_pyscreenshot()

        if success:
            self.preprocess_image()
            self.perform_ocr_and_display()

    def change_font_size(self, event=None):
        font_size = self.font_size_slider.get()
        self.output_text.configure(font=("JetBrainsMono Nerd Font Mono", font_size))

if __name__ == "__main__":
    window = tk.Tk()
    app = ScreenshotOCRApp(window)
    window.mainloop()
