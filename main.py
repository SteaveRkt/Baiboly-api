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
    def parcours(dossier): 
        for f in sorted(dossier.iterdir()):
            if f.is_dir(): 
                parcours(f) 
            elif f.is_file(): 
                with open(f.absolute(),encoding="utf-8") as b:
                    boky=json.load(b)
                    anarana=boky["meta"]["name"]
                dic={"id":boky["meta"]["order"],"titre":anarana,"abreviation":anarana[:3].upper(),"testameta":f.parent.stem.split()[1],"nombre_chapitre":boky["meta"]["chapter_number"]}
                data.append(dic)
    parcours(Path(baiboly))
    data=sorted(data,key=lambda x:x["id"])#for x in data return x["id"]
    return data


#contenu d'un livre
@app.get("/livres/{nom_livre}",status_code=status.HTTP_200_OK)
async def contenu_livre(nom_livre:Annotated[str,Path()]):
    def trouver_titre (dossier,nom):
        for f in sorted(dossier.iterdir()):
            if f.is_dir():
                res=trouver_titre(f,nom)
                if res is not False:
                    return res
            elif f.is_file():
                with open (f.absolute(),encoding="utf-8") as l:
                    livre=json.load(l)
                    anarana=livre["meta"]["name"].lower().replace(" ","")
                if nom in anarana :
                    premier_chapitre =livre["1"]
                    return premier_chapitre
        return False
    nom_livre=nom_livre.lower().replace(" ","")
    data=trouver_titre(baiboly,nom_livre)
    if data==False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Livre non trouvé")
    return data
                    

            
