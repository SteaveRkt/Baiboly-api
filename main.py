from typing import Annotated,List,Dict,Any
from fastapi import FastAPI, HTTPException,Path
from pathlib import Path
from starlette import status
import json

app = FastAPI()

baiboly=Path("baiboly-json")
Testamenta_Taloha = Path("baiboly-json/Testameta taloha")
Testamenta_Vaovao = Path("baiboly-json/Testameta vaovao")

#liste des livres
@app.get("/livres",status_code=status.HTTP_200_OK)
async def liste_livre():
    data : List[Dict[str,Any]]=[]
    for f in baiboly.rglob("*.json"):
        with open(f.absolute(),encoding="utf-8") as b:
            boky=json.load(b)
            anarana=boky["meta"]["name"]
            dic:Dict[str,Any]={"id":boky["meta"]["order"],"titre":anarana,"abreviation":anarana[:3].upper(),"testameta":f.parent.stem.split()[1],"nombre_chapitre":boky["meta"]["chapter_number"]}
            data.append(dic)
    data=sorted(data,key=lambda x:x["id"])#for x in data return x["id"]
    return data


#contenu d'un livre
@app.get("/livres/{nom_livre}",status_code=status.HTTP_200_OK)
async def contenu_livre(nom_livre:Annotated[str,Path()]):
    nom_livre=nom_livre.lower().replace(" ","")
    for f in baiboly.rglob("*.json"):
        with open (f,encoding="utf-8") as l:
            livre=json.load(l)
            anarana=livre["meta"]["name"].lower().replace(" ","")
        if nom_livre in anarana :
            premier_chapitre =livre["1"]
            return premier_chapitre
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Livre non trouvé")

                    

            
