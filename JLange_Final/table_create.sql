CREATE DATABASE IF NOT EXISTS cpsc408;
USE cpsc408;
CREATE TABLE Athletes(
athleteID INTEGER NOT NULL auto_increment primary key,
Name VARCHAR(70),
NOC VARCHAR(70),
Discipline VARCHAR(70)
);
CREATE TABLE Medals(
medalID INTEGER NOT NULL auto_increment primary key,
Ranking INTEGER NOT NULL,
TeamNOC VARCHAR(70),
Gold INTEGER,
Silver INTEGER,
Bronze INTEGER,
Total INTEGER,
RankByTotal INTEGER
);
CREATE TABLE EntriesGender(
genderID INTEGER NOT NULL auto_increment primary key,
Discipline VARCHAR(70),
Female INTEGER,
Male INTEGER,
Total INTEGER
);

CREATE TABLE Teams(
teamID INTEGER NOT NULL auto_increment primary key,
Name VARCHAR(70),
Discipline VARCHAR(70),
NOC VARCHAR(70),
Event VARCHAR(70)
);

CREATE TABLE Coaches(
coachesID INTEGER NOT NULL auto_increment primary key,
Name VARCHAR(70) NOT NULL,
NOC VARCHAR(70),
Discipline VARCHAR(70),
Event VARCHAR(70)
);
