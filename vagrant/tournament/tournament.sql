-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table players (name text, id serial primary key);
create table results (
    player1 int references players (id),
    player2 int references players (id),
    winner int references players (id),
    primary key (player1, player2),
    check (player1 < player2 and (winner = player1 or winner = player2))
);
