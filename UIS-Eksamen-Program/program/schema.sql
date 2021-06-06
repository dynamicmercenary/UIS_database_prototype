\i schema_drop.sql

CREATE TABLE IF NOT EXISTS Coordinator(
	id integer PRIMARY KEY,
    name varchar(20),
    password varchar(120)
);

CREATE TABLE IF NOT EXISTS Volunteer(
    id integer PRIMARY KEY,
    name varchar(20),
    password varchar(120) default '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO',
    CONSTRAINT butiks_ID FOREIGN KEY (id) REFERENCES Butik (bID),
    CONSTRAINT butiks_navn FOREIGN KEY (name) REFERENCES Butik (navn)
);

CREATE TABLE IF NOT EXISTS Butik(
    bID integer PRIMARY KEY,
    har_program boolean default False, 
    navn varchar(100),
    region varchar(100),
    Modtaget integer default 0, 
    telefon varchar(10),
    email varchar(100)
);

CREATE TABLE IF NOT EXISTS harProgram(
    pID integer PRIMARY KEY,
    Ugedag varchar(10),
    scala integer default 0,
    CONSTRAINT butiks_ID FOREIGN KEY (pID) REFERENCES Butik (bID),
    first_shift integer default 0
);
