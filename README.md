# Movie Database API 

A basic movie database interacting with external API using Django, DRF and PostgreSQL.
PostgreSQL was chosen, because of it's ability to store JSON objects.

**Heroku link**: https://afternoon-mesa-86810.herokuapp.com/movies/

## Available endpoints: ##

* **POST** ```json {"title": "Movie Name"}```  */movies/* - add movie to DB 

* **GET** */movies/* - fetch all movies existing in DB

* **GET** */movies/{movie_id}/* - fetch movie with specified ID

* **GET** */movies/?ordering={field_to_order}* - sorting movies by specified field

* **GET** */movies/?year={year}&country={country}&imdb_rating={imdb_rating}* - filter movies by specified fields

* **GET** */movies/?year={year}&ordering={field_to_order}* - filter movies by specified year and sorting by specified field

* **POST** ```json {"movie_id": "Movie ID", "text": "Comment text"}```  */comments/* - add comment for movie

* **GET** */comments/* - fetch all comments existing in DB

* **GET** */comments/?movie_id={movie_id}* -fetch all comments connected with specified movie_id

## Installing: ##

1. **git clone https://github.com/dmitrikuksik/movies-api.git**

2. **docker-compose build**

3. **docker-compose run db -d**

4. **docker-compose run --rm web python3 manage.py migrate**

5. **docker-compose run --rm web python3 manage.py test**

6. **docker-compose up**

Now server is listening on host 0.0.0.0 and port 8000.
