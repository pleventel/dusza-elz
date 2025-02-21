**Dusza ELZ - Dokumentáció**

# 1. Bevezetés
A Dusza ELZ projekt egy klasztermenedzsment rendszer, amely lehetővé teszi a felhasználók számára a klaszteren futó folyamatok figyelését, módosítását, új programok indítását, valamint a számítógépek erőforrásainak nyomon követését. A rendszer a fájlrendszerben tárolja a klaszter állapotát, és az adatok kezelésére egyszerű szöveges fájlokat használ. A programhoz tartozó grafikus felületet a PySide6-on keresztül érhetjük el.

A projekt céljai: részvétel a Dusza Árpád Országos Programozói Emlékversenyen, a korábban elkészített program prodoktifikálásával.

# 2. Telepítési útmutató
### 2.1. Rendszerkövetelmények
- Operációs rendszer: Windows 10 vagy újabb, Linux, macOS
- Python 3.9 vagy újabb
- Szükséges csomagok: `os`, `sys`, `shutil`, `random`, `PySide6`
- Javasolt futtatási környezet: Visual Studio Code

### 2.2. Telepítés lépései
Mivel a projekt futtatható konzolból és grafikus felületen keresztül egyaránt, ezért a telepítése is kétféleképpen zajlik.

A program egyszerűbb használatának érdekében javasoljuk a grafikus környezet használatát.

#### 2.2.1. Konzolos használat
Nyissa meg a Terminált, majd kövesse a lentebb leírt lépéseket.
1. Projekt klónozása a GitHubról:
   ```bash
   git clone https://github.com/pleventel/dusza-elz.git
   ```
2. Belépés a projekt mappába:
   ```bash
   cd dusza-elz
   ```
3. Program futtatása:
   
   python menu.py
   
   Vagy: F5 gomb megnyomásával a Pythont futtatni képes környezetben (pl. Microsoft Visual Studio Code, Microsoft Visual Studio, Python IDLE).
Ezen lépéssel befejeződött a program telepítése. A használat módjáról az dokumentáció 3. pontjában olvashat.


#### 2.2.2. Grafikus programkörnyezet használata
Nyissa meg a Terminált, majd kövesse a lentebb leírt lépéseket.
1. Projekt klónozása a GitHubról - mindkét felhasználási mód esetén:
   ```bash
   git clone https://github.com/pleventel/dusza-elz.git
   ```
2. Belépés a projekt mappába - mindkét felhasználási mód esetén:
   ```bash
   cd dusza-elz
   ```
3. PySide6 telepítése a grafikus felület kezeléséhez.
    ```
    py -m pip install PySide6
    ```
4. Program futtatása
   ```bash
   python gui_menu.py
   ```
   Vagy: `F5` gomb megnyomásával a Pythont futtatni képes környezetben *(pl. Microsoft Visual Studio Code, Microsoft Visual Studio, Python IDLE)*.

# 3. Használati útmutató
A program első indításakor a menübe léphetünk be. Első lépésként mindig meg kell adni az a mappát *(gyökérkönyvtárat)*, ahol a számítógépeket modellező klaszter található. Ezen lépés a program alapvető működésének feltétele<; kihagyása esetén a program hibaüzenetet küld, továbbá nem fut le.

A program menürendszeréből az alábbi funkciókat választhatjuk:
- **Monitoring**: A klaszter aktuális állapotának lekérdezése.
- **Számítógép hozzáadása**: Új számítógép létrehozása a klaszterben.
- **Számítógép törlése**: Egy számítógép eltávolítása a klaszterből *(Ez a funkció csak abban az esetben érhető el, hogyha az adott számítógépen nem fut egyetlen program egyetlen példánya sem!)*.
- **Programpéldány indítása**: Egy már meglévő, vagy új program egy példányának futtatása.
- **Program leállítása**: Egy adott program összes példányának leállítása.
- **Program módosítása**: A futtatandó program példányszámának és erőforrásigényének módosítása.

Az almenükből a vissza gomb megnyomásával juthatunk vissza a menübe.

# 4. Fejlesztői dokumentáció
### 4.1. Fájlstruktúra
- `menu.py` - A program főmenüje, ez jelenik meg a program elindításakor is.
- `monitoring.py` - A klaszter állapotának megjelenítése.
- `szamitogep_hozzaadasa.py` - Új számítógép hozzáadása.
- `szamitogep_torlese.py` - Számítógép törlése.
- `uj_program_futtatasa.py` - Program indítása.
- `program_leallitasa.py` - Program leállítása.
- `program_modositasa.py` - Program módosítása.
- `programpeldany_leallitasa.py` - Egy adott programpéldánypéldány leállítása.
- `kihasznaltsag.py` - Számítógépek erőforrás-kihasználtságának figyelése.
- `read_dir.py` - Könyvtárak beolvasása *(tartalmazza a könyvtárba való írást, valamint a gyökérkönyvtár bekérését is)*.
- `hiba.py` - Hibakezelés, visszajelző üzenetek küldése.

# 5. Hibakezelés és hibaelhárítás
A programban található hibaüzenetek értelmezése
- **Nem található a klaszter könyvtár**: Ellenőrizze a megadott elérési utat! Próbálkozzon annak újbóli megadásával a menüben!
- **Egy folyamat nem indítható el**: Győződjön meg arról, hogy a számítógép rendelkezik elegendő szabad erőforrással a folyamat futtatására. Amennyiben lehetséges, próbálja meg a rendelkezésre álló erőforrások átcsoportosítását!
- **Egy számítógép nem törölhető**: A számítógép leállítása/törlése nem lehetséges, mivel futnak rajta folyamatok. A törléshez először állítsa le a folyamatokat!

# 6. Korlátok és ismert problémák
- Az alkalmazás nem támogatja a valós idejű klaszterkezelést.
- A program működése erősen függ a fájlrendszer állapotától.

# 7. Összegzés
A Dusza ELZ egy egyszerű, de hatékony klaszterkezelő alkalmazás, amely fájlrendszer-alapú megoldásokkal biztosítja a számítógépek és folyamatok kezelését. A dokumentáció célja, hogy segítse a felhasználókat a program telepítésében, használatában és fejlesztésében.

