try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2


def ocr_core(filename):
    """
    This function will handle the core OCR processing of images.
    """
    text = pytesseract.image_to_string(Image.open(
        filename))  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
    return text


print(ocr_core('images/staff-id-card.jpg'))

# Create the voice_text variable to store the data.

voice_text = ""

# Pre-processing the data

for i in ocr_core('images/staff-id-card.jpg').split():
    voice_text += i + ' '

voice_text = voice_text[:-1]
voice_text

from gtts import gTTS
from playsound import playsound

tts = gTTS(voice_text)
tts.save("test.mp3")
playsound("test.mp3")
