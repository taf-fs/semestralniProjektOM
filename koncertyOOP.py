from datetime import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from typing import List
from math import ceil

class Kapela:
    """Trida Kapela reprezentuje kapelu. Jeji inicializacni parametry jsou nazev kapely, rok zalozeni,
    zemi puvoudu, zanr, seznam clenu. Pri inicializaci muze byt seznam clenu prazdny, totiz pri
    inicializaci instance tridy Clen se clen automaticky pridava to prislusne kapely"""
    def __init__(self, nazev:str, rokZalozeni:int, zemePuvodu:str, zanr:str, clenove:List['ClenKapely']) -> None:
        self.nazev = nazev
        self.rokZalozeni = rokZalozeni
        self.zemePuvodu = zemePuvodu
        self.zanr = zanr
        self.clenove = clenove

    def vypisCleny(self) -> str:
        """Metoda vypisCleny() vraci formatovany string se seznamem clenu"""
        members = [f"Člen {i+1}: {self.clenove[i].celeJmeno()} - {self.clenove[i].nastroj}" for i in range(len(self.clenove))]
        vypis = "\n".join(members)
        return vypis
        
        
    def prumernyVek(self) -> float:
        """Metoda prumernyVek() vypocita prumerny vek a vraci ho jako float"""
        soucet = 0
        for clen in self.clenove:
            soucet += clen.vek()
        return soucet / len(self.clenove)
    
    def nastrojFiltr(self, nastroj:str) -> bool:
        """Metoda nastrojFiltr() slouzi jako filtracni funkce, ktera vraci True pokud se nastroj
        vyskytuje v repertoaru alespon jednoho z clenu kapely"""
        return any(nastroj in clen.nastroj for clen in self.clenove)

class KapelaRevival(Kapela):
    """Trida KapelaRevival dedi z tridy Kapela. Je doplnena o jeden inicializacni parametr navic, jeho puvodni kapelu"""
    def __init__(self, nazev:str, rokZalozeni:int, zemePuvodu:str, zanr:str, clenove:List['ClenKapely'], puvodniKapela:Kapela):
        super().__init__(nazev, rokZalozeni, zemePuvodu, zanr, clenove)
        self.puvodniKapela = puvodniKapela 

class ClenKapely:
    """Trida ClenKapely reprezentuje clena kapely. Jeji inicializacni parametry jsou jmeno clena,
    jeho prijmeni, datum narozeni, nastroje, na ktere hraje, a kapela, kterym je clenem."""
    def __init__(self, jmeno:str, prijmeni:str, datumNarozeni:date, nastroj:str, kapela:Kapela) -> None:
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.datumNarozeni = datumNarozeni
        self.nastroj = nastroj
        self.kapela = kapela

        # pri vytvoreni instance se clen rovnou prida do seznamu clenu kapely
        self.kapela.clenove.append(self)

    def celeJmeno(self) -> str:
        """Metoda celeJmeno() vraci formatovane cele jmeno jako string"""
        celeJmeno = f"{self.jmeno} {self.prijmeni}".title()
        return celeJmeno
    
    def vek(self) -> int:
        """Metoda vek() vypocita a vraci vek clena kapely"""
        now = datetime.now()
        vek = now.year - self.datumNarozeni.year
        if not (now.month > self.datumNarozeni.month and now.day >= self.datumNarozeni.day):
            vek -= 1
        return vek

class Klub:
    """Trida Klub reprezentuje klub. Jeji inicializacni parametry jsou nazev klubu, adresa a kapacita."""
    def __init__(self, nazev:str, adresa:str, kapacita:int) -> None:
        self.nazev = nazev
        self.adresa = adresa
        self.kapacita = kapacita

    def mesto(self) -> str:
        """Metoda mesto() vraci mesto, ve kterem se klub nachazi.
        Spoleha se na to, ze self.adresa je string ve formatu "Ulice 10, Mesto" """
        return self.adresa.split(", ")[-1]

