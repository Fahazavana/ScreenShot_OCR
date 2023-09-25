# ScreenShot OCR

ScreenShot OCR is a simple GUI application that captures a screenshot and performs Optical Character Recognition (OCR) on it.
Prerequisites

## To use ScreenShot OCR, you need the following:

* Linux operating system (Tested on Debian 12 and Ubuntu 20.04)
* Python 3 installed
* Dependencies listed in the requirements.txt file
* Tesseract OCR engine
* Xclip
* Maim


## Installation

Follow these steps to install and set up ScreenShot OCR:

1. Ensure you have Python 3 installed on your system. If not, you can download and install it from the official Python website.

2. Install the required dependencies by running the following command in your terminal:
```
pip install -r requirements.txt
```

3. Install the Tesseract OCR engine. You can install it using the package manager for your Linux distribution. For example, on Debian-based systems, you can use the following command:

```
sudo apt-get install tesseract-ocr
```
4. Install Xclip and Maim, which are also available through the package manager. On Debian-based systems, you can use the following commands:
```
sudo apt-get install xclip maim
```
# Usage

Once you have installed the necessary dependencies, you can use ScreenShot OCR as follows:

1. Launch the application by executing the following command in your terminal:

```
python main.py
```
2. The application will open a GUI window.

3. Capture a screenshot by clicking the "Capture" button or using a keyboard shortcut if available.

4. The captured screenshot will be processed using OCR, and the extracted text will be displayed in the GUI window.
