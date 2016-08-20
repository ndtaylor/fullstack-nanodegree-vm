#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def doOnDb(action):
    db = connect()
    cursor = db.cursor()
    result = action(cursor)
    db.commit()
    db.close()
    return result


def queryDb(action):
    db = connect()
    cursor = db.cursor()
    result = action(cursor)
    db.close()
    return result


def deleteMatches():
    """Remove all the match records from the database."""
    doOnDb(lambda cursor: cursor.execute("delete from results;"))


def deletePlayers():
    """Remove all the player records from the database."""
    doOnDb(lambda cursor: cursor.execute('delete from players;'))


def countPlayers():
    """Returns the number of players currently registered."""
    def fetch(cursor):
        cursor.execute('select count(*) from players;')
        return cursor.fetchone()[0]

    return int(queryDb(fetch))


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """

    doOnDb(lambda cur: cur.execute('insert into players values (%s);', (bleach.clean(name),)))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    query = """create view wins as select id, count(winner) as count
        from players left join results on id = winner
        group by id;
    create view matches as select id, count(winner) as count
        from players left join results on (id = player1 or id = player2)
        group by id;
    select players.id, players.name, wins.count, matches.count
        from players, wins, matches
        where players.id = wins.id and players.id = matches.id;
    """
    def fetch(cursor):
        cursor.execute(query)
        return cursor.fetchall()
    return queryDb(fetch)


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
