#this is another way to calculate similarities with euclidean distance 

import dlib
from scipy.spatial import distance
import face_recognition
import os
import numpy as np
import logging
import cv2
import json
 


#Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("face_distance.log"),  #  Save logs in a file
        logging.StreamHandler()  #  Displays logs in the console
    ]
)

def euclidean_distance(image_names, list_of_embeddings):
    """ 
    calculate the level of  similarity between two faces in a picture(or two differents pictures) and save them in a list.

    param
    ------
    list_of_embeddings : the embeddings of each face detected (list) 
    images_names : the index of each image by embedings(int)   
    return 
    -------
    list_of_similarities :save the result of similarities  (list)

    """

    if not isinstance(image_names, list) or not isinstance(list_of_embeddings, (list, np.ndarray)):
        logging.error("Inputs must be lists or np-array.")
        return []
        
        
    for emb_list in list_of_embeddings:
        if not isinstance(emb_list, (list, np.ndarray)):
            logging.error("Each element of embeddings must be an np-array.")
            return []
 

    if image_names == [] or list_of_embeddings == []:
        return []

    resultats = []
    
    for i in range(len(list_of_embeddings)):  # Brownse all images

        embeddings_image_i = list_of_embeddings[i]
        # Do not compare faces in a same image 
        if len(embeddings_image_i) > 1:
            logging.info(f"{len(embeddings_image_i)}  faces detected in  {image_names[i]}, considered as different individuals.")

        #Compare faces with other images
        for j in range(i + 1, len(list_of_embeddings)):

            embeddings_image_j = list_of_embeddings[j]
            for k in range(len(embeddings_image_i)):
                for l in range(len(embeddings_image_j)):
                    
                    similarity = distance.euclidean(embeddings_image_i[k], embeddings_image_j[l])

                    resultat = {
                        "image_1": image_names[i],
                        "visage_1": k,
                        "image_2": image_names[j],
                        "visage_2": l,
                        "similarite": similarity  
                    }
                    resultats.append(resultat)
        logging.info(f"All similarities between  {image_names[i]} and the others images were calculated")
        

    for rslt in resultats:

        if not isinstance(rslt, dict):
            raise TypeError("Each result must be a dictionnary .")

        if  rslt is None or rslt == [[]] or rslt == {} :
            logging.warning("Results are empty.")
            return []
        else:
            continue

        
    print(json.dumps(resultats, indent=4))             
   
    return resultats



