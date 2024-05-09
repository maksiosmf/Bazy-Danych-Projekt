Widok prezentujący informacje o produktach wraz z kategoriami:
  
create view widok_produktow_kategorii as
select p.id_produktu, p.nazwa as nazwa_produktu, p.cena, k.nazwa as nazwa_kategorii
from produkty p
join kategorie k on p.id_kategorii = k.id_kategorii;


Widok prezentujący szczegóły zamówień wraz z informacjami o kliencie:

create view widok_szczegolow_klientow as
select z.id_zamowienia, k.imie, k.nazwisko, k.email, z.data_zamowienia, z.suma
from zamowienia z
join klienci k on z.id_klienta = k.id_klienta;
