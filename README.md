A basic movie database interacting with external API using Django, DRF and PostgreSQL.
PostgreSQL was chosen, because of it's ability to store JSON objects.

**Heroku link**: https://afternoon-mesa-86810.herokuapp.com/

**Available endpoints:**

POST JSON {"title":"Movie Name"}  /movies/ - add movie to DB 

GET /movies/ - fetch all movies existing in DB
GET /movies/{movie_id}/ - fetch movie with specified ID
GET /movies/?order_by={field_to_order} - sorting movies in DB by specified field. 

Available fields: movie_id, data__{field_from_external_api_response} (ex. data__title)

GET /movies/?year={year} - filter movies by specified year

GET /movies/?year={year}&order_by={field_to_order} - filter movies by specified year and sorting by specified field 

POST JSON {"movie_id":"Movie ID", "text":"Comment text"}  /comments/ - add comment for movie
GET /comments/ - fetch all comments existing in DB
GET /comments/{movie_id}/ -fetch all comments connected with specified movie_id

**Installing:**

1. git clone https://github.com/dmitrikuksik/movies-api.git

2. docker-compose build

3. docker-compose run db -d

5. Wait a bit untill db will be available on port.

4. docker-compose run --rm web python3 manage.py migrate

5. docker-compose run --rm web python3 manage.py test

6. docker-compose up

Now server is listening on host 0.0.0.0 and port 8000.
