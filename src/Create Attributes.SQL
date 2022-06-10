drop table if exists Attributes;
CREATE TABLE Attributes(id char(4),
type char(20),
gender char(20),
skin_tone char(30),
count int,
accessories char(10000),
CONSTRAINT nft_pk PRIMARY KEY (id));

copy  Attributes(id,type,gender, skin_tone, count, accessories)
            from 'ABSOLUTE_PATH_OF_CSV_FILE\attributes.csv'
            delimiter ','
            CSV HEADER;