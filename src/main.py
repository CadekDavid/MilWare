from database import Database
from repositories.soldier_repository import SoldierRepository
from models.soldier import Soldier
import sys
from repositories.mission_repository import MissionRepository
import os
from repositories.base_repository import BaseRepository
import json
from repositories.view_repository import ViewRepository
from repositories.vehicle_repository import VehicleRepository

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    print("=" * 50)
    print("      MILWARE - MILITARY DATABASE SYSTEM      ")
    print("=" * 50)


def pause():
    input("\nStiskni Enter pro pokračování...")


def action_generate_report(base_repo):
    clear_screen()
    print_header()
    print("--- GENERÁLNÍ REPORT: STAV ZÁKLADEN (Agregace) ---\n")

    stats = base_repo.get_base_statistics()

    print(f"{'Základna':<20} {'Lokace':<20} {'Vojáci':<10} {'Vozidla'}")
    print("-" * 60)

    for stat in stats:
        print(f"{stat['name']:<20} {stat['location']:<20} {stat['soldiers']:<10} {stat['vehicles']}")

    print("\n" + "-" * 60)
    print("Report vygenerován úspěšně.")
    pause()



def action_list_tables(soldier_repo, base_repo, mission_repo, vehicle_repo):
    clear_screen()
    print_header()
    print("--- PROHLÍŽEČ DATABÁZE ---\n")
    print("Kterou tabulku chceš vypsat?")
    print("1. Vojáci (Soldiers)")
    print("2. Základny (Bases)")
    print("3. Vozidla (Vehicles)")
    print("4. Mise (Missions)")
    print("5. Rozkazy (MissionAssignments - M:N vazba)")
    volba = input("\n>>> Tvoje volba (1-5): ")
    print("\n" + "-" * 60)

    if volba == '1':
        print(f"{'ID':<5} {'Callsign':<15} {'Hodnost':<15} {'Jméno'}")
        print("-" * 60)
        for s in soldier_repo.get_all():
            print(f"{s.soldier_id:<5} {s.callsign:<15} {s.rank:<15} {s.full_name}")

    elif volba == '2':
        print(f"{'ID':<5} {'Název':<20} {'Lokace':<20} {'Kapacita'}")
        print("-" * 60)
        for b in base_repo.get_all():
            print(f"{b[0]:<5} {b[1]:<20} {b[2]:<20} {b[3]}")

    elif volba == '3':
        print(f"{'ID':<5} {'Model':<20} {'Spotřeba':<10} {'Bojeschopné'}")
        print("-" * 60)
        for v in vehicle_repo.get_all():
            ready = "ANO" if v[3] == 1 else "NE"
            print(f"{v[0]:<5} {v[1]:<20} {v[2]:<10} {ready}")

    elif volba == '4':
        print(f"{'ID':<5} {'Operace':<30} {'Začátek'}")
        print("-" * 60)
        for m in mission_repo.get_all():
            print(f"{m.mission_id:<5} {m.operation_name:<30} {m.start_time}")

    elif volba == '5':
        print(f"{'Operace':<30} {'Voják':<20} {'Role'}")
        print("-" * 60)
        for row in mission_repo.get_all_assignments():
            print(f"{row[0]:<30} {row[1]:<20} {row[2]}")

    else:
        print("Neplatná volba.")
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


def action_show_views(view_repo):
    clear_screen()
    print_header()
    print("--- SQL VIEWS (POHLEDY) ---\n")

    print("[1] View_Soldier_Details (Vojáci + Názvy základen)")
    print("[2] View_Mission_Status (Obsazenost misí)")

    volba = input("\nKterý pohled chceš načíst? (1/2): ")

    if volba == '1':
        print(f"\n{'ID':<5} {'Callsign':<15} {'Hodnost':<15} {'Základna (Lokace)'}")
        print("-" * 70)
        data = view_repo.get_soldier_details()
        for row in data:
            print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]} ({row[4]})")

    elif volba == '2':
        print(f"\n{'Operace':<30} {'Začátek':<20} {'Počet vojáků'}")
        print("-" * 70)
        data = view_repo.get_mission_status()
        for row in data:
            print(f"{row[0]:<30} {str(row[1]):<20} {row[2]}")

    else:
        print("Neplatná volba.")

    pause()



