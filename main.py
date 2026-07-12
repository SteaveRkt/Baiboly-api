from fastapi import FastAPI, HTTPException
from pathlib import Path
import json

app = FastAPI()


Testamenta_Taloha = Path("baiboly-json/Testameta taloha")
Testamenta_Vaovao = Path("baiboly-json/Testameta vaovao")

@app.get("/livres/{nom_livre}")
async def lire_livre(nom_livre: str):
    
    TT= Testamenta_Taloha / f"{nom_livre}.json"
    TV=Testamenta_Vaovao / f"{nom_livre}.json"
    
    if TV.exists():
        with open (TV,encoding="utf-8") as tv:
            data =json.load(tv)
    if TT.exists():
        with open (TT,encoding="utf-8") as tt:
            data =json.load(tt)
    if not (TT.exists()) and not(TV.exists()):
        raise HTTPException(status_code=404,detail="livre non trouvé")
    return data # type: ignore