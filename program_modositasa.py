from read_dir import read_dir, write_dir
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

def program_modositasa(path:str):
    adat=read_dir(path)
    program=input("Adja meg melyik programon szeretne változtatni:")
    modositando=int(input("Kérjük adja meg mit szeretne módosítani: 1:Program erőforrás igénye, 2:Program futtatandó példányszámainak módsítása "))
    if(not(modositando==1 or modositando==2)):
        hiba("Hibás választás")
    else:
        if(modositando==1):
            magok=int(input("Szükséges magok száma: "))
            memoria=int(input("Szükséges memória száma:"))
            for dolog in adat['FOLYAMATOK'][program]:
                for i in range (len(adat['FOLYAMATOK'][program])):
                    adat['FOLYAMATOK'][program][i]['MAGSZAM']=magok
                    adat['FOLYAMATOK'][program][i]['MEMORIASZAM']=memoria
        else:
            darab=input("Adja meg, hogy hány darabot szeretne futtatni:")
            temp=adat['Folyamatok'][program][0]
            adat['Folyamatok'][program].append(temp)
        write_dir(path,adat)




