from hiba import hiba
from program_leallitasa import program_leallitasa
from read_dir import read_dir, get_cluster
from szamitogep_torlese import szamitogep_torlese
from szamitogep_hozzaadasa import szamitogep_hozzaadasa
from program_leallitasa import program_leallitasa
from program_modositasa import program_modositasa
from uj_program_futtatasa import uj_program_futtatasa


def elsoindulas(utvonal):

    if utvonal == "":
        print("Üdvözüljük a programban!")
        utvonal = input("Kérem adja meg a gyökérkönyvtár elérési útját!\t")
    
    return utvonal


def fomenu():
    print("Klaszter állapot:")
    adatok = get_cluster(eleresiut)
    realadatok = read_dir(eleresiut)
    l = 4
    for klaszter in adatok:
        print(f"{klaszter['NEV']}:")
        print(f"\t{klaszter['FOLYAMATSZAM']} példányszám;")
        print(f"\t{klaszter['MAGSZAM']} milimag;")
        print(f"\t{klaszter['MEMORIASZAM']} MB.")
    
    # Felhasznált és rendelkezésre álló energiaforrások számítása
    magsum = sum(int(x['MAGSZAM']) for x in adatok)
    memsum = sum(int(x['MEMORIASZAM']) for x in adatok)
    maxmag = 0
    maxmem = 0
    for gep in realadatok['SZAMITOGEPEK'].keys():
        maxmag += int(realadatok['SZAMITOGEPEK'][gep]['MAGSZAM'])
        maxmem += int(realadatok['SZAMITOGEPEK'][gep]['MEMORIASZAM'])
    if magsum > maxmag:
        hiba("TÖBB A MAGSZÁM A MEGENGEDETTNÉL!")
    if memsum > maxmem:
        hiba("TÖBB A MEMÓRIA A MEGENGEDETTNÉL!")
    
    print("Főmenü")
    print("Válasszon az alábbi menüpontok közül!")
    print("1. Monitoring")
    print("2. Számítógép törlése")
    print("3. Számítógép hozzáadása")
    print("4. Program leállítása")
    print("5. Program módosítása")
    print("6. Új programpéldány futtatása")
    print("7. Programpéldány leállítása")
    valasztas = int(input("Adja meg választását (1-7)!\t"))
    menupont(valasztas)


def menupont(bemenet):
    if bemenet == 1:
        monitoring_menu()
    elif bemenet == 2:
        szamitogep_torlese(eleresiut)
    elif bemenet == 3:
        szamitogep_hozzaadasa(eleresiut)
    elif bemenet == 4: # Prog. leállítása
        program_leallitasa(eleresiut)
    elif bemenet == 5: # Prog. módosítása
        program_modositasa(eleresiut)
    elif bemenet == 6: # Új programpéld. futtatása
        uj_program_futtatasa(eleresiut)
    elif bemenet == 7: # Programpéld. leállítása
        pass
    else:
        menupont_ujra()


def menupont_ujra():
    print("Kérem adjon meg egy helyes menüválasztást!")
    print("1. Monitoring")
    print("2. Számítógép törlése")
    print("3. Számítógép hozzáadása")
    print("4. Program leállítása")
    print("5. Program módosítása")
    print("6. Új programpéldány futtatása")
    print("7. Programpéldány leállítása")
    valasztas = int(input("Adja meg választását (1-7)!\t"))
    menupont(valasztas)



def monitoring_menu():
    while True:
        print("Monitoring menü")
        print("Válasszon az alábbi menüpontok közül!")
        print("1. Számítógépek kihasználtsága")
        print("2. Futó programik kilistázása")
        print("3. Aktív és inaktív folyamatok száma")
        print("4. Klaszter állapota")
        print("5. Konkrét program adatainak vizsgálata (a program összes futó példányán)")
        print()
        print("6. Visszalépés a főmenübe")
        valasztas = int(input("Adja meg választását (1-5)!\t"))
        monitoring_menupont(valasztas)


def monitoring_menupont(bemenet):

    if bemenet == 1:
        kihasznaltsag()
    elif bemenet == 2:
        programpeldanyok()
    elif bemenet == 3:
        aktivprogramok()
    elif bemenet == 4: # Klaszter állapota
        klaszterallapot()
    elif bemenet == 5:
        konkretprogram()
    elif bemenet == 6:
        fomenu()
    else:
        hiba("\n\nHELYTELEN VALASZTAS!\n")
        return -1

# ---------- o ----------
# Alprogramok menüinek létrehozása

def alprogramok_menuvalasztas(bemenet):
    if bemenet == 1:
        fomenu()
    if bemenet == 2:
        monitoring_menu()
    else:
        alprogramok_menu_ujra()


def alprogramok_menu_ujra():
    print("Kérem adjon meg egy helyes menüválasztást!")
    print("1. Visszalépés a főmenübe")
    print("2. Visszalépés a Monitoring menübe.")
    valasztas = int(input("Adja meg választását (1-2)!\t"))
    alprogramok_menuvalasztas(valasztas)

# ---------- o ----------
# Alprogramok

