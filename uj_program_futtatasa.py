from sqlite3 import Time
from kihasznaltsag import kihasznaltsag
from read_dir import read_dir,write_dir
from hiba import hiba
import random
import string
import time

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


def uj_program_futtatasa(path: str):
    adat=read_dir(path)
    gepen=input("Adja meg, hogy melyik számítógépenszeretné futtatni:")
    program=input("Adja meg, hogy melyik programot szeretné elindítani:")
    hasznalt_mag,hasznalt_memoria=kihasznaltsag(path,gepen)
    if(adat['SZAMITOGEPEK'][gepen]['MAGSZAM']<hasznalt_mag+adat['FOLYAMATOK'][program][0]['MAGSZAM'] or adat['SZAMITOGEPEK'][gepen]['MEMORIASZAM']<hasznalt_memoria+adat['FOLYAMATOK'][program][0]['MEMORIASZAM']):
        hiba("Kevés Mag vagy Memória")
    else:
        azonosito=""
        lehetseges=string.ascii_lowercase
        for i in range (6):
            azonosito+=lehetseges[random.randrange(0,len(lehetseges))]
        ido=time.time
        mag=adat['FOLYAMATOK'][program][0]['MAGSZAM']
        memoria=adat['FOLYAMATOK'][program][0]['MEMORIASZAM']
        adat['FOLYAMATOK'][program].append({'SZAMITOGEP':gepen,'KOD':azonosito,'INDITAS':ido,'AKTIV':True,'MAGSZAM':mag,'MEMORIASZAM':memoria})
        write_dir(path,adat)