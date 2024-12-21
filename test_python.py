import datetime
import platform
import getpass

def main():
    # Hallo Welt Ausgabe
    print("Hallo Welt!")
    
    # Aktuelle Uhrzeit und Datum ausgeben
    aktuelle_zeit = datetime.datetime.now()
    print(f"Aktuelle Uhrzeit: {aktuelle_zeit.strftime('%H:%M:%S')}")
    print(f"Aktuelles Datum: {aktuelle_zeit.strftime('%d.%m.%Y')}")
    
    # Zusätzliche Systeminformationen
    print(f"\nBenutzer: {getpass.getuser()}")
    print(f"Betriebssystem: {platform.system()} {platform.release()}")
    print(f"Computer-Typ: {platform.machine()}")

if __name__ == "__main__":
    main()