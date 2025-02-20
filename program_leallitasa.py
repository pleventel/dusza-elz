from operator import truediv
from read_dir import read_dir,write_dir
from hiba import hiba
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
            'AKTIV': true,
            'MAGSZAM': 2,
            'MEMORIASZAM': 3
        }]
    }
}

"""
def program_leallitasa(path:str):
    adat=read_dir(path)
    folyamat=input("Adja meg a folyamat nevét:")
    valtozas=False
    for folyamatok in adat['FOLYAMATOK']:
        if(folyamatok==folyamat):
            valtozas=True
            del(adat['FOLYAMATOK'][folyamatok])
            break
    if(valtozas==False):
        hiba("Nincs ilyen folyamat")
    else:
        write_dir(path,adat)