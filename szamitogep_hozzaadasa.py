from http.client import ImproperConnectionState #szerintem ezt ki lehetne venni


from read_dir import read_dir,write_dir
from hiba import hiba
import string


lehetseges=string.ascii_letters+"0123456789"

def helyesnev(nev: str):
    for a in nev:
        if a not in lehetseges:
            return False


def szamitogep_hozzaadasa(path: str):
    """beolvasas majd adat módosítása"""
    adat=read_dir(path)

    nev=input("Számítógép neve:")
    magok=input("Magok száma:")
    memoria=input("Memória mennyisége:")
    
    if(helyesnev(nev)==False):
        hiba("Hibás név!")
    else:
        adat['SZAMITOGEPEK'].append([{'név':nev}])
        adat['SZAMITOGEPEK'][nev].append({
            'MAGSZAM':magok,
            'MEMORIASZAM':memoria})

    write_dir(path, adat)

    