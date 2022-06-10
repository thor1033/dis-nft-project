drop table if exists favorites;
create table favorites(id char(4), username char(20), constraint nuser primary key(id, username))