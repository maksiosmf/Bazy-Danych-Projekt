Opis biznesowy zagadnienia:


Tabela kategorie - Przechowuje informacje o różnych kategoriach produktów dostępnych w sklepie. Każda kategoria ma unikalny identyfikator (id_kategorii) i nazwę (nazwa). Ta tabela pozwala na organizację produktów w sklepie według kategorii, co ułatwia zarządzanie asortymentem i nawigację po sklepie.
Tabela produkty - Zawiera informacje o produktach oferowanych w sklepie. Każdy produkt ma unikalny identyfikator (id_produktu), nazwę (nazwa), cenę (cena) oraz identyfikator kategorii (id_kategorii), który łączy go z odpowiednią kategorią w tabeli kategorie. Tabela ta jest kluczowa dla działalności sklepu, ponieważ pozwala zarządzać oferowanymi produktami.
Tabela klienci - Przechowuje dane o klientach sklepu, takie jak unikalny identyfikator klienta (id_klienta), imię (imie), nazwisko (nazwisko) i email (email). Tabela ta umożliwia personalizację obsługi klienta oraz efektywne zarządzanie informacjami o klientach, co jest kluczowe dla marketingu i komunikacji.
Tabela zamowienia - Zapisuje informacje o zamówieniach złożonych przez klientów. Zawiera identyfikator zamówienia (id_zamowienia), identyfikator klienta (id_klienta), datę zamówienia (data_zamowienia) oraz sumę zamówienia (suma). Ta tabela jest podstawą dla obsługi zamówień, monitorowania sprzedaży oraz analizy danych sprzedażowych.
Tabela szczegoly_zamowienia - Przechowuje szczegóły każdego zamówienia, w tym identyfikatory zamówienia i produktu (id_zamowienia, id_produktu), ilość zamówionego produktu (ilosc) i cenę jednostkową (cena_jednostkowa). Jest to kluczowa tabela do zarządzania zawartością poszczególnych zamówień, co pozwala na precyzyjne śledzenie sprzedaży produktów i ich dostępności.

Diagram ERD Bazy:


![image](https://github.com/maksiosmf/Bazy-Danych-Projekt/assets/136759557/e70acc36-a325-445b-aa09-153fbd180185)

Opis funkcjonalności biznesowych realizowanych:


Zarządzanie kategoriami produktów:
Umożliwia dodawanie, edytowanie i usuwanie kategorii produktów.
Ułatwia grupowanie produktów.

Zarządzanie produktami:
Dodawanie nowych produktów do oferty sklepu, w tym opisy, ceny oraz przypisywanie do odpowiednich kategorii.
Aktualizacja danych o produktach, takich jak cena.
Usuwanie produktów z oferty.

Zarządzanie klientami:
Rejestrowanie nowych klientów oraz zarządzanie ich danymi, takimi jak imiona, nazwiska i adresy e-mail.

Zarządzanie zamówieniami:
Przyjmowanie i przetwarzanie zamówień składanych przez klientów.

Integracja z systemami płatności i logistyki:
Integracja z zewnętrznymi systemami płatniczymi umożliwiająca bezpieczne przeprowadzanie transakcji.
Współpraca z systemami logistycznymi.
