import json
from pathlib import Path
from typing import Dict,List,Any
baiboly=Path("baiboly-json")
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