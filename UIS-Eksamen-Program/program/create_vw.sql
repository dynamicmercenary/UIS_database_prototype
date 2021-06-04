CREATE OR REPLACE VIEW Ugedage
AS 
SELECT pID, Ugedag
FROM harProgram;

CREATE OR REPLACE VIEW Scala
AS
SELECT pID, Scala
FROM harProgram
ORDER BY Scala DESC;

CREATE OR REPLACE VIEW ButikkeriRegion
AS
SELECT bID, navn
FROM Butik;

CREATE OR REPLACE VIEW ContactInfo
AS
SELECT bID, navn, email, telefon, region
FROM butik;