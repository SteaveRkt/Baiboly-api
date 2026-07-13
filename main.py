from typing import Annotated,List,Dict,Any
from fastapi import FastAPI, HTTPException,Path,Query
from pathlib import Path
from starlette import status
import json

app = FastAPI()

baiboly=Path("baiboly-json")

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
    for f in baiboly.rglob("*.json"):
        with open (f,encoding="utf-8") as l:
            livre=json.load(l)
            anarana=livre["meta"]["name"].lower().replace(" ","")
        if nom_livre in anarana :
            premier_chapitre =livre["1"]
            return premier_chapitre
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Livre non trouvé")

#affichage d'un verset d"un livre
                    

            
