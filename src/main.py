from database import Database
from repositories.soldier_repository import SoldierRepository
from models.soldier import Soldier
import sys
from repositories.mission_repository import MissionRepository


def action_assign_mission(soldier_repo, mission_repo):
    print("\n--- ROZKAZ DO AKCE (Přiřazení M:N) ---")
    print("Dostupní vojáci:")
    soldiers = soldier_repo.get_all()
    for s in soldiers:
        print(f"ID {s.soldier_id}: {s.full_name} ({s.rank})")

    try:
        sid = int(input("\nZadej ID vojáka: "))
    except:
        print("Chyba: Musíš zadat číslo.")
        return

    print("\nDostupné mise:")
    missions = mission_repo.get_all()
    if not missions:
        print("Žádné mise nejsou v systému! (Vlož je přes SQL nebo vytvoř funkci)")
        return

    for m in missions:
        print(f"ID {m.mission_id}: {m.operation_name}")

    try:
        mid = int(input("\nZadej ID mise: "))
    except:
        print("Chyba: Musíš zadat číslo.")
        return
    role = input("Role na misi (např. Kulometčík, Řidič): ")

    if mission_repo.assign_soldier(mid, sid, role):
        print(f"\n[ÚSPĚCH] Voják byl přiřazen k misi.")
    else:
        print("\n[CHYBA] Nepodařilo se přiřadit (možná už tam je?).")

    input("\nStiskni Enter...")


def main():
    print("Start aplikace...")

    soldier_repo = SoldierRepository()
    mission_repo = MissionRepository()

    while True:
        print("1. Seznam vojáků")
        print("2. ... (tvoje staré možnosti)")
        print("6. POSLAT VOJÁKA NA MISI (NOVÉ)")
        print("0. Konec")

        choice = input("Volba: ")

        if choice == '1':

        elif choice == '6':
            action_assign_mission(soldier_repo, mission_repo)


if __name__ == "__main__":
    main()