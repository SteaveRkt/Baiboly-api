from typing import Annotated,List,Dict,Any
from fastapi import FastAPI, HTTPException,Path,Query
from pathlib import Path
from starlette import status
import json

app = FastAPI()

baiboly=Path("baiboly-json")

def trouve_livre (nom:str,chap:int,fast_rech:bool):
    for f in baiboly.rglob('*.json'):
        with open(f,encoding="utf-8") as l:
            livre=json.load(l)
            anarana=livre["meta"]["name"].lower().replace(" ","")
            if (nom in anarana) and fast_rech:
                return livre[str(chap)]
            elif nom==anarana and (not fast_rech):
                if chap > livre["meta"]["chapter_number"]:
                    return False
                return livre[str(chap)]
    return False


#liste des livres
@app.get("/liste",status_code=status.HTTP_200_OK)
async def liste_livre():
    data : List[Dict[str,Any]]=[]
    for f in baiboly.rglob("*.json"):
        with open(f,encoding="utf-8") as b:
            boky=json.load(b)
            anarana=boky["meta"]["name"]
            dic:Dict[str,Any]={"id":boky["meta"]["order"],"titre":anarana,"abreviation":anarana[:3].upper(),"testameta":f.parent.stem.split()[1],"nombre_chapitre":boky["meta"]["chapter_number"]}
            data.append(dic)
    data=sorted(data,key=lambda x:x["id"])#for x in data return x["id"]
    return data


#premier chapitre d'un livre
@app.get("/livre",status_code=status.HTTP_200_OK)
async def contenu_livre(nom_livre:Annotated[str,Query(min_length=2)]):
    nom_livre=nom_livre.lower().replace(" ","")
    reponse=trouve_livre(nom_livre,1,True)
    if not reponse:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Livre non trouvé")
    return reponse

#affichage d'un verset d"un livre
@app.get('/livre/{nom_livre}',status_code=status.HTTP_200_OK)
async def verset(nom_livre:str,chapitre:Annotated[int,Query(gt=0)],deb_verset:int|None=None,fin_verset:int|None=None):
    nom_livre =nom_livre.lower().replace(" ","")
    res:Dict[str,str]
    reponse= trouve_livre(nom_livre,chap=chapitre,fast_rech=False)
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
    
    
    




            
