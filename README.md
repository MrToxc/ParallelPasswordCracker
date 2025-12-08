# Paralelní Password Cracker — stručně pro uživatele

**Autor:** Václav Křivka  
**Datum:** 12. 7. 2025  
**Předmět:** Programové vybavení

---

## Krátký popis
Program zkusí najít heslo porovnáním SHA-384 hashe pomocí více procesů najednou — určené pro testování vlastních hesel a ověření jejich slabosti.  
Výstup je buď nalezené heslo, nebo informace, že heslo nebylo nalezeno.

**Důležité upozornění**  
Používej pouze na vlastních datech nebo s jasným svolením. Zneužití k prolomení cizích účtů je nezákonné.

---

## Co program používá
- Program může načíst vlastní znaky ze souboru `config.txt` (jeden řetězec všech znaků).  
  Pokud soubor neexistuje, použije se kombinace podle zvolených přednastavených sad znaků.  
- Výchozí nastavení lze přepsat argumenty při spuštění (max. délka, počet procesů, cílový hash, sady znaků).

---

## Struktura příkazu (command)
```bash
python crack.py <max_chars> <max_processes> <sha384_hash> [char_sets...]
```

## Podporované sady znaků (charsety)
Do příkazové řádky můžeš specifikovat tyto předdefinované sady (rozlišuje se velká/malá písmena):

- `letters` — malá písmena `a–z`  
- `LETTERS` — velká písmena `A–Z`  
- `numbers` — číslice `0–9`  
- `special` — speciální znaky (podle `string.punctuation` v Pythonu)

Příklad:  
```bash
python crack.py 6 4 <sha384_hash> letters numbers special
```
