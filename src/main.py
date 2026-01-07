from database import Database
from repositories.soldier_repository import SoldierRepository
from models.soldier import Soldier
import sys
from repositories.mission_repository import MissionRepository
import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    print("=" * 50)
    print("      MILWARE - MILITARY DATABASE SYSTEM      ")
    print("=" * 50)


def pause():
    input("\nStiskni Enter pro pokračování...")


def action_list_soldiers(repo):
    clear_screen()
    print_header()
    print("--- SEZNAM PERSONÁLU ---\n")
    soldiers = repo.get_all()

    if not soldiers:
        print("Databáze je prázdná.")
    else:
        print(f"{'ID':<5} {'Callsign':<15} {'Hodnost':<15} {'Jméno'}")
        print("-" * 60)
        for s in soldiers:
            print(f"{s.soldier_id:<5} {s.callsign:<15} {s.rank:<15} {s.full_name}")
    pause()


def action_find_soldier(repo):
    print("\n--- HLEDÁNÍ VOJÁKA ---")
    try:
        sid = int(input("Zadej ID vojáka: "))
        soldier = repo.get_by_id(sid)
        if soldier:
            print(f"\n[NALEZEN]: {soldier}")
            print(f"ID: {soldier.soldier_id}")
            print(f"Jméno: {soldier.full_name}")
            print(f"Hodnost: {soldier.rank}")
            print(f"Základna ID: {soldier.base_id}")
        else:
            print(f"\n[CHYBA] Voják s ID {sid} neexistuje.")
    except ValueError:
        print("\n[CHYBA] ID musí být číslo!")
    pause()


def action_add_soldier(repo):
    print("\n--- REKRUTACE (NOVÝ ZÁZNAM) ---")
    try:
        fullname = input("Jméno a příjmení: ")
        if not fullname: raise ValueError("Jméno nesmí být prázdné.")

        callsign = input("Volací znak (Callsign): ")

        print("Dostupné hodnosti: Private, Corporal, Sergeant, Lieutenant, General")
        rank = input("Hodnost: ")

        # Pro zjednodušení dáváme base_id natvrdo nebo uživatel musí vědět číslo
        # V pokročilé verzi bys tady vypsal seznam základen
        try:
            base_id = int(input("ID Základny (např. 1): "))
        except ValueError:
            print("Zadáno neplatné číslo základny, nastavuji defaultní (1).")
            base_id = 1

        new_soldier = Soldier(None, callsign, fullname, rank, base_id)
        new_id = repo.create(new_soldier)
        print(f"\n[ÚSPĚCH] Voják byl uložen do systému. Přidělené ID: {new_id}")

    except Exception as e:
        print(f"\n[CHYBA] Nepodařilo se uložit: {e}")
    pause()


def action_update_soldier(repo):
    print("\n--- ÚPRAVA ZÁZNAMU (POVÝŠENÍ) ---")
    try:
        sid = int(input("Zadej ID vojáka pro úpravu: "))
        soldier = repo.get_by_id(sid)

        if not soldier:
            print("Voják neexistuje.")
            pause()
            return

        print(f"Upravujete: {soldier}")
        print("(Nechte políčko prázdné, pokud ho nechcete měnit)")

        new_name = input(f"Nové jméno [{soldier.full_name}]: ")
        if new_name: soldier.full_name = new_name

        new_call = input(f"Nový callsign [{soldier.callsign}]: ")
        if new_call: soldier.callsign = new_call

        new_rank = input(f"Nová hodnost [{soldier.rank}]: ")
        if new_rank: soldier.rank = new_rank

        repo.update(soldier)
        print("\n[ÚSPĚCH] Záznam aktualizován.")

    except ValueError:
        print("\n[CHYBA] ID musí být číslo.")
    except Exception as e:
        print(f"\n[CHYBA] Aktualizace selhala: {e}")
    pause()


