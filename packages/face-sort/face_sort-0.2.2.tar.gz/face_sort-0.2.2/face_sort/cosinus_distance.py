from scipy.spatial.distance import cosine 
import face_recognition
import os
import numpy as np
import logging
import cv2 
import json


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("face_distance.log"),  # Sauvegarder les logs dans un fichier
        logging.StreamHandler()  # Afficher les logs dans la console
    ]
)



def cosinus_distance(image_names, list_of_embeddings):
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
        logging.error("Inputs must be lists or np-arrays.")
        return []
        

    for emb_list in list_of_embeddings:
        if not isinstance(emb_list, (list, np.ndarray)):
            logging.error("Each element of embedings must be an np-array")
            return []
        

    if image_names == [] or list_of_embeddings == []:
        return []

    resultats = []
    
    for i in range(len(list_of_embeddings)):  # Browse all images

        embeddings_image_i = list_of_embeddings[i]

        # Compare faces in the same image
        for k in range(len(embeddings_image_i)):

            for l in range(k + 1, len(embeddings_image_i)):  # Évite de comparer un visage à lui-même

                #converted the data that was in str to float (removing the Nones)
                embeddings_image_i[k] = [float(x) for x in embeddings_image_i[k] if x is not None]
                embeddings_image_i[l] = [float(x) for x in embeddings_image_i[l] if x is not None]

                #convert the processed data into a 1-D table containing only numbers
                vecteur_i_k = np.array(embeddings_image_i[k], dtype=float)
                vecteur_i_l = np.array(embeddings_image_i[l], dtype=float)

                #similarity calculation 
                sim = 1 - cosine(vecteur_i_k, vecteur_i_l)

                resultat = {
                    "image": image_names[i],
                    "visage_1": k,
                    "visage_2": l,
                    "similarite": float(sim) #so that it does not display as np.float
                }
                resultats.append(resultat)

        logging.info(f" All the sim in the image  {image_names[i]} are calculate .")


        if len(list_of_embeddings) == 1 : 
            logging.warning(f"There is just one picture")
            continue

        # Compare face with others images 
        for j in range(i + 1, len(list_of_embeddings) ):

            embeddings_image_j = list_of_embeddings[j]
            for k in range(len(embeddings_image_i)):
                for l in range(len(embeddings_image_j)):

                    embeddings_image_i[k] = [float(x) for x in embeddings_image_i[k] if x is not None]
                    embeddings_image_j[l] = [float(x) for x in embeddings_image_j[l] if x is not None]

                    #we convert the cleaned data into a table containing only numbers
                    vecteur_i_k = np.array(embeddings_image_i[k], dtype=float)
                    vecteur_j_l = np.array(embeddings_image_j[l], dtype=float)

                    sim = 1 - cosine(vecteur_i_k, vecteur_j_l)

                    resultat = {
                        "image_1": image_names[i],
                        "visage_1": k,
                        "image_2": image_names[j],
                        "visage_2": l,
                        "similarite": float(sim)  
                    }
                    resultats.append(resultat)
        logging.info(f" All the sim in the image  {image_names[i]}  and the image {image_names[j]} are calculate .")

    for rslt in resultats:

        if not isinstance(rslt, dict):
            raise TypeError("Each element must be a dictionnary.")

        if  rslt is None or rslt == [[]] or rslt == {} :
            logging.warning("Results are empty.")
            return []
        else:
            continue

        
    print(json.dumps(resultats, indent=4)) 

    return resultats



