# Paralelní Password Cracker (Producer-Consumer)

**Autor:** Václav Křivka  
**Datum:** 24. 11. 2025  
**Předmět:** Programové vybavení

## Popis projektu
Tato aplikace demonstruje řešení reálného problému (brute-force útok na hesla) s využitím **paralelního zpracování**. Problém je řešen pomocí návrhového vzoru **Producer-Consumer** (Producent-Konzument), který zajišťuje efektivní využití více jader procesoru a zabraňuje situacím typu *starvation* (hladovění procesů).

Aplikace se pokouší prolomit SHA-384 hash zadaného hesla generováním kombinací znaků.

## Architektura a paralelizace
Řešení je rozděleno na dvě hlavní části komunikující přes `multiprocessing.Queue`:

1.  **Process Manager (Producent):**
    * Generuje rozsahy indexů (úkoly) pro danou délku hesla.
    * Vkládá úkoly do sdílené fronty.
    * Řídí životní cyklus workerů a zajišťuje synchronizaci.
    * Na konci vkládá do fronty "Poison Pill" (`None`) pro korektní ukončení.

2.  **Workers (Konzumenti):**
    * Nezávislé procesy, které si odebírají práci z fronty.
    * Provádí výpočetně náročné generování hesel a hashování.
    * Při nalezení hesla uloží výsledek do sdílené paměti a signalizují ukončení ostatním procesům pomocí `finish_flag`.

## Požadavky
* Python 3.x
* Standardní knihovny: `multiprocessing`, `hashlib`, `string`, `time`
* Program nevyžaduje instalaci žádných externích balíčků.

## Návod ke spuštění
Program je navržen tak, aby byl spustitelný z příkazové řádky bez nutnosti IDE.

1.  Otevřete terminál (CMD/PowerShell/Bash) ve složce se skriptem.
2.  Spusťte příkaz:
    ```bash
    python cracker.py
    ```

## Konfigurace
Z důvodu optimalizace výkonu a jednoduchosti nasazení je konfigurace umístěna přímo v bloku `__main__` ve zdrojovém kódu. Pro změnu parametrů otevřete skript v libovolném textovém editoru a upravte sekci na konci souboru:

* **`password_hash`**: Cílový SHA-384 hash, který chcete prolomit.
* **`args=(6, 4, queue)`**:
    * První číslo (`6`): Maximální délka generovaného hesla.
    * Druhé číslo (`4`): Počet paralelních procesů (doporučeno nastavit dle počtu jader CPU).
* **Třída `PasswordCracker`**: Zde lze zapnout/vypnout sady znaků (`contains_lowercase`, `contains_numbers` atd.).

## Ukázka běhu
Program vypíše do konzole průběh startování workerů a po nalezení hesla (nebo vyčerpání možností) zobrazí výsledek a celkový čas výpočtu.
