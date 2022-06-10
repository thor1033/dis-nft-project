drop table if exists users;
CREATE TABLE users( username char(20) NOT NULL,
    password char(20) NOT NULL,
    CONSTRAINT user_pk PRIMARY KEY (username))