def action_import_soldiers(soldier_repo, vehicle_repo):
    clear_screen()
    print_header()
    print("--- IMPORT DAT ---")
    print("1. Importovat VOJÁKY (soldiers.json)")
    print("2. Importovat VOZIDLA (vehicles.json)")
    choice = input("\nCo chceš nahrát? (1-3): ")

    filename = ""
    mode = ""

    base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

    if choice == '1':
        filename = "new_recruits.json"
        mode = "soldiers"
    elif choice == '2':
        filename = "new_vehicles.json"
        mode = "vehicles"
    else:
        print("Neplatná volba.")
        pause()
        return

    file_path = os.path.join(base_path, filename)
    print(f"\nHledám soubor: {file_path}")

    if not os.path.exists(file_path):
        print(f"Chyba: Soubor {filename} neexistuje!")
        pause()
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"Soubor načten. Zahajuji import ({mode})...")

        count = 0
        if mode == "soldiers":
            count = soldier_repo.bulk_import_json(data)
            print(f"[ÚSPĚCH] Nahráno {count} vojáků.")

        elif mode == "vehicles":
            count = vehicle_repo.import_from_json(data)
            print(f"[ÚSPĚCH] Nahráno {count} vozidel.")

    except Exception as e:
        print(f"\n[CHYBA] Import selhal: {e}")
        print("Byl proveden Rollback (nic se neuložilo).")

    pause()



def action_assign_mission(soldier_repo, mission_repo):
    clear_screen()
    print_header()
    print("--- ROZKAZ DO AKCE (Přiřazení na Misi) ---\n")

    print("Dostupní vojáci:")
    soldiers = soldier_repo.get_all()
    for s in soldiers:
        print(f"ID {s.soldier_id}: {s.full_name} ({s.rank})")

    try:
        sid = int(input("\n>>> Vyber ID vojáka: "))

        if not soldier_repo.get_by_id(sid):
            print("Chyba: Voják s tímto ID neexistuje.")
            pause()
            return
    except ValueError:
        print("Chyba: Musíš zadat číslo.")
        pause()
        return


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


    role = input("Zadej roli na misi (např. Kulometčík, Řidič, Velitel): ")
    if not role: role = "Voják"


    print(f"\nPřiřazuji vojáka {sid} na misi {mid} jako '{role}'...")
    if mission_repo.assign_soldier(mid, sid, role):
        print(f"[ÚSPĚCH] Rozkaz potvrzen. Voják je na seznamu mise.")
    else:
        print("\n[CHYBA] Nepodařilo se přiřadit. (Možná už na té misi je?)")

    pause()

def main():
    try:
        soldier_repo = SoldierRepository()
        mission_repo = MissionRepository()
        base_repo = BaseRepository()
        view_repo = ViewRepository()
        vehicle_repo = VehicleRepository()
    except Exception as e:
        print(f"Kritická chyba při startu: {e}")
        print("Zkontroluj config.json a jestli běží MySQL/XAMPP.")
        input("Stiskni Enter pro ukončení...")
        sys.exit(1)

    while True:
        clear_screen()
        print_header()
        print("HLAVNÍ NABÍDKA:")
        print("1. Seznamy")
        print("2. Najít vojáka podle ID")
        print("3. Rekrutovat nového vojáka (CREATE)")
        print("4. Povýšit/Upravit vojáka (UPDATE)")
        print("5. Propustit vojáka (DELETE)")
        print("-" * 40)
        print("6. POSLAT VOJÁKA NA MISI (M:N Vazba)")
        print("7. GENERÁLNÍ REPORT (Statistiky)")
        print("8. IMPORT DATA (JSON)")
        print("9. ZOBRAZIT SQL POHLEDY (Views)")
        print("-" * 40)
        print("0. Konec aplikace")
        print("=" * 50)

        choice = input("Vaše volba: ")

        if choice == '1':
            action_list_tables(soldier_repo, base_repo, mission_repo, vehicle_repo)
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
        elif choice == '7':
            action_generate_report(base_repo)
        elif choice == '8':
            action_import_soldiers(soldier_repo, vehicle_repo)
        elif choice == '9':
            action_show_views(view_repo)
        elif choice == '0':
            print("\nUkončuji MilWare. Rozchod!")
            sys.exit(0)
        else:
            print("\nNeplatná volba.")
            pause()


if __name__ == "__main__":
    main()