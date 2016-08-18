#
# Database access functions for the web forum.
#

import time
import psycopg2
import bleach


## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''

    db = psycopg2.connect("dbname=forum")
    cursor = db.cursor()
    cursor.execute("select content, time from posts order by time desc")
    rows = cursor.fetchall()
    posts = map(lambda (content, time): {'content': str(bleach.clean(content)), 'time': str(time)}, rows)
    db.close()
    return posts


## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''

    db = psycopg2.connect("dbname=forum")
    cursor = db.cursor()
    cursor.execute("insert into posts values (%s)", (bleach.clean(content),))
    db.commit()
    db.close()
