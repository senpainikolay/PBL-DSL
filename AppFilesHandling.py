import pathlib  
import os


path = pathlib.Path().resolve() 
print(path)  
path = f'{path}\DataBins'   


def if_folder_do_not_exist():
    for x in os.listdir(path):
        if os.path.isdir(f'{path}\{x}'): 
            return False
    return True


if if_folder_do_not_exist() is False:
    print('auf')

if if_folder_do_not_exist():

    new_dir = f'DataBin1'
    new_path = os.path.join(path, new_dir ) 
    os.mkdir(new_path)  
    del new_dir, new_path  



print(path)