class Koncert:
    """Trida Koncert reprezentuje koncert. Jeji inicializacni parametry jsou nazev koncertu, datum a cas konani, 
    misto konani (klub), vystupujici kapela a cena vstupenky."""
    def __init__(self, nazev:str, datumKonani:date, casKonani:time, mistoKonani:Klub, vystupujiciKapela:Kapela, cenaVstupenky:int) -> None:
        self.nazev = nazev
        self.datumKonani = datumKonani
        self.casKonani = casKonani
        self.mistoKonani = mistoKonani
        self.vystupujiciKapela = vystupujiciKapela
        self.cenaVstupenky = cenaVstupenky

    def celeInformace(self) -> str:
        """Metoda celeInformace() vraci vsechny dulezite informace o koncertu."""
        output = (
            f"Jmeno koncertu: {self.nazev}\n"
            f"Datum Konani: {self.datumKonani.day}. {self.datumKonani.month}. {self.datumKonani.year}\n"
            f"Misto konani: {self.mistoKonani.nazev}\n"
            f"Vystupujici kapela: {self.vystupujiciKapela.nazev}\n"
            f"Cena vstupenky: {self.cenaVstupenky}CZK"
        )
        return output
    
    def maximalniTrzba(self, sleva:int=0) -> float:
        """Metoda maximalniTrzba() vraci maximalni mozne trzby z koncertu. Je mozne zadat slevu jako parametr."""
        return self.cenaVstupenky * self.mistoKonani.kapacita * ((100-sleva) / 100)
    
    def mestoFiltr(self, mesto:str) -> bool:
        """Metoda mestoFiltr() slouzi jako filtracni funkce, ktera vraci True pokud se koncert kona v danem meste."""
        if self.mistoKonani.mesto() == mesto:
            return True
        else:
            return False
        
    def cenovyFiltr(self, dolniLimit:int, horniLimit:int) -> bool:
        """Metoda cenovyFiltr() slouzi jako filtracni funkce, ktera vraci True pokud je cena vstupenky v danem rozmezi."""
        if self.cenaVstupenky >= dolniLimit and self.cenaVstupenky <= horniLimit:
            return True
        else:
            return False


kapela1 = Kapela("kessoku band", 2022, "JP", "rock", [])
clen1_1 = ClenKapely("Goto", "Hitori", date(2005, 2, 21), "kytara", kapela1)
clen1_2 = ClenKapely("Ijichi", "Nijika", date(2004, 5, 29), "bubny", kapela1)
clen1_3 = ClenKapely("Yamada", "Ryo", date(2004, 9, 18), "basa", kapela1)
clen1_4 = ClenKapely("Kita", "Ikuyo", date(2005, 9, 18), "zpěv", kapela1)

kapela2 = Kapela("Deftones", 1988, "US", "alt metal, art rock, experimental rock", [])
clen2_1 = ClenKapely("Stephen", "Carpenter", date(1970, 8, 3), "kytara", kapela2)
clen2_2 = ClenKapely("Abe", "Cunningham", date(1973, 7, 27), "bubny", kapela2)
clen2_3 = ClenKapely("Chino", "Moreno", date(1973, 6, 20), "zpěv", kapela2)
clen2_4 = ClenKapely("Frank", "Delgado", date(1970, 11, 19), "keyboard", kapela2)

kapela3 = Kapela("Kabát", 1983, "CZ", "hard rock, thrash metal", [])
clen3_1 = ClenKapely("Milan", "Špalek", date(1966, 12, 10), "basa", kapela3)
clen3_2 = ClenKapely("Tomáš", "Krulich", date(1966, 4, 19), "kytara", kapela3)
clen3_3 = ClenKapely("Radek", "Hurčík", date(1969, 1, 14), "bubny", kapela3)
clen3_4 = ClenKapely("Josef", "Vojtek", date(1965, 6, 21), "zpěv", kapela3)
clen3_5 = ClenKapely("Ota", "Váňa", date(1971, 6, 11), "kytara", kapela3)

kapela4 = Kapela("The Beatles", 1960, "UK", "rock, pop", [])
clen4_1 = ClenKapely("John", "Lennon", date(1940, 10, 9), "kytara", kapela4)
clen4_2 = ClenKapely("Paul", "McCartney", date(1942, 6, 18), "basa", kapela4)
clen4_3 = ClenKapely("George", "Harrison", date(1943, 2, 25), "kytara", kapela4)
clen4_4 = ClenKapely("Ringo", "Starr", date(1940, 7, 7), "bubny", kapela4)

kapela4_revival = KapelaRevival("The Beatles Revival", 1992, "CZ", "rock, pop", [], kapela4)
clen_revival_1 = ClenKapely("Luděk", "Maulis", date(1940, 10, 9), "kytara", kapela4_revival)
clen_revival_2 = ClenKapely("Zbyněk", "Maulis", date(1942, 6, 18), "basa", kapela4_revival)
clen_revival_3 = ClenKapely("Petr", "Lux", date(1943, 2, 25), "kytara", kapela4_revival)
clen_revival_4 = ClenKapely("Jiří", "Tomišín",  date(1940, 7, 7), "bubny", kapela4_revival)

