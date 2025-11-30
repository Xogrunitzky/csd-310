import mysql.connector
from mysql.connector import errorcode
import dotenv  # to use .env
from dotenv import dotenv_values

# Load secrets from .env file
secrets = dotenv_values(".env")

# Database config
config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True
}

try:
    # Connect to database
    db = mysql.connector.connect(**config)

    print("\n Database user {} connected to MySQL on host {} with database {}"
          .format(config["user"], config["host"], config["database"]))

    input("\n\n Press any key to continue...")

    cursor = db.cursor()

    # ---------------- QUERY 1 ----------------
    print("\n-- DISPLAYING Studio RECORDS --")
    cursor.execute("SELECT * FROM studio;")
    studios = cursor.fetchall()

    for studio in studios:
        print("Studio ID: {}".format(studio[0]))
        print("Studio Name: {}\n".format(studio[1]))

    # ---------------- QUERY 2 ----------------
    print("\n-- DISPLAYING Genre RECORDS --")
    cursor.execute("SELECT * FROM genre;")
    genres = cursor.fetchall()

    for genre in genres:
        print("Genre ID: {}".format(genre[0]))
        print("Genre Name: {}\n".format(genre[1]))

    # ---------------- QUERY 3 ----------------
    print("\n-- DISPLAYING Short Film Names --")
    short_query = """
                  SELECT film_name, film_runtime
                  FROM film
                  WHERE film_runtime < 120; \
                  """
    cursor.execute(short_query)
    short_films = cursor.fetchall()

    for film in short_films:
        print("Film Name: {}".format(film[0]))
        print("Runtime: {} minutes\n".format(film[1]))

    # ---------------- QUERY 4 ----------------
    print("\n-- DISPLAYING Director Grouped Film Records --")
    director_query = """
                     SELECT film_director, film_name
                     FROM film
                     ORDER BY film_director; \
                     """
    cursor.execute(director_query)
    directors = cursor.fetchall()

    for record in directors:
        print("Director: {}".format(record[0]))
        print("Film Name: {}\n".format(record[1]))

except mysql.connector.Error as err:
    # Error Handling
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" The specified database does not exist")
    else:
        print(err)

finally:
    # Close DB connection
    db.close()

