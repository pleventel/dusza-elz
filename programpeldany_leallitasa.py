from read_dir import read_dir
from hiba import hiba
import os
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
def programpeldany_leallitasa(path: str,):
    adat = read_dir(path)
    print("Jelenleg futó programpéldányok:")
    i = 1
    lehetsegesek = []
    for folyamat in list(adat['FOLYAMATOK']):
        print(f"{i}. folyamat: {folyamat['név'][0][1]}")
        lehetsegesek.append(folyamat['név'][0][1])
        i += 1
    print("Válassza ki a leállítani kívánt folyamatot!")
    kod = input("Adja meg a leállítani kívánt folyamat azonosítóját!\t")
    if kod not in (lehetsegesek):
        hiba("Sajnos ez egy hibásan megadott azonosító.")
    os.remove(str(str(path), "\\", adat['FOLYAMATOK']['név'], "-", [kod]))
    print("A megadott azonosítójú programpéldány leállítása megtörtént.")