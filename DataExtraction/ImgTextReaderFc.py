import cv2
from pytesseract import pytesseract
from pytesseract import Output 

def read_test_from_image(img):
    pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    image_data = pytesseract.image_to_data(img, output_type=Output.DICT)  

    while '' in image_data['text']:
        image_data['text'].remove('')  

    if len(image_data['text']) == 0:
        return 'Error Selecting' 
     
    if len(image_data['text']) > 1:
        str_final = ""
        for x in image_data['text']:
            str_final = str_final + ' ' + str(x)
        return str_final

    return image_data['text'][0]
