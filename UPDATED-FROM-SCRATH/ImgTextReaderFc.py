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


    final = image_data['text'][0]

    bool_float = False
    k = 0
    for i in range(len(final) - k):
        if final[i] == ',':
            final = final.replace(',','.')
            bool_float = True
            continue

        if not final[i-k].isnumeric() and final[i-k] not in ['.', '-']:
            final  = final.replace(final[i-k], '')
            k += 1 

    if bool_float:
        return float(final)
    return int(final)









