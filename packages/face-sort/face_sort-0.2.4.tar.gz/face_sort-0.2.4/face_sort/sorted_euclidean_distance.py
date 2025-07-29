import os
import shutil
import json
import logging
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("face_distance.log"),
        logging.StreamHandler()
    ]
)

def calculer_stats(similarities):
    """ #calculation of the mean and standard deviation which will be used to adjust the threshold using euclidean distance 
    
    param 
    -------
        similarities : the list of dictionnary containing all the similarities (List of dictionnaries)
    
    returns
    --------
    mean : the mean of all similarities (float).
    std : the standard deviation associated to the mean (float).
    
    """
    
    valeurs = [1 / (1 + sim['similarite']) for sim in similarities]
    return np.mean(valeurs), np.std(valeurs)

def fusionner_groupes(groupes, groupe1, groupe2):
    
    """ merge two groups of a list
    param 
    -------
        groupes : A list of lists containing groups of elements (List of lists).
        groupe1 : Index of the first group to merge (List).
        groupe2 : Index of the second group to merge (List).
        
    """
    if groupe1 != groupe2:
        logging.info(f"Merger of groups {groupe1} and {groupe2}")
        groupes[groupe1 - 1].extend(groupes[groupe2 - 1])
        groupes[groupe2 - 1] = []  # Empty the second merged group



def regroupement_faces(groupes, output_folder, image_folder):
    
    """ reorganize images into folders according to detected face groups.
    param 
    -------
        groupes : a list of lists where each sublist represents a group of faces belonging to the same person.(List of lists).
        output_folder : the output folder where the sorted images will be saved (Folder).
        images_folder : the folder containing the original images. (Folder).
        
    """
    
    for idx, groupe in enumerate([g for g in groupes if g], 1):  # Ignore empty groups
        dossier_personne = os.path.join(output_folder, f"personne_{idx}")
        os.makedirs(dossier_personne, exist_ok=True)
        for id_visage in groupe:
            image_name = id_visage.split("_visage_")[0]
            shutil.copy(os.path.join(image_folder, image_name), os.path.join(dossier_personne, image_name))

def sorted_euclidean_distance(similarities, image_folder, seuil_type = "strict"):
    
    """ Sorts similarities and organizes images into folders, saves results as JSON

        similarities : A list of dictionnaries containing all similarities (List of dictionnaries).
        images_folder : the folder containing the original images. (Folder).
        seuil_type: the chosen threshold ( between "strict" , "large" or none ) (Str).
    
    """
    output_folder = os.path.join(os.path.dirname(image_folder), "output")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    groupes = []
    dejà_classés = {}

    for sim in sorted(similarities, key=lambda x: x['similarite']):  #Sort by increasing distance
        image_1, visage_1 = sim["image_1"], sim["visage_1"]
        image_2, visage_2 = sim["image_2"], sim["visage_2"]
        similarite = sim["similarite"]

        id_visage_1 = f"{image_1}_visage_{visage_1}"
        id_visage_2 = f"{image_2}_visage_{visage_2}"
            
        # Calculation of statistics 
        moyenne, ecart_type = calculer_stats(similarities)
  
        # Adjusting the threshold according to the chosen type
        if seuil_type == "strict":
            seuil = moyenne 
        elif seuil_type == "large":
            seuil = moyenne + ecart_type
        else:  # Moderate by default
            seuil=0.61
            
        
        if similarite < seuil:
            if id_visage_1 in dejà_classés and id_visage_2 in dejà_classés:
                # Merge groups if both faces are already classified
                fusionner_groupes(groupes, dejà_classés[id_visage_1], dejà_classés[id_visage_2])
            elif id_visage_1 in dejà_classés:
                groupe = dejà_classés[id_visage_1]
                groupes[groupe - 1].append(id_visage_2)
                dejà_classés[id_visage_2] = groupe
            elif id_visage_2 in dejà_classés:
                groupe = dejà_classés[id_visage_2]
                groupes[groupe - 1].append(id_visage_1)
                dejà_classés[id_visage_1] = groupe
            else:
                groupe = len(groupes) + 1
                groupes.append([id_visage_1, id_visage_2])
                dejà_classés[id_visage_1] = groupe
                dejà_classés[id_visage_2] = groupe

    regroupement_faces(groupes, output_folder, image_folder)
