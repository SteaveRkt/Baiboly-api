import json
from pathlib import Path
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