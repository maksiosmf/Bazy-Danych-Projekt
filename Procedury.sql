Procedura do dodawania nowej kategorii:

CREATE PROCEDURE stworzKategorie
@nazwa VARCHAR(255)
AS
BEGIN
    INSERT INTO kategorie (nazwa) VALUES (@nazwa);
END;

Procedura do usuwania produktu:

CREATE PROCEDURE usunProdukt
@produkt_id INT
AS
BEGIN
    DELETE FROM produkty WHERE id_produktu = @produkt_id;
END;