klub0 = Klub("STARRY", "G2-6-10 Kitazawa, Setagaya 155-0031, Tokyo", 250)
klub1 = Klub("Zepp Haneda", "1-1-4 Hanedakuko, Ota-ku, Tokyo", 2925)
klub2 = Klub("Lucerna Music Bar", "Vodičkova 36, Praha", 800)
klub3 = Klub("ROXY", "Dlouhá 33, Praha", 600)
klub4 = Klub("MeetFactory", "Ke Sklárně 3213/15, Smíchov, Praha", 750)

koncert0 = Koncert("-Fixed Star-", date(2024, 4, 13), time(23, 0), klub0, kapela1, 1250)
koncert1 = Koncert("-Fixed Star-", date(2024, 4, 13), time(23, 0), klub1, kapela1, 1250)
koncert2 = Koncert("Good Things", date(2024, 7, 3), time(18, 45), klub2, kapela2, 2350)
koncert3 = Koncert("Po Čertech", date(2024, 11, 10), time(20, 15), klub3, kapela3, 880)
koncert4 = Koncert("Po Čertech", date(2024, 11, 11), time(19, 0), klub4, kapela3, 800)
koncert5 = Koncert("Po Čertech", date(2024, 11, 12), time(18, 45), klub2, kapela3, 900)
koncert6 = Koncert("The Beatles Revival Tour", date(2024, 2, 28), time(15, 30), klub4, kapela4_revival, 300)

kapely = [kapela1, kapela2, kapela3, kapela4, kapela4_revival]
clenoveKapel = [clen1_1, clen1_2, clen1_3, clen1_4]
clenoveKapel += [clen2_1, clen2_2, clen2_3, clen2_4,]
clenoveKapel += [clen3_1, clen3_2, clen3_3, clen3_4, clen3_5]
clenoveKapel += [clen_revival_1, clen_revival_2, clen_revival_3, clen_revival_4]
kluby = [klub0, klub1, klub2, klub3, klub4]
koncerty = [koncert0, koncert1, koncert2, koncert3, koncert4, koncert5, koncert6]


# Dotazy
# Vypis clenu kapely 1
print(kapela1.vypisCleny())

# Seznam koncertu v Tokiu:
print("\n\n".join(koncert.celeInformace() for koncert in filter(lambda koncert: koncert.mestoFiltr("Tokyo"), koncerty)))

# Seznam koncertu v Praze pozdeji nez 18:45 (ne vcetne)
print("\n\n".join(koncert.celeInformace() for koncert in filter(lambda koncert: koncert.mestoFiltr("Praha") and koncert.casKonani > time(18,45), koncerty)))

# Prijmeni clenu kapely 2 
print([clen.prijmeni for clen in kapela2.clenove])

# Maximalni trzba koncertu Kabatu v klubu Roxy
print(koncert3.maximalniTrzba(), "CZK")

# Maximalni trzba koncertu Kabatu se dvacetiprocetni slevou na vsech listcich 
print(koncert3.maximalniTrzba(20), "CZK")

# Vypis koncertu za vice nez 100CZK a mene nez 900CZK (vcetne rovno)
print("\n\n".join(koncert.celeInformace() for koncert in filter(lambda koncert: koncert.cenovyFiltr(100, 900), koncerty)))

# Kapely, ve kterem nekdo hraje na klavesy:
print([kapela.nazev for kapela in filter(lambda kapela: kapela.nastrojFiltr("keyboard"), kapely)])

# O kolik let je revival kapely 4 novejsi nez original
print(kapela4_revival.rokZalozeni - kapela4_revival.puvodniKapela.rokZalozeni, "let")

# Kolik by musela stat vstupenka aby trzba byla milion korun na koncertu 6 ve vyprodanem klubu
print(ceil(1000000 / koncert6.mistoKonani.kapacita), "CZK")

# Prumerny vek clenu kapely 3
print(kapela3.prumernyVek(), "let")

# Seznam kapel ktere hraji metal a jejich cely zanr string
print("\n".join([f"{kapela.nazev} - {kapela.zanr}" for kapela  in filter(lambda kapela: "metal" in kapela.zanr, kapely)]))


# Pravidla
# Každá kapela má alespoň jednoho clena
print(all(len(kapela.clenove) > 0 for kapela in kapely))

# Kazdy clen kapely se narodil v minulosti (je mu vice nez 0 let)
print(all(date.today() - clen.datumNarozeni > timedelta(days=0) for clen in clenoveKapel))

# Vsechny koncerty se konaji v nejakem klubu a vystupuje tam nejaka kapela
print(all(koncert.mistoKonani is not None and koncert.vystupujiciKapela is not None for koncert in koncerty))