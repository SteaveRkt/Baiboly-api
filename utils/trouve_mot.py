from pathlib import Path
from typing import List,Dict,Any
import json
baiboly=Path("baiboly-json")
def trouver_tout_les_mot(mot:str)->List[Dict[str,str]]:
    mot_vaovao=mot.lower().split()
    reponse:List[Any]=[]
    for f in baiboly.rglob("*.json"):
        with open (f,encoding="utf-8") as b:
            boky=json.load(b)
            for i in range(1,len(boky)):
                resultat={k:v for k,v in boky[str(i)].items() if all(m in v.lower() for m in mot_vaovao)}
                if len(resultat)!=0:
                    for k,v in resultat.items():
                        reponse.append({"livre":boky["meta"]["name"],"chapitre":str(i),"verset":k,"content":v})
    return reponse

