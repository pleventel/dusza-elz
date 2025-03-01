from operator import truediv
from read_dir import read_dir,write_dir
from hiba import hiba
from kihasznaltsag import kihasznaltsag
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

def monitoring(path:str):
    adat=read_dir(path)
    futofolyamatok=[]
    print("Számítógépek a clusterben: \n")
    for szamitogep in adat['SZAMITOGEPEK']:
        nev=szamitogep
        maxmag=szamitogep['MAGSZAM']
        maxmem=szamitogep['MEMORIASZAM']
        usedmag,usedmem=kihasznaltsag(path,szamitogep)
        print("Számítógép neve: ",nev," számítógép maximális magja: ",maxmag, " számítógép nem felhsznált magja: ", maxmag-usedmag, " szamitógép maximális memótiája: ",maxmem, " számítógép nem felhasznált memóriája: ",maxmem-usedmem)
    print("Futó folyamatok:\n") #én ezt a részt így értelmeztem ha ez nem jó akkor nem tudom hogy kéne értelmezni
    for folyamat in adat['Folyamatok']:
        
        aktiv=0;inaktiv=0
        futofolyamatok.append(folyamat)
        print("Futófolyamat neve: ",folyamat, "futó folyamat azpmosítója: ", folyamat['KOD'], "folyamat által használt memória: ",folyamat['MEMORIASZAM'],"folyamat által használt magok: ",folyamat['MAGSZAM'] )
        if(folyamat['AKTIV']==True):
            aktiv+=1
        else:
            inaktiv+=1
            
    print("Futó folyamatok és darabszámaik:")
    while(len(futofolyamatok)!=0):
        print("Folyamat neve: ",futofolyamatok[0], "futó folyamat darabszáma: ", futofolyamatok.count(futofolyamatok[0]))
        for i in range (1,len(futofolyamatok)):
            if futofolyamatok[i]==futofolyamatok[0]:
                futofolyamatok.pop(i)
        futofolyamatok.pop(0)
    print("aktív folymatok: ",aktiv, "inaktiv folyamatok: ",inaktiv)
    print("Kluszter állapota: HELYES") #???
    print("szeretne konkrét programot megadni? (i/n)")
    ans=input()
    if(ans=="i"):
        print("adja meg a folyamatot")
        foly=input()
        for folyamat in adat['FOLYAMAT']:
            if folyamat==foly:
                print("Számítógép amelyen fut a folyamat: ",folyamat['SZAMITOGEP'],"a folyamat által felhasznált erőforrások: ",folyamat['MAGSZAM']," ",folyamat['MEMORIASZAM'])
    
