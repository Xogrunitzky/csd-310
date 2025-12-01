
import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values

# ----------------------------------------------------------------------
# LOAD .env SECRETS
# ----------------------------------------------------------------------
secrets = dotenv_values(".env")

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

# ----------------------------------------------------------------------
# SHOW FILMS FUNCTION
# ----------------------------------------------------------------------
def show_films(cursor, title):
    cursor.execute("""
                   SELECT film.film_name AS Name,
                          film.film_director AS Director,
                          genre.genre_name AS Genre,
                          studio.studio_name AS 'Studio Name'
                   FROM film
                            INNER JOIN genre ON film.genre_id = genre.genre_id
                            INNER JOIN studio ON film.studio_id = studio.studio_id;
                   """)

    films = cursor.fetchall()

    print("\n-- {} --".format(title))

    for film in films:
        print("Film Name: {}".format(film[0]))
        print("Director: {}".format(film[1]))
        print("Genre: {}".format(film[2]))
        print("Studio: {}\n".format(film[3]))


# ----------------------------------------------------------------------
# MAIN PROGRAM
# ----------------------------------------------------------------------
try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    print("\nConnected to database '{}' on host '{}' as user '{}'"
          .format(config["database"], config["host"], config["user"]))

    # ----------------------------------------------------------
    # 1. DISPLAY ORIGINAL FILMS
    # ----------------------------------------------------------
    show_films(cursor, "DISPLAYING ORIGINAL FILMS")

    # ----------------------------------------------------------
    # 2. INSERT NEW FILM RECORD (Back to the Future)
    # ----------------------------------------------------------
    print("\n-- INSERTING NEW FILM: Back to the Future --")

    insert_query = """
                   INSERT INTO film (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
                   VALUES (
                              'Back to the Future',
                              '1985',
                              '116',
                              'Robert Zemeckis',
                              (SELECT studio_id FROM studio WHERE studio_name = 'Universal Pictures'),
                              (SELECT genre_id FROM genre WHERE genre_name = 'SciFi')
                          ); \
                   """

    cursor.execute(insert_query)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # ----------------------------------------------------------
    # 3. UPDATE ALIEN TO HORROR
    # ----------------------------------------------------------
    print("\n-- UPDATING 'Alien' TO HORROR --")

    update_query = """
                   UPDATE film
                   SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror')
                   WHERE film_name = 'Alien'; \
                   """

    cursor.execute(update_query)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE")

    # ----------------------------------------------------------
    # 4. DELETE GLADIATOR
    # ----------------------------------------------------------
    print("\n-- DELETING 'Gladiator' --")

    delete_query = """
                   DELETE FROM film
                   WHERE film_name = 'Gladiator'; \
                   """

    cursor.execute(delete_query)
    db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

# ----------------------------------------------------------------------
# ERROR HANDLING
# ----------------------------------------------------------------------
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Invalid username or password.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist.")
    else:
        print(err)

# ----------------------------------------------------------------------
# CLOSE CONNECTION
# ----------------------------------------------------------------------
finally:
    try:
        db.close()
        print("\nDatabase connection closed.")
    except:
        pass
