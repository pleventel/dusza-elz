
"""
!!!
{
    'SZAMITOGEPEK': {
        'név': {
            'MAGSZAM': 2,
            'MEMORIASZAM': 3
        }
    },
    'FOLYAMATOK': {
        'név': [{
            'SZAMITOGEP': "asd",
            'KOD': "qwetrrwr",
            'INDITAS': 9812378912783,
            'AKTIV': True,
            'MAGSZAM': 2,
            'MEMORIASZAM': 3
        }]
    }
}

"""

from os import remove, makedirs, listdir, rmdir, system
from hiba import hiba as error
from hiba import warning
import datetime

def read_dir(path):
    path_separator = ""
    if not path[:-1] == "\\" and not path[:-1] == "/":
        if len(path) > len(path.replace("/", "")): # hacky ahh solution
            path = path + "/"
            path_separator = "/"
        else: 
            path = path + "\\"
            path_separator = "\\"
    
    home = listdir(path)
    
    klaszter = []
    try:
        with open(f"{path}.klaszter", "r", encoding='utf-8') as klaszterfile:
            lines = klaszterfile.readlines()
            lines = [x.rstrip() for x in lines]
            for i in range(0, int(len(lines)/4)):
                klaszter.append({
                    'NEV': lines[i*4],
                    'FOLYAMATSZAM': int(lines[i*4+1]),
                    'MAGSZAM': int(lines[i*4+2]),
                    'MEMORIASZAM': int(lines[i*4+3])
                })
    except:
        error("nincs vagy hibás a .klaszer file") # át kéne irni hibara
        return -1
    
    adatok = dict()
    adatok['SZAMITOGEPEK'] = dict()
    adatok['FOLYAMATOK'] = dict()

    home.remove(".klaszter")
    print(path)
    for szamitogep in home:
        folyamatok = listdir(f"{path}{szamitogep}")
        konfig = ".szamitogep_konfig"
        if not konfig in folyamatok:
            konfig = ".szamitogep_config"
            if not konfig in folyamatok:
                error(f"NINCS KONFIG FILE A {szamitogep} MAPPÁBAN")
                return -1

        with open(f"{path}{szamitogep}{path_separator}{konfig}", "r", encoding='utf-8') as szamitogepfile:
            lines = szamitogepfile.readlines()
            lines = [x.rstrip() for x in lines]
            adatok["SZAMITOGEPEK"][szamitogep] = {
                'MAGSZAM': int(lines[0]),
                'MEMORIASZAM': int(lines[1])
            }
            
            folyamatok.remove(konfig)

            for folyamat in folyamatok:
                nev = folyamat.split("-")[0]
                kod = folyamat.split("-")[1]
                with open(f"{path}{szamitogep}{path_separator}{folyamat}", "r", encoding='utf-8') as folyamatfile:
                    lines = folyamatfile.readlines()
                    lines = [x.rstrip() for x in lines]
                    if not nev in adatok["FOLYAMATOK"].keys():
                        adatok["FOLYAMATOK"][nev] = []
                    adatok["FOLYAMATOK"][nev].append({
                        'SZAMITOGEP': szamitogep,
                        'KOD': kod,
                        'INDITAS': lines[0], # ---------------------------------------------------------- IDOPONT KIOLVASASA ide
                        'AKTIV': (True if lines[1]=="AKTÍV" else False),
                        'MAGSZAM': int(lines[2]),
                        'MEMORIASZAM': int(lines[3])
                    })
    # aktiv = sum(sum((1 if y['AKTIV'] == True else 0) for y in x) for x in list(adatok['FOLYAMATOK'].values()))
    # inaktiv = sum(sum((1 if y['AKTIV'] == False else 0) for y in x) for x in list(adatok['FOLYAMATOK'].values()))
    # print(aktiv, inaktiv)
    return adatok


