from typing import Annotated,List,Dict,Any
from fastapi import FastAPI, HTTPException,Path,Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from starlette import status
import json
import random
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

baiboly=Path("baiboly-json")

def trouve_livre (nom:str,chap:int):
    for f in baiboly.rglob('*.json'):
        with open(f,encoding="utf-8") as l:
            livre=json.load(l)
            anarana=livre["meta"]["name"].lower().replace(" ","")
            if nom==anarana:
                if chap > livre["meta"]["chapter_number"]:
                    return False
                return livre[str(chap)]
    return False

def liste_des_livre(cacher_source:bool)->List[Dict[str,str]]:
    data : List[Dict[str,Any]]=[]
    for f in baiboly.rglob("*.json"):
        with open(f,encoding="utf-8") as b:
            boky=json.load(b)
            anarana=boky["meta"]["name"]
            if not(cacher_source):
                dic:Dict[str,Any]={"id":boky["meta"]["order"],"titre":anarana,"abreviation":anarana[:3].upper(),"testameta":f.parent.stem.split()[1],"nombre_chapitre":boky["meta"]["chapter_number"],"lien":f.absolute()}
            else:
                 dic:Dict[str,Any]={"id":boky["meta"]["order"],"titre":anarana,"abreviation":anarana[:3].upper(),"testameta":f.parent.stem.split()[1],"nombre_chapitre":boky["meta"]["chapter_number"]}
            data.append(dic)
    data=sorted(data,key=lambda x:x["id"])#for x in data return x["id"]
    return data


#liste des livres
@app.get("/liste",status_code=status.HTTP_200_OK)
async def liste_livre():
    reponse=liste_des_livre(cacher_source=True)
    return reponse


#premier chapitre d'un livre
@app.get("/livre",status_code=status.HTTP_200_OK)
async def contenu_livre(nom_livre:Annotated[str,Query(min_length=2)]):
    nom_livre=nom_livre.lower().replace(" ","")
    reponse=trouve_livre(nom_livre,1)
    if not reponse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Livre non trouvé")
    return reponse

#affichage d'un verset d"un livre
@app.get('/livre/{nom_livre}',status_code=status.HTTP_200_OK)
async def verset(nom_livre:str,chapitre:Annotated[int,Query(gt=0)],deb_verset:int|None=None,fin_verset:int|None=None):
    nom_livre =nom_livre.lower().replace(" ","")
    res:Dict[str,str]={"first":"value"}
    reponse= trouve_livre(nom_livre,chap=chapitre)
    if not reponse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Livre ou chapitre non trouvé")
    elif deb_verset==None and fin_verset==None:
        return reponse
    elif deb_verset != None:
        res={k:v for k,v in reponse.items() if int(k)>=deb_verset}
    elif fin_verset != None:
        res={k:v for k,v in reponse.items() if int(k)<=fin_verset}
    if len(res)==0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="il n'y a pas ce verset")
    return res
# verset aléatoire
@app.get("/random",status_code=status.HTTP_200_OK)
async def random_verset():
    liste_fichier=[f for f in baiboly.rglob("*.json")]
    random_fichier=random.choice(liste_fichier)
    with open (random_fichier,encoding="utf-8") as f:
        rd=json.load(f)
        nom_livre:str=rd["meta"]["name"]
        len_chapitre:str=rd["meta"]["chapter_number"]
        chapitre_aleatoire:str=str(random.randint(1,int(len_chapitre)))
        verset_aleatoire:str =str(random.randint(1,len(rd[chapitre_aleatoire])))
    reponse:Dict[str,str]={"nom_du_live":nom_livre,"chapitre":chapitre_aleatoire,"verset":verset_aleatoire,"content":rd[chapitre_aleatoire][verset_aleatoire]}
    return reponse
    

    
    




            
