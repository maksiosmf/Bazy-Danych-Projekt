use sklep


create table kategorie (
    id_kategorii int primary key,
    nazwa varchar(255)
);

create table produkty (
    id_produktu int primary key,
    nazwa varchar(255),
    cena decimal(10, 2),
    id_kategorii int,
    foreign key (id_kategorii) references kategorie(id_kategorii)
);

create table klienci (
    id_klienta int primary key,
    imie varchar(255),
    nazwisko varchar(255),
    email varchar(255)
);

create table zamowienia (
    id_zamowienia int primary key,
    id_klienta int,
    data_zamowienia date,
    suma decimal(10, 2),
    foreign key (id_klienta) references klienci(id_klienta)
);

create table szczegoly_zamowienia (
    id_zamowienia int,
    id_produktu int,
    ilosc int,
    cena_jednostkowa decimal(10, 2),
    primary key (id_zamowienia, id_produktu),
    foreign key (id_zamowienia) references zamowienia(id_zamowienia),
    foreign key (id_produktu) references produkty(id_produktu)
);