def get_cluster(path):
    path_separator = ""
    if not path[:-1] == "\\" and not path[:-1] == "/":
        if len(path) > len(path.replace("/", "")): # hacky ahh solution
            path = path + "/"
            path_separator = "/"
        else: 
            path = path + "\\"
            path_separator = "\\"
    
    home = listdir(path)
    
    klaszter = []
    try:
        with open(f"{path}.klaszter", "r", encoding='utf-8') as klaszterfile:
            lines = klaszterfile.readlines()
            lines = [x.rstrip() for x in lines]
            for i in range(0, int(len(lines)/4)):
                klaszter.append({
                    'NEV': lines[i*4],
                    'FOLYAMATSZAM': int(lines[i*4+1]),
                    'MAGSZAM': int(lines[i*4+2]),
                    'MEMORIASZAM': int(lines[i*4+3])
                })
    except:
        error("nincs vagy hibás a .klaszer file") # át kéne irni hibara
        return -1
    
    adatok = dict()
    adatok['SZAMITOGEPEK'] = dict()
    adatok['FOLYAMATOK'] = dict()

    home.remove(".klaszter")
    print(path)
    for szamitogep in home:
        folyamatok = listdir(f"{path}{szamitogep}")
        konfig = ".szamitogep_konfig"
        if not konfig in folyamatok:
            konfig = ".szamitogep_config"
            if not konfig in folyamatok:
                error(f"NINCS KONFIG FILE A {szamitogep} MAPPÁBAN")
                return -1

        with open(f"{path}{szamitogep}{path_separator}{konfig}", "r", encoding='utf-8') as szamitogepfile:
            lines = szamitogepfile.readlines()
            lines = [x.rstrip() for x in lines]
            adatok["SZAMITOGEPEK"][szamitogep] = {
                'MAGSZAM': int(lines[0]),
                'MEMORIASZAM': int(lines[1])
            }
            
            folyamatok.remove(konfig)

            for folyamat in folyamatok:
                nev = folyamat.split("-")[0]
                kod = folyamat.split("-")[1]
                with open(f"{path}{szamitogep}{path_separator}{folyamat}", "r", encoding='utf-8') as folyamatfile:
                    lines = folyamatfile.readlines()
                    lines = [x.rstrip() for x in lines]
                    if not nev in adatok["FOLYAMATOK"].keys():
                        adatok["FOLYAMATOK"][nev] = []
                    adatok["FOLYAMATOK"][nev].append({
                        'SZAMITOGEP': szamitogep,
                        'KOD': kod,
                        'INDITAS': lines[0], # ---------------------------------------------------------- IDOPONT KIOLVASASA ide
                        'AKTIV': (True if lines[1]=="AKTÍV" else False),
                        'MAGSZAM': int(lines[2]),
                        'MEMORIASZAM': int(lines[3])
                    })
    # aktiv = sum(sum((1 if y['AKTIV'] == True else 0) for y in x) for x in list(adatok['FOLYAMATOK'].values()))
    # inaktiv = sum(sum((1 if y['AKTIV'] == False else 0) for y in x) for x in list(adatok['FOLYAMATOK'].values()))
    # print(aktiv, inaktiv)
    return klaszter

    

def write_dir(path, adatok):
    path_separator = ""
    if not path[:-1] == "\\" and not path[:-1] == "/":
        if len(path) > len(path.replace("/", "")): # hacky ahh solution
            path = path + "/"
            path_separator = "/"
        else: 
            path = path + "\\"
            path_separator = "\\"

    home = listdir(path)

    # <><REMOVING EVERYTHING><>
    try:
        remove(f"{path}.klaszter")
        home.remove(".klaszter")
    except:
        warning(f"NINCS '{path}.klaszter' FILE!")

    for szamitogep in home:
        files = listdir(f"{path}{szamitogep}")
        for file in files:
            remove(f"{path}{szamitogep}{path_separator}{file}")
        rmdir(f"{path}{szamitogep}{path_separator}")

    # <>< ----------------- ><>

    klaszter = ""
    for folyamat in adatok['FOLYAMATOK'].keys():
        folyamatszam = len(adatok['FOLYAMATOK'][folyamat])
        magszam = sum(x['MAGSZAM'] for x in adatok['FOLYAMATOK'][folyamat])
        memoriaszam = sum(x['MEMORIASZAM'] for x in adatok['FOLYAMATOK'][folyamat])

        klaszter = f"{klaszter}\n{folyamat}\n{folyamatszam}\n{magszam}\n{memoriaszam}"
    klaszter = klaszter[1:]

    with open(f"{path}.klaszter","w", encoding="utf-8") as f:
        f.write(klaszter)

    for szamitogep in adatok['SZAMITOGEPEK'].keys():
        makedirs(f"{path}{szamitogep}")
        with open(f"{path}{szamitogep}{path_separator}.szamitogep_konfig", "w", encoding="utf-8") as f:
            f.write(f"{adatok['SZAMITOGEPEK'][szamitogep]['MAGSZAM']}\n{adatok['SZAMITOGEPEK'][szamitogep]['MEMORIASZAM']}")
    
    for folyamatnev in adatok['FOLYAMATOK'].keys():
        for folyamat in adatok['FOLYAMATOK'][folyamatnev]:
            filepath = f"{path}{folyamat['SZAMITOGEP']}{path_separator}{folyamatnev}-{folyamat['KOD']}" 
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(
                    f"{folyamat['INDITAS']}\n{'AKTÍV' if folyamat['AKTIV'] else 'INAKTÍV'}\n{folyamat['MAGSZAM']}\n{folyamat['MEMORIASZAM']}"
                )
    return 0


if __name__ == "__main__":
     adatok = read_dir(r"/home/edi/dev/competitions/dusza-elz/minta_bemenet/cluster0")
     print(adatok)
#     pass
#     write_dir(r"C:\Users\d2\Desktop\dir\cluster1", adatok)