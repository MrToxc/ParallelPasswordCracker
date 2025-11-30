# Paralelní Password Cracker (Producer–Consumer)

**Autor:** Václav Křivka  
**Datum:** 24. 11. 2025  
**Předmět:** Programové vybavení

---

## Stručný popis
Jednoduchý studentský projekt demonstrující paralelní brute-force útok proti **SHA-384** hashi pomocí více procesů (`multiprocessing`). Ukazuje rozdělení práce, synchronizaci přes `Queue` a sdílení výsledku přes `multiprocessing.Value` a `multiprocessing.Array`.

> **Poznámka:** Projekt je výukový — nevyužívej k nelegálnímým účelům.

---

## Požadavky
- Python 3.x  
- Standardní knihovny: `multiprocessing`, `hashlib`, `string`, `time`, `sys`  
- Žádné externí balíčky

---

## Co program dělá
1. Vytvoří množinu znaků podle konfigurace (malá/velká písmena, čísla, speciální znaky).  
2. Generuje kombinace všech hesel od délky 1 do `max_chars`.  
3. Rozdělí práci mezi N workerů — každý worker dostane svůj rozsah indexů (start/end).  
4. Workery hashují každé generované heslo (`SHA-384`) a porovnávají s cílovým hashem.  
5. Při nalezení hesla worker uloží výsledek do sdílené paměti a nastaví `finish_flag`; ostatní workery se ukončí po „poison pill“ (`None`).

---

## Struktura řešení
- `PasswordCracker` — hlavní třída obsahující logiku pro generování, dělení práce a spuštění workerů.  
- `process_manager` — producent; generuje úkoly `(symbols_count, start, end)` a vkládá je do `multiprocessing.Queue`.  
- `worker_crack_password` — konzument; bere úkoly z fronty, generuje hesla, hashuje a porovnává.  
- Sdílený stav:
  - `finish_flag = multiprocessing.Value('i', 0)` — 0 = běží, 1 = nalezeno.  
  - `final_password = multiprocessing.Array('c', 100)` — buffer pro nalezené heslo (padding nulami).

---

## Jak spustit
1. Otevři terminál ve složce se skriptem `cracker.py`.  
2. Spusť (výchozí hodnoty použity, pokud argumenty vynecháš):

```bash
# výchozí: max délka 5, 2 procesy, testovací hash
python cracker.py

# explicitně: <max_chars> <max_processes> <sha384_hash>
python cracker.py 6 4 9e0133f2a13... (96 hex znaků)
