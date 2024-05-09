use sklep;

insert into kategorie (id_kategorii, nazwa) values
(1, 'Elektronika'),
(2, 'Gry i zabawki'),
(3, 'Książki'),
(4, 'Odzież');

insert into produkty (id_produktu, nazwa, cena, id_kategorii) values
(1, 'Laptop', 3199.99, 1),
(2, 'Smartfon', 1999.99, 1),
(3, 'Monopoly', 129.99, 2),
(4, 'Harry Potter', 39.99, 3),
(5, 'T-shirt', 49.99, 4);

insert into klienci (id_klienta, imie, nazwisko, email) values
(1, 'Jan', 'Kowalski', 'jan.kowalski@mail.com'),
(2, 'Ann', 'Nowak', 'ann.nowak@mail.com');

insert into zamowienia (id_zamowienia, id_klienta, data_zamowienia, suma) values
(1, 1, '2024-04-01', 3049.98),
(2, 2, '2024-04-02', 49.99);

insert into szczegoly_zamowienia (id_zamowienia, id_produktu, ilosc, cena_jednostkowa) values
(1, 1, 1, 2999.99),
(1, 3, 1, 129.99),
(2, 5, 1, 49.99);

insert into klienci (id_klienta, imie, nazwisko, email) values
(1, 'Peter', 'Parker', 'peter.parker@mail.com');
