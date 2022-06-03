import pathlib  
import os 
import cv2

from  TextExtraction import TextSelectorFromImage 
from  ImgTextReaderFc import read_test_from_image
 
import pandas as pd


def start_run(counter):
    path = pathlib.Path().resolve() 
    path = f'{path}\DataBins'   


    def if_folder_do_not_exist():
        for x in os.listdir(path):
            if os.path.isdir(f'{path}\{x}') and x[-1] == str(counter+1) : 
                return False
        return True


    new_path = path
    if if_folder_do_not_exist():

        new_dir = f'DataBin{counter+1}'
        new_path = os.path.join(path, new_dir ) 
        os.mkdir(new_path)  
        print( f'Please, move you files to the: {new_path}')
    else:
        new_dir =  f'DataBin{counter+1}'
        new_path = new_path = os.path.join(path, new_dir )  
        print( f'The folder you choosed is: {new_path}')

    return new_path


def main_run(img_path, col_name):

    path = start_run(0)
    print('Once done, press ENTER')
    input()  

    img_path = f'{path }\{img_path}' 

    a = TextSelectorFromImage()
    a.run(img_path)
    coords = a.current_coords 


    series_arr = []
    for x in os.listdir(path):

        img_path = f'{path }\{x}' 
        img = cv2.imread(img_path) 
        starting_x = coords[0][0]
        starting_y = coords[0][1]
        ending_x = coords[1][0]
        ending_y = coords[1][1]
        # Cropping image
        img_cropped = img[starting_y:ending_y, starting_x:ending_x]

        series_arr.append(  read_test_from_image(img_cropped) ) 

    return pd.DataFrame( {  col_name : series_arr   } ) 

    

    


#kek = main_run('a.jpg', 'a')
#print(kek)

