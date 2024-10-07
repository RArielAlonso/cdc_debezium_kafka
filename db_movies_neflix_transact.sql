CREATE DATABASE db_movies_neflix_transact;

USE db_movies_neflix_transact;

CREATE TABLE genre (
    genreid INT AUTO_INCREMENT,
    name VARCHAR(100),
    PRIMARY KEY (genreid)
);

CREATE TABLE movie (
    movieid VARCHAR(100),
    movietitle VARCHAR(100),
    releasedate DATE,
    originallanguage VARCHAR(100),
    link VARCHAR(255),
    PRIMARY KEY (movieid)
);

CREATE TABLE movie_genre (
    movieid VARCHAR(100),
    genreid INT,
    PRIMARY KEY (movieid, genreid),
    FOREIGN KEY (movieid) REFERENCES movie(movieid),
    FOREIGN KEY (genreid) REFERENCES genre(genreid)
);

CREATE TABLE person (
    personid VARCHAR(8),
    name VARCHAR(100),
    birthdate DATE,
    PRIMARY KEY (personid)
);

CREATE TABLE participant (
    movieid VARCHAR(100),
    personid VARCHAR(8),
    participantrole VARCHAR(30),
    PRIMARY KEY (movieid, personid),
    FOREIGN KEY (movieid) REFERENCES movie(movieid),
    FOREIGN KEY (personid) REFERENCES person(personid)
);