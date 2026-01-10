# MilWare – Military Database System

**MilWare** je konzolová databázová aplikace pro správu vojenských posádek, personálu, vozového parku a operačních misí.

* **Verze:** 1.0
* **Varianta řešení:** D1 (Repository Pattern)
* **Autor:** David Čadek

---

Projekt je rozdělen do následujících adresářů:

* `src/` – Zdrojové kódy aplikace (Python).
* `data/` – JSON soubory pro import dat.
* `sql/` – SQL skripty pro vytvoření databáze a pohledů.
* `doc/` – Technická dokumentace (PDF).
* `test/` – Testovací scénáře pro testery (PDF).

---


Tento návod slouží pro testery a uživatele, kteří chtějí aplikaci spustit v příkazovém řádku (CMD/Terminál) bez nutnosti instalovat vývojové prostředí (jako VS Code nebo PyCharm).

Před spuštěním se ujistěte, že máte nainstalováno:
* **Python 3.8+** (při instalaci zaškrtněte "Add Python to PATH").
* **MySQL Server** (např. přes XAMPP nebo samostatný MySQL Community Server).
* **Git** (volitelné, pro stažení repozitáře).

1. Spusťte MySQL server (např. v XAMPP Control Panel klikněte na *Start* u MySQL).
2. Otevřete nástroj pro správu databáze (MySQL Workbench nebo phpMyAdmin).
3. **Vytvoření struktury:** Spusťte (importujte) skript **`sql/init_db.sql`**.
   * *Tím se vytvoří databáze `milware_db` a prázdné tabulky.*
4. **Vytvoření pohledů:** Spusťte skript **`sql/views_db.sql`**.
   * *Tím se vytvoří SQL Views potřebné pro reporty.*

1. V kořenové složce projektu najděte soubor `config.example.json` (pokud existuje) nebo vytvořte nový soubor **`config.json`**.
2. Otevřete ho v Poznámkovém bloku a nastavte přístupové údaje k vaší databázi:
   ```json
   {
       "host": "localhost",
       "user": "root",
       "password": "", 
       "database": "milware_db"
   }


Tento návod slouží pro spuštění aplikace v příkazovém řádku (CMD/Terminál).

Otevřete příkazový řádek (CMD) ve složce, kam chcete projekt stáhnout, a zadejte:

```bash
git clone [https://github.com/CadekDavid/MilWare.git](https://github.com/CadekDavid/MilWare.git)
cd MilWare
pip install -r requirements.txt
python src/main.py
