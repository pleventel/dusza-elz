from asyncore import write
from math import fabs
from operator import index
from read_dir import read_dir, write_dir
from hiba import hiba

def szamitogep_torlese(path: str):
    szamitogep=input("Adja meg, hogy melyik számítógépet akarja törölni:")
    adat = read_dir(path)
    for folyamat in adat['FOLYAMATOK']:
        if(folyamat[folyamat.index(szamitogep)]==str(szamitogep)):
            hiba("Aktiv folyamat")
            
    del(adat['SZAMITOGEPEK'][szamitogep])

    write_dir(path, adat)
