DELETE FROM harProgram;
DELETE FROM Butik;

INSERT INTO public.coordinator(ID, name, password) VALUES (6000, 'Anna', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO');
INSERT INTO public.volunteer(ID, name, password) VALUES (9,'Hvidovre', '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO');

INSERT INTO public.butik(bID, navn, region, modtaget, telefon, email) VALUES (0001, 'Butik1', 'Region1', 0, '12345678', 'butik1@dca.dk');
INSERT INTO public.butik(bID, navn, region, modtaget, telefon, email) VALUES (0002, 'Butik2', 'Region2', 0, '23456789', 'butik2@dca.dk');
INSERT INTO public.butik(bID, navn, region, modtaget, telefon, email) VALUES (0003, 'Butik3', 'Region1', 0, '34567890', 'butik3@dca.dk');
INSERT INTO public.butik(bID, navn, region, modtaget, telefon, email) VALUES (0004, 'Butik4', 'Region4', 0, '45678910', 'butik4@dca.dk');
INSERT INTO public.butik(bID, navn, region, modtaget, telefon, email) VALUES (0005, 'Butik5', 'Region5', 0, '56789101', 'butik5@dca.dk');
INSERT INTO public.butik(bID, navn, region, modtaget, telefon, email) VALUES (0006, 'Butik6', 'Region6', 0, '67891011', 'butik6@dca.dk');
INSERT INTO public.butik(bID, navn, region, modtaget, telefon, email) VALUES (0007, 'Butik7', 'Region7', 0, '78910111', 'butik7@dca.dk');
