import os
import mysql.connector

# # Read the password from the environment variable
# password = os.getenv('MYSQL_ROOT_PASSWORD')

# This function creates a connection to the database and creates 
# the reviewer table and the rating table
def start_func():
  # Create a connection
  cnx = mysql.connector.connect(
      user='root',
      # here we need to change 'password' to mysql password
      password=os.getenv('MYSQL_ROOT_PASSWORD', 'password'),
      host='127.0.0.1',
      database='sakila'
  )

  # Create a cursor
  my_cursor = cnx.cursor(buffered=True)

  # Creates rating table
  my_cursor.execute('''
      CREATE TABLE if not exists rating (
        film_id SMALLINT PRIMARY KEY,
        reviewer_id INT NOT NULL,
        rating DECIMAL(2,1) NOT NULL
      )
  ''')

  cnx.commit()

  # Creates reviewer table
  my_cursor.execute('''
      CREATE TABLE if not exists reviewer (
        reviewer_id int PRIMARY KEY, 
        first_name VARCHAR(45), 
        last_name VARCHAR(45)
      );
  ''')

  cnx.commit()


# This function ask for reviewer ID, in order to check if the ID exists in the database 
def asking_for_reviewer_id():
  # asking for reviwer ID
  ID_of_reviewer = input('Hello, ID please\n')

  # Check if the ID exists
  my_cursor.execute("SELECT reviewer_id FROM reviewer WHERE reviewer_id=%s", [ID_of_reviewer,])
  result = my_cursor.fetchone()

  # if ID doesn't exists, add the reviewer to the database
  if result is None:
    first_name_reviewer = input('Hello, first name please\n')
    last_name_reviewer = input('Hello, last name please\n')
    # add ID, first name and last name to reviewer table
    sql = "INSERT INTO reviewer (reviewer_id, first_name, last_name) VALUES (%s, %s, %s)"
    val = (ID_of_reviewer, first_name_reviewer, last_name_reviewer)
    my_cursor.execute(sql, val)
    cnx.commit()


# This function greetings the reviewer
def hello_to_reviewer():
  my_cursor.execute("SELECT first_name FROM reviewer WHERE reviewer_id=%s", [ID_of_reviewer,])
  first_name_reviewer = my_cursor.fetchone()
  my_cursor.execute("SELECT last_name FROM reviewer WHERE reviewer_id=%s", [ID_of_reviewer,])
  last_name_reviewer = my_cursor.fetchone()
  print("Hello, " + ''.join(first_name_reviewer) + " " + ''.join(last_name_reviewer) )


# This function let the reviewer to choose a film
def choose_a_film():
  name_of_film = input('Please insert a name of film\n')
  # Check if the film exists in database
  my_cursor.execute("SELECT title FROM film WHERE title=%s", [name_of_film,])
  result = my_cursor.fetchall()

  # if the reviewer inserted a wrong film name, then needs to choose again
  if len(result) == 0:
    print("There is no film with this name. Please choose again")
    choose_a_film()

  # if there is a single film with this title, we continue and let the reviewer to rate
  elif len(result) == 1:
    add_a_rating()

  # if there are multiple films with this name, we let the reviewer to choose
  # between the films, bases by their ID and release year
  # invalid input from the list, will make him choose a film again 
  elif len(result) > 1:
    print("There is more than one film with this title. Have a look:")
    my_cursor.execute("SELECT film_id, release_year FROM film WHERE title=%s", [name_of_film,])
    result = my_cursor.fetchall()

    # present to the reviewer all the matching films with the same title
    # based by film ID and release year
    movie_ids = []
    for item in result:
      print("film_id " + str(item[0]) + ", release_year " + str(item[1]))
      movie_ids.append(str(item[0]))
    
    selected_movie_id=input("Please Choose one of the films above, by entering its ID\n")
    if selected_movie_id not in movie_ids:
      print("This film ID is invalid. Choose a film again")
      choose_a_film()
    
    else:
      add_a_rating()

# This function let the reviewer to rate the film
def add_a_rating():
  print("Here we add a rating")
  # need to make


def main():
  # Connects to database and creates tables
  start_func()

  # Ask for reviewer ID, in order to check if the ID exists in the database
  asking_for_reviewer_id()

  # Greeting the reviewer
  hello_to_reviewer()

  # Asking the reviewer to insert a film name
  choose_a_film()

  # Asking the reviewer for a rating
  add_a_rating()

  # Close the connection
  cnx.close()

if __name__ == '__main__':
  main()
