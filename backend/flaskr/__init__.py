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

    #Pagination function.
    def pagination(request, selected_items):
        '''
        input: request, items(questions)
        output: paginated objext
        '''
        page = request.args.get('page',1,type=int)
        start_page = (page-1)*QUESTIONS_PER_PAGE 
        end_page = start_page+QUESTIONS_PER_PAGE

        items = [item.format() for item in selected_items]
        current = items[start_page:end_page]

        return current

    #Search Function    
    def search(searchterm):
        '''
        input: string search term
        output: queried questions that match search string
        '''

        searched_items = Question.query.filter(
            Question.question.ilike("%{}%".format(searchterm))).all()
        if searched_items is None: 
            abort(404, "No items matching the searchterm")
        return searched_items

    #flask cors initialization
    cors = CORS(app, resources={r"/api/*":{"origins":"*"}})


    @app.after_request
    def ater_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response  

    #GET categories. Return a list of categories
    @app.route('/categories')
    def get_categories():
        '''
        input:None
        output: json object with category list
        '''

        categories = Category.query.all()
        data={}
        for i in categories: 
            data[i.id]=i.type

        if len(data)==0: 
            abort(404, "No Categories Found :(")

        return jsonify({
            'success': True,
            'categories': data
            })

    #GET request for questions
    @app.route('/questions')
    def get_questions():
        '''
        input: None
        output: json object with list of questions and categories
        ''' 
        questions = Question.query.order_by(Question.id).all()
        current_questions = pagination(request, questions)
        categories = Category.query.order_by(Category.type).all()
        cats ={}

        for category in categories: 
            cats[category.id]=category.type

        if len(current_questions)==0: 
            abort(404, 'No Questions Found :(')

        return jsonify({
            'success':True, 
            'questions': current_questions,
            'total_questons': len(questions),
            'current_category': None, 
            'categories': cats
            })

    #DELETE question functionality 
    @app.route("/questions/<question_id>", methods=['DELETE'])
    def delete_question(question_id):
        '''
        input: None
        output: json object with the id of the deleted question
        ''' 
        try: 
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                'success':True,
                'deleted':question_id
                })
        except: 
            abort(404)

    #Post Question and Search
    @app.route("/questions", methods=['POST'])
    def add_question():
        '''
        input: None
        output: Json object with Search results if there is a search term, or a new question
        '''
        #search question functionality
        if request.get_json().get("searchTerm"):
            searched_items = search(request.get_json().get("searchTerm"))
            paginate_questions = pagination(request, searched_items)

            return jsonify({
                'success': True,
                'questions': paginate_questions,
                'total_questions': len(Question.query.all())
                })

        #Add question
        else:
            question = request.get_json().get("question")
            answer = request.get_json().get("answer")
            difficulty = request.get_json().get("difficulty")
            Category = request.get_json().get("category")
            if question==None or answer==None or difficulty==None or Category==None: 
                abort(422)
            try: 
                new = Question(question=question, answer=answer, difficulty=difficulty, category=Category)
                new.insert()
                return jsonify({
                    'success':True,
                    'added' : new.id
                    })
            except: 
                abort(422)

    #Returns questions by category
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        '''
        input:category id 
        output: json object with questions that have the given category id
        '''

        try:
            questions = Question.query.filter(Question.category == str(id)).all()

            return jsonify({
                'success': True,
                'questions': [question.format() for question in questions],
                'total_questions': len(questions),
                'current_category': id
                })
        except:
            abort(400)

    #Functionality for quizzes
    @app.route('/quizzes', methods=['POST'])
    def get_guesses():
        '''
        input: none
        output: json object with next question in the quiz
        '''

        body = request.get_json()

        if body == None or 'quiz_category' not in body.keys():
            return abort(422)

        previous_questions = []
        if 'previous_questions' in body.keys():
            previous_questions = body['previous_questions']

        if body['quiz_category']['id'] ==0: 
            question =Question.query.filter(Question.id.notin_(previous_questions)).first()
        else:
            question = Question.query.filter(Question.category == body['quiz_category']['id'], Question.id.notin_(previous_questions)).first()

        return jsonify({
            "success": True,
            "question": question.format() if question != None else None
            })

    #Error Handlers Created
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

