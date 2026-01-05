from database import Database
from repositories.soldier_repository import SoldierRepository
from models.soldier import Soldier
import sys


def main():
    print("Start aplikace...")

    try:
        repo = SoldierRepository()
        print("Připojení k databázi proběhlo úspěšně.")

        print("\n--- 1. Vytváření vojáka ---")
        novacek = Soldier(None, "Rambo", "John Rambo", "Private", 1)
        new_id = repo.create(novacek)
        novacek.soldier_id = new_id
        print(f"Vytvořen nový voják s ID: {new_id}")

        print("\n--- 2. Načtení vojáka ---")
        nacteny = repo.get_by_id(new_id)
        if nacteny:
            print(f"Načteno z DB: {nacteny.full_name} ({nacteny.callsign}) - {nacteny.rank}")

        print("\n--- 3. Úprava vojáka ---")
        if nacteny:
            nacteny.rank = "General"
            nacteny.callsign = "Snake"
            repo.update(nacteny)
            print("Voják byl upraven (povýšen).")

            kontrola = repo.get_by_id(new_id)
            print(f"Kontrola po změně: {kontrola.full_name} - {kontrola.rank}")

        print("\n--- 4. Mazání vojáka ---")
        repo.delete(new_id)
        print("Voják byl smazán.")

        overeni = repo.get_by_id(new_id)
        if overeni is None:
            print("Potvrzeno: Záznam už v databázi neexistuje.")

    except Exception as e:
        print(f"Kritická chyba: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()