
import os
import logging
from PIL import Image, ImageDraw 
import face_recognition
import cv2 
import numpy as np


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("extract_faces.log"),  
        logging.StreamHandler() 
    ]
)

def extract_faces(folder_to_sort):
    """ 
    extract all embedding's faces of each image in a folder

    param
    ------
    folder_to_sort : the path of the folder that contains all pictures.(path)
    
    return 
    -------
    list_of_locations_of_cd : return a list of list , where each list represent a list of all the embeddings of faces present here.(list)
    """

     # Return an empty list if the path does not exist.
    if not os.path.exists(folder_to_sort):
        logging.error(f"The folder '{folder_to_sort}' does not exist.")
        return [] ,[]
    

    list_of_locations_of_cd = []
    list_of_embeddings = []
    image_names =[]# to track file names and keep track of the starting image
    for filename in os.listdir(folder_to_sort):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")): #converts extensions that are uppercase to lowercase
            image_path = os.path.join(folder_to_sort,filename) #retrieve the path of each image
            logging.info(f"Processing file: {filename}")

            try:

                image_to_work_on = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                if image_to_work_on is None:
                    logging.warning(f"Unable to load image: {filename}")
                    continue        
                
                assert not isinstance(image_to_work_on,type(None)), " image not found or could not be read ."

                # Check if the image is in RGB
                if len(image_to_work_on.shape) == 2:
                 
                # Convert to RGB if grayscale image
                    image_to_work_on = cv2.cvtColor(image_to_work_on, cv2.COLOR_GRAY2RGB)
                elif image_to_work_on.shape[2] == 4:
                  
                    # Convert to RGB if image in RGBA
                    image_to_work_on = cv2.cvtColor(image_to_work_on, cv2.COLOR_RGBA2RGB)
                elif image_to_work_on.shape[2]== 3 :
                    image_to_work_on = cv2.cvtColor(image_to_work_on, cv2.COLOR_BGR2RGB)

               
                list_of_cd = face_recognition.face_locations(image_to_work_on)#list of coordinates of each face in an image
                face_encodings = face_recognition.face_encodings(image_to_work_on, list_of_cd)

                # allows you to report the number of faces detected in an image.
                if face_encodings:
                    logging.info(f"Detected {len(face_encodings)} face(s) in {filename}.")
                else:
                    logging.warning(f"No faces detected in {filename}.")

                # Add embeddings and image name
                list_of_embeddings.append(face_encodings)
                image_names.append(filename)

            
                for tete in list_of_cd:
                    
                    assert tete is not None ,"list can not be empty . "
                    assert isinstance(tete,tuple) and all(isinstance(coord, int ) for coord in tete), " each coordinate must be an integer ."

                
            except Exception as e:
                logging.error(f"An error occurred while processing {filename}: {e}")

    return list_of_embeddings ,image_names
