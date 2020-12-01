import numpy as np
import os

# preprocessing
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.image import rgb_to_grayscale


# Reshaping 
from tensorflow import reshape
from tensorflow.image import resize_with_pad


def import_image(PATH, image_name):
    """
    PATH --> str: Relative path to image directoy
    image_name --> str: Name of the image to load
    
    Returns:
    PIL image
    
    """
    
    # create path to file
    img_path = PATH + "/" + image_name
    
    # load file and return pil
    return image.load_img(img_path) 

def grayscale_and_resize(PIL, shape=(255,256), padding=False):
    """
    This is the preprocessing function that will take the raw jpeg, gray scale it, resize it and 
    turn it into an array
    
    
    PIL --> PIL object
    shape --> tuple: size of the final array
    padding --> bool: if True, will use tf.resize_with_pad
    """
    if padding:
        gray_image = rgb_to_grayscale(PIL)
        resized_image_arr = resize_with_pad(gray_image, target_height=shape[0], target_width=shape[1])
    else:
        resized_image_arr = img_to_array(PIL.convert(mode = 'L').resize(shape))
    
    return resized_image_arr


def import_image_to_array(RELPATH,
         dir_names = ['train', 'test', 'val'],
         sub_dir_names = ['NORMAL', 'PNEUMONIA'],
         padding=False,
         shape=(256,256), test=False):
    """
    This function loads all train, test and validation data into a dictionary of images
    =====================================================================================
    RELPATH --> str: The relative path to the cwd to the directory containing image directories
    eg '../../src/data/chest_xray'
    =====================================================================================
    dir_names --> list, str: The names of the subdirectories containing the images
    eg ['train', 'test', 'val'] <-- default
    =====================================================================================
    sub_dir_names --> list -> str: names of the subdirectory containg postivie and negative cases
    
    =====================================================================================
    padding  --> bool: Whether you want the reshaping to be padded to or not
    
    =====================================================================================
    shape --> tuple-> int: The final shape of the tensor array
    
    returns
    
    dict --> str:list -> tuple -> (tf.array, bool)
    A dictionary where the keys are the dir_names and the values are lists containing tuple where 
    the first index is the tf.array and the second is a boolian, True if class is pnuemonia, false otherwise.
    """
    # test relative path works!! 
    PATH = os.getcwd() + RELPATH
    
    try:
        os.listdir(PATH)
        print("You're relative directory is good, proceeding to import files...", end="\n\n")
    except Exception as e:
        print(str(e))
        print(f"Your relative path directory is not pointing to the correct location. Double check your input \n")
        print("Terminating Program", end='\n')
        print("=======================================================================================")
        return False
    # instantiate a dict object and populate the keys
    image_dict = {}
    for name in dir_names:
        image_dict[name] = []
        
        print(f"Loading images from {name}", end='\n')
        
        
        # For each subdirectory, get all of the images and append to dictionary
        for sub_dir in sub_dir_names:
            subPATH = PATH + name + "/" + sub_dir
            # list of all image names in the subdirectory
            image_batch = os.listdir(subPATH)
            
            for image in image_batch:
                # import the image in pil format
                pil = import_image(subPATH, image)
                # gray scale and reshape the image turning it into an array
                gray_resized_pil = grayscale_and_resize(pil, shape=shape, padding=padding)
                
                # center the pixels
                centered_array = gray_resized_pil/255
                
                # append to the image_dict
                flag = 1
                if sub_dir == 'NORMAL':
                    flag = 0
                
                image_dict[name].append((centered_array, flag))
                
            
                # if this is just a test case, break out of this loop so we get one from each class
                if test == True:
                    break
            
            print(f"Finished loading images from {sub_dir}", end="\n")

        print()
    
    return image_dict               