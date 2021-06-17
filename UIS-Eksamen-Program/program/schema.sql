\i schema_drop.sql

CREATE TABLE IF NOT EXISTS Coordinator(
	cID integer PRIMARY KEY,
    name varchar(20),
    password varchar(120)
);

CREATE TABLE IF NOT EXISTS Store(
    sID integer PRIMARY KEY NOT NULL,
    hasProgram boolean default False, 
    name varchar(100),
    region varchar(100),
    received integer default 0, 
    telephone varchar(10),
    email varchar(100)
);

CREATE TABLE IF NOT EXISTS hasProgram(
    pID integer PRIMARY KEY,
    weekDay varchar(10),
    scala integer default 0,
    CONSTRAINT storeID FOREIGN KEY (pID) REFERENCES Store (sID),
    firstShift integer default 0
);

CREATE TABLE IF NOT EXISTS Volunteer(
    vID integer PRIMARY KEY,
    name varchar(20),
    password varchar(120) default '$2b$12$KFkp1IEMGT4QrWwjPGhE3ejOv6Z3pYhx/S4qOoFbanR2sMiZqgeJO',
    CONSTRAINT hasProgram_id FOREIGN KEY (vID) REFERENCES hasProgram (pID)
);
