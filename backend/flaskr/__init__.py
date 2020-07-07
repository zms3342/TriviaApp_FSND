import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  db = SQLAlchemy()


  def pagination(request, selected_items):
    page = request.args.get('page',1,type=int)
    start_page = (page-1)*QUESTIONS_PER_PAGE 
    end_page = start_page+QUESTIONS_PER_PAGE

    items = [item.format() for item in selected_items]
    current = items[start_page:end_page]

    return current

  def search(searchterm): 
    searched_items = Question.query.filter(
      Question.question.ilike(f"%{searchterm}%")).all()
    if searched_items is None: 
      abort(404, "No items matching the searchterm")
    return searched_items
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*":{"origins":"*"}})
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def ater_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response  


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    data={}
    for i in categories: 
      data[i.id]=i.type

    if len(data)==0: 
      abort(404, "WHOOPS BRUH.... YOU LOST")

    return jsonify({
            'success': True,
            'categories': data
        })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions(): 
    questions = Question.query.order_by(Question.id).all()
    current_questions = pagination(request, questions)

    categories = Category.query.order_by(Category.type).all()
    cats ={}
    for category in categories: 
      cats[category.id]=category.type

    if len(cats)==0: 
      abort(404, 'Questions aint here loser')

    return jsonify({
      'success':True, 
      'questions': current_questions,
      'total_questons': len(questions),
      'current_category': None, 
      'categories': cats

      })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route("/questions/<question_id>", methods=['DELETE'])
  def delete_question(question_id):
    try: 
      question = Question.query.get(question_id)
      question.delete()
      return jsonify({
      'success':True,
      'deleted':question_id
      })
    except: 
      abort(404)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  @app.route("/questions", methods=['POST'])
  def add_question():
    
    #search question functionality
    if request.get_json().get("searchTerm"):
      searched_items = search(request.get_json().get("searchTerm"))
      paginate_questions = pagination(request, searched_items)

      return jsonify({
                'success': True,
                'questions': paginate_questions,
                'total_questions': len(Question.query.all())
            })


    else:
      question = request.get_json().get("question")
      answer = request.get_json().get("answer")
      difficulty = request.get_json().get("difficulty")
      Category = request.get_json().get("category")
      try: 
        new = Question(question=question, answer=answer, difficulty=difficulty, category=Category)
        new.insert()
        return jsonify({
          'success':True,
          'added' : new.id 
            })
      except: 
        abort(422)




  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:id>/questions')
  def get_questions_by_category(id):
    '''
  Handles GET requests for getting questions based on category.
  '''
    try:
        questions = Question.query.filter(
            Question.category == str(id)).all()

        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'total_questions': len(questions),
            'current_category': id
        })
    except:
        abort(404)
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def get_guesses():
    body = request.get_json()

    if body == None or 'quiz_category' not in body.keys():
      return abort(422)

    previous_questions = []
    if 'previous_questions' in body.keys():
      previous_questions = body['previous_questions']

    question = Question.query.filter(
      Question.category == body['quiz_category']['id'], Question.id.notin_(previous_questions)).first()

    return jsonify({
        "success": True,
        "question": question.format() if question != None else None
    })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400
  return app

    