cd ..
# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. `done`
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT


Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

## GET '/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

- Request Arguments: None

- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

-ex. curl <uri>/categories
	`{
		"categories":{
			'1' : "Science",
			'2' : "Art",
			'3' : "Geography",l
			'4' : "History",
			'5' : "Entertainment",
			'6' : "Sports"}
		}
	}`

## GET '/questions'

- fetches a dictionary containing questions, categories, the category currently being filtered by, and the total number of questions. 

- Questions are returned as a list of dictionaries with the answer, category, difficulty , id , and of course the question itself. 

-ex: curl <uri>/questions

	{
	  "categories": {
	    "1": "jokes", 
	    "2": "Science", 
	    "3": "Math", 
	    "4": "CS"
	  }, 
	  "current_category": null, 
	  "questions": [
	    {
	      "answer": "To get to the other side.", 
	      "category": "1", 
	      "difficulty": 1, 
	      "id": 4, 
	      "question": "why did the chicken cross the road?"
	    },
	    .
	    .
	    .]
	   	"success": true, 
  		"total_questons": 22
	}

## DELETE '/questions/<question_id>'

- Deletes question by id, and returns the id of the delted question

- ex: curl -X DELETE <url>/questions/<question_id>

	`{
  "deleted": "4", 
  "success": true
	}`


## POST '/questions'

- This end point serves 2 purposes. 
	1.) It adds questions, and returns the id of the added question and a success response. 

	2.) If you give this endpoint a string to search for, it will return the questions that match the search term.

- Case 1 ex: curl -X POST <url>/questions -H "Content-Type: application/json" -d '{"question": "A nanny that flies to work with an umbrella", "answer": "who is marry poppins?", "difficulty":"3", "category":"1"}'

	`{
  "added": 26, 
  "success": true
	}`

- Case 2 ex: curl -X POST <url>/questions -H "Content-Type: application/json" -d '{"searchTerm":"2"}'

	`{
	  "questions": [
	    {
	      "answer": "4", 
	      "category": "3", 
	      "difficulty": 1, 
	      "id": 5, 
	      "question": "2+2 =?"
	    }, 
	    {
	      "answer": "5", 
	      "category": "3", 
	      "difficulty": 3, 
	      "id": 9, 
	      "question": "2+3 =?"
	    }
	  ], 
	  "success": true, 
	  "total_questions": 21
	}`

##POST '/quizzes'
- Returns a random quiz question given a category parameter

- If a question has been randomly given it will not come up again. Previous Questions are kept track of. 

- ex: curl -X POST <url>/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [5,6], "quiz_category":{"type":"Math", "id":"2"}}'

	`{
	  "question": {
	    "answer": "H2", 
	    "category": "2", 
	    "difficulty": 3, 
	    "id": 7, 
	    "question": "what H+H"
	  }, 
	  "success": true
	}`


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```