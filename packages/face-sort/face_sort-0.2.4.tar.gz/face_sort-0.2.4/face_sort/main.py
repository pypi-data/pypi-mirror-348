import dlib
import argparse
from scipy.spatial import distance
import face_recognition
import os
import numpy as np
import logging
import cv2
import json
from .extract_faces import extract_faces  
from .euclidean_distance import euclidean_distance
from .cosinus_distance import cosinus_distance
from .sorted_euclidean_distance import sorted_euclidean_distance
from .sorted_cosinus_distance import sorted_cosinus_distance



def face_sort(folder_to_sort, seuil_type = None, ia_model="ED" ):
    """ 
    sorts all images in a folder and classifies them by face on the same folder as the given folder  (default destination)
    
    :param folder_to_sort : the  path of the folder containing all the images . (path)
    :param seuil_type: the chosen threshold to sorted faces (between "large" ,"strict" and nothing (default threshold)).(str)
    :param ia_model : the   chosen ia model to classify (between ED= euclidean distance and COS = cosinus) .(str)
    
    """    
    
  # Verification 
    if not os.path.isdir(folder_to_sort):
        raise FileNotFoundError(f"Error: the folder '{folder_to_sort}' does not exist or is not a valid folder.")
    
    assert seuil_type in [None, "large", "strict"], "Error : seuil_type must be 'large', 'strict' or None."
    assert ia_model in ["ED", "COS"], "Error : ia_model must be 'ED' (euclidean distance) or 'COS' (cosinus)."
    
    
    list_of_embeddings, image_names = extract_faces(folder_to_sort)
    folder = folder_to_sort
    
    if ia_model == "ED" :
        similarites = euclidean_distance(image_names, list_of_embeddings)
        if seuil_type is None :#if no parameter was passed as an argument
            sorted_euclidean_distance(similarites, folder)
        else:
            sorted_euclidean_distance(similarites, folder,seuil_type=seuil_type)
    
    elif ia_model == "COS":
        similarites = cosinus_distance(image_names, list_of_embeddings)
        if seuil_type is None :#if no parameter was passed as an argument
            sorted_cosinus_distance(similarites, folder)
        else:
            sorted_cosinus_distance(similarites, folder,seuil_type=seuil_type)
    else:
        print("ia_model must be 'ED' or 'COS' , please retry .")          
    return True



#to read the arguments in the terminal
def main():
    parser = argparse.ArgumentParser(description=" Image sorting by facial recognition ")
    parser.add_argument("folder_to_sort", help="Path of the folder to sort")
    parser.add_argument("--seuil_type", default=None, help=" Sorting severity level ('strict', 'large', none.)")
    parser.add_argument("--ia_model", default="ED", help="AI model used('ED', 'COS')")
    
    args = parser.parse_args()
    face_sort(args.folder_to_sort, args.seuil_type, args.ia_model)

if __name__ == "__main__":
    main()



