from read_dir import read_dir, write_dir

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
def kihasznaltsag(path: str,szamitogep:str):
    adat=read_dir(path)
    magsum=0
    memoriasum=0
    for folyamat in adat['FOLYAMATOK']:
        for i in range(len(folyamat)):
            if(folyamat[i][0]==szamitogep):
                magsum+=folyamat[i][4]
                memoriasum+=folyamat[i][5]
    return magsum, memoriasum
