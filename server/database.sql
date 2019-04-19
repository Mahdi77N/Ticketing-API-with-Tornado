-- auto-generated definition
create table chats
(
    id       int auto_increment
        primary key,
    username text not null,
    body     text not null
);

-- auto-generated definition
create table ticket
(
    id       int auto_increment
        primary key,
    username text not null,
    subject  text not null,
    body     text not null,
    status   text not null
);

-- auto-generated definition
create table users
(
    id        int auto_increment
        primary key,
    username  text not null,
    password  text not null,
    token     text null,
    rule      text not null,
    firstname text null,
    lastname  text null
);