def action_delete_soldier(repo):
    print("\n--- PROPUŠTĚNÍ (SMAZÁNÍ) ---")
    try:
        sid = int(input("Zadej ID vojáka ke smazání: "))
        confirm = input(f"Opravdu smazat ID {sid}? Napiš 'ano': ")

        if confirm.lower() == 'ano':
            if repo.delete(sid):
                print("\n[ÚSPĚCH] Záznam smazán.")
            else:
                print("\n[CHYBA] Záznam nebyl nalezen nebo nejde smazat.")
        else:
            print("Akce zrušena.")
    except ValueError:
        print("\n[CHYBA] ID musí být číslo.")
    pause()


# --- AKCE S MISEMI (VAZBA M:N) ---

def action_assign_mission(soldier_repo, mission_repo):
    clear_screen()
    print_header()
    print("--- ROZKAZ DO AKCE (Přiřazení na Misi) ---\n")

    # 1. Výpis vojáků pro výběr
    print("Dostupní vojáci:")
    soldiers = soldier_repo.get_all()
    for s in soldiers:
        print(f"ID {s.soldier_id}: {s.full_name} ({s.rank})")

    try:
        sid = int(input("\n>>> Vyber ID vojáka: "))
        # Rychlá kontrola, jestli voják existuje
        if not soldier_repo.get_by_id(sid):
            print("Chyba: Voják s tímto ID neexistuje.")
            pause()
            return
    except ValueError:
        print("Chyba: Musíš zadat číslo.")
        pause()
        return

    # 2. Výpis misí pro výběr
    print("\nDostupné mise:")
    missions = mission_repo.get_all()
    if not missions:
        print("!!! V databázi nejsou žádné mise. Vlož je nejdřív přes SQL.")
        pause()
        return

    for m in missions:
        print(f"ID {m.mission_id}: {m.operation_name} ({m.start_time})")

    try:
        mid = int(input("\n>>> Vyber ID mise: "))
    except ValueError:
        print("Chyba: Musíš zadat číslo.")
        pause()
        return

    # 3. Určení role
    role = input("Zadej roli na misi (např. Kulometčík, Řidič, Velitel): ")
    if not role: role = "Voják"  # Defaultní role

    # 4. Zápis do M:N tabulky
    print(f"\nPřiřazuji vojáka {sid} na misi {mid} jako '{role}'...")
    if mission_repo.assign_soldier(mid, sid, role):
        print(f"[ÚSPĚCH] Rozkaz potvrzen. Voják je na seznamu mise.")
    else:
        print("\n[CHYBA] Nepodařilo se přiřadit. (Možná už na té misi je?)")

    pause()


# --- HLAVNÍ MENU ---

def main():
    try:
        # Inicializace repozitářů (připojení k DB)
        soldier_repo = SoldierRepository()
        mission_repo = MissionRepository()
    except Exception as e:
        print(f"Kritická chyba při startu: {e}")
        print("Zkontroluj config.json a jestli běží MySQL/XAMPP.")
        input("Stiskni Enter pro ukončení...")
        sys.exit(1)

    while True:
        clear_screen()
        print_header()
        print("HLAVNÍ NABÍDKA:")
        print("1. Seznam všech vojáků")
        print("2. Najít vojáka podle ID")
        print("3. Rekrutovat nového vojáka (CREATE)")
        print("4. Povýšit/Upravit vojáka (UPDATE)")
        print("5. Propustit vojáka (DELETE)")
        print("-" * 40)
        print("6. POSLAT VOJÁKA NA MISI (M:N Vazba)")
        print("-" * 40)
        print("0. Konec aplikace")
        print("=" * 50)

        choice = input("Vaše volba: ")

        if choice == '1':
            action_list_soldiers(soldier_repo)
        elif choice == '2':
            action_find_soldier(soldier_repo)
        elif choice == '3':
            action_add_soldier(soldier_repo)
        elif choice == '4':
            action_update_soldier(soldier_repo)
        elif choice == '5':
            action_delete_soldier(soldier_repo)
        elif choice == '6':
            action_assign_mission(soldier_repo, mission_repo)
        elif choice == '0':
            print("\nUkončuji MilWare. Rozchod!")
            sys.exit(0)
        else:
            print("\nNeplatná volba.")
            pause()


if __name__ == "__main__":
    main()