def kihasznaltsag():
    adatok = read_dir(eleresiut)
    print("Számítógépek kihasználtsága")
    for szamitogep in adatok['SZAMITOGEPEK'].keys():
        print(szamitogep)
        print("\tMaximális erőforrások:")
        print(f"\tProcesszor: {adatok['SZAMITOGEPEK'][szamitogep]['MAGSZAM']} milimag;")
        print(f"\tMemória: {adatok['SZAMITOGEPEK'][szamitogep]['MEMORIASZAM']} MB.")
    # adatok['SZAMITOGEPEK'][szamitogep]
    print()
    print("1. Visszalépés a főmenübe")
    print("2. Visszalépés a Monitoring menübe.")
    valasztas = int(input("Adja meg választását (1-5)!\t"))
    alprogramok_menuvalasztas(valasztas)


def programpeldanyok():
    adatok = read_dir(eleresiut)
    print("Futó programpéldányok listázása")

    for folyamatnev in adatok['FOLYAMATOK'].keys():
        print(f"{folyamatnev} példányai:")
        for folyamat in adatok['FOLYAMATOK'][folyamatnev]:

            print(f"\t{folyamatnev}-{folyamat['KOD']}")
            print(f"\t\t számítógép: {folyamat['SZAMITOGEP']};")
            
            print(f"\t\t inditasi idő: {folyamat['INDITAS']};")
            
            print(f"\t\t aktivitás: {'AKTIV' if folyamat['AKTIV'] else 'INAKTIV'};")
            
            print(f"\t\t magszám: {folyamat['MAGSZAM']} milimag;")
            
            print(f"\t\t memóriaszám: {folyamat['MEMORIASZAM']} MB.")

    print()
    print("1. Visszalépés a főmenübe")
    print("2. Visszalépés a Monitoring menübe.")
    valasztas = int(input("Adja meg választását (1-5)!\t"))
    alprogramok_menuvalasztas(valasztas)


def aktivprogramok():
    adatok = read_dir(eleresiut)
    aktiv = sum(sum((1 if y['AKTIV'] == True else 0) for y in x) for x in list(adatok['FOLYAMATOK'].values()))
    inaktiv = sum(sum((1 if y['AKTIV'] == False else 0) for y in x) for x in list(adatok['FOLYAMATOK'].values()))
    print(f"A klaszteren futó összes programpéldány közül {aktiv} db aktív folyamat és {inaktiv} db inaktív folyamat.")
    print()
    print("1. Visszalépés a főmenübe")
    print("2. Visszalépés a Monitoring menübe.")
    valasztas = int(input("Adja meg választását (1-5)!\t"))
    alprogramok_menuvalasztas(valasztas)


def klaszterallapot():
    adatok = get_cluster(eleresiut)
    realadatok = read_dir(eleresiut)
    l = 4
    for klaszter in adatok:
        print(f"{klaszter['NEV']}:")
        print(f"\t{klaszter['FOLYAMATSZAM']} példányszám;")
        print(f"\t{klaszter['MAGSZAM']} milimag;")
        print(f"\t{klaszter['MEMORIASZAM']} MB.")
    
    magsum = sum(int(x['MAGSZAM']) for x in adatok)
    memsum = sum(int(x['MEMORIASZAM']) for x in adatok)
    maxmag = 0
    maxmem = 0
    for gep in realadatok['SZAMITOGEPEK'].keys():
        maxmag += int(realadatok['SZAMITOGEPEK'][gep]['MAGSZAM'])
        maxmem += int(realadatok['SZAMITOGEPEK'][gep]['MEMORIASZAM'])
    # ez hibas megoldas de mind1
    if magsum > maxmag:
        hiba("TÖBB A MAGSZÁM A MEGENGEDETTNÉL!")
    if memsum > maxmem:
        hiba("TÖBB A MEMÓRIA A MEGENGEDETTNÉL!")


    print()
    print("1. Visszalépés a főmenübe")
    print("2. Visszalépés a Monitoring menübe.")
    valasztas = int(input("Adja meg választását (1-5)!\t"))
    alprogramok_menuvalasztas(valasztas)


def konkretprogram():
    adatok = read_dir(eleresiut)
    program = input("Adja meg a kiválasztott program nevét!\t")
    folyamatok = []
    for folyamat in adatok['FOLYAMATOK'][program]:
        folyamatok.append([folyamat['KOD'], folyamat['SZAMITOGEP'], folyamat['MAGSZAM'], folyamat['MEMORIASZAM']])
    print(f"A kiválasztott '{program}' információi:")
    for folyamat in folyamatok:
        print(f"Azonosító: {folyamat[0]}, Számítógép az.: {folyamat[1]}, Processzor igény: {folyamat[2]/1000} processzormag, Memória igény: {folyamat[3]} MB.")
    print()
    print("1. Visszalépés a főmenübe")
    print("2. Visszalépés a Monitoring menübe.")
    valasztas = int(input("Adja meg választását (1-5)!\t"))
    alprogramok_menuvalasztas(valasztas)

eleresiut = elsoindulas("")
fomenu()