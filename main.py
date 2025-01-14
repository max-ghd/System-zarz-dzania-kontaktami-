import pandas as pd
#Importujemy bibliotekę pandas, która pozwala nam nad działaniami danyh w tabelach i plikach CSV
import re
#importujemy moduł re(regular expressions) do sprawdzania poprawności danych, takich jak numery telefonów czy adresy email

def validate_phone(phone):#Funkcja do sprawdzania poprawności formatu numeru telefonu od 7 do 15 cyfr oraz może zawierać '+' na początku
    return re.fullmatch(r"\+?[0-9\s\-]{7,15}", phone) is not None

def validate_email(email):#ta funkcja sprawdza poprawność formatu adresu email kontakta i sprawdza, czy email zawiera znak '@' oraz domenę po kropce
    return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) is not None

def append_contact(data):#Funkcja do dodawania nowego kontaktu i pobiera dane od użytkownika i dodaje je do pliku CSV
    inp = input("Napisz imię i nazwisko kontaktów: ").split(",")#Użytkownik wprowadza imię i nazwisko
    csv_file = pd.read_csv("note.csv")#Odczytanie istniejącego pliku csv z kontaktami

    data["Imię i Nazwisko"] = inp #Przypisanie imienia i nazwiska do danych
    phones = input("Napisz numer telefonu: ").split(",")#Pobranie numerów telefonów i ich weryfikacja
    valid_phones = []
    for phone in phones:
        while not validate_phone(phone):
            phone = input(f"Nieprawidłowy numer '{phone}'. Napisz poprawny numer: ")
        valid_phones.append(phone)
    data["Telefon"] = valid_phones
    
    emails = input("Napisz mail skrzyńki elektronicznej: ").split(",") #Pobranie adresów email i ich weryfikacja
    valid_emails = []
    for email in emails:
        while not validate_email(email):
            email = input(f"Nieprawidłowy mail '{email}'. Napisz poprawny mail: ")
        valid_emails.append(email)
    data["Email"] = valid_emails

    df = pd.concat([csv_file, pd.DataFrame(data)], ignore_index=True)#Dodanie nowych danych do pliku CSV
    df.to_csv("note.csv", index=None)

    print("\nAktualne kontakty:")#Wyświetlenie aktualnej listy kontaktów
    print(df)

data = {"Imię i Nazwisko": [], "Telefon": [], "Email": []}#Tworzymy pustą listę z kolumnami "Imię i Nazwisko", "Telefon", "Email"

try:#Sprawdzamy, czy plik istnieje, jeśli nie , tworzymy nowy z pustą listę danych
    pd.read_csv("note.csv")
except FileNotFoundError:
    pd.DataFrame(data).to_csv("note.csv", index=None)
append_contact(data)#Dodajemy pierwszy kontakt w program

while True:#Główny cykl programu, gzie użytkownik wybiera jedną z opcji za numerem, czyli dodawanie kontaktu, usunięcie, zmiana, wyswietlienie 
    what = input("\n1 - Dodać nowy kontakt\n2 - Zmienić kontakt\n3 - Usunąć kontakt\n4 - Pokazać wszystkie kontakty\n5 - Stop\nWybierz opcje: ")
    if what == "1":
        append_contact(data)#Dodanie nowego kontaktu za numerem 1
    elif what == "2":
        csv_file = pd.read_csv("note.csv")
        print(csv_file)#Wyświetlenie kontaktów i zmiana wybranego za numerem 2
        idx = int(input("Napisz indeks kontaktu dla zmienienia: "))#Użytkownik podaje indeks kontaktu, który chce zmienić
        column = input("Co zmienić? (Imię i Nazwisko/Telefon/Email): ")#Użytkownik wybiera, co chce zmienić, czyli imię i nazwisko, telefon lub email
        new_value = input("Napisz nowe znaczenie: ")

        if column == "Telefon":#Sprawdzanie poprawności danych przy zmianie numeru telefonu lub emaila
            while not validate_phone(new_value):
                new_value = input("Nieprawidłowy numer. Napisz poprawnie: ")
        elif column == "Email":
            while not validate_email(new_value):
                new_value = input("Nieprawidłowy email. Napisz poprawnie email: ")

        csv_file.at[idx, column] = new_value#Aktualizacja po funkcjach w pliku
        csv_file.to_csv("note.csv", index=None)
        print("\nKontakt został zmieniony:")#Wyświetlenie zaktualizowanej listy kontaktów
        print(csv_file)

    elif what == "3":#Usunięcie wybranego kontaktu za numerem 3
        csv_file = pd.read_csv("note.csv")
        print(csv_file)

        idx = int(input("Napisz index kontaktu dla usunięcia: "))#Użytkownik podaje indeks kontaktu do usunięcia
        csv_file = csv_file.drop(index=idx)
        csv_file.reset_index(drop=True, inplace=True)
        csv_file.to_csv("note.csv", index=None)

        print("\nKontakt usunięty:")#wyświetlenie zaktualizowanej listy kontaktów
        print(csv_file)

    elif what == "4":#Wyświetlenie wszystkich kontaktów w pliku za numerem 4
        csv_file = pd.read_csv("note.csv")
        print("\nWszytkie kontakty:")
        print(csv_file)

    elif what == "5":#Zakończenie działania programu za numerem 5
        print("Program został zakończony.")
        break

    else:#Jeżeli błędne wejście od użytkownika to wyświetli błąd
        print("Nieprawidłowe dane wejściowe. Spróbuj ponownie.")
