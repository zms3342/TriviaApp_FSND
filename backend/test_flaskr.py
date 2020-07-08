import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:password@localhost:5432/trivia_test"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_question_pagination(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        #ensure that our response is good with a 200 status code
        self.assertEqual(response.status_code,200)
        #ensure that success is True in response
        self.assertEqual(data['success'],True)

    def test_categories(self): 
        response=self.client().get('/categories')
        data = json.loads(response.data)

        #ensure that our response is good with a 200 status code
        self.assertEqual(response.status_code,200)
        #ensure that success is True in response
        self.assertEqual(data['success'],True)


    def test_delete_question(self): 
        #create a question that will be deleted
        question = Question(
            question="hello",
            answer="its me",
            category=1,
            difficulty=1)
        #adds question to DB
        question.insert()
        #get its id so we can delete it 
        question_id = question.id

        response = self.client().delete(f'/questions/{question_id}')
        data = json.loads(response.data)

        self.assertEqual(data['deleted'], str(question_id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'],True) 


    def test_search(self): 
        response = self.client().post('questions', json = {'searchTerm':'k'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True )
        self.assertIsNotNone(data['questions'])

    def test_add_question(self): 
        question_json = {
        "question":"sample",
        "answer": "sample answer",
        "difficulty": "1",
        "category":"1"
        }
        total_questions = len(Question.query.all())

        response = self.client().post('questions', json=question_json)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True )
        self.assertIsNotNone(data['added'])


    def test_quesitions_by_cat(self): 
        response = self.client().get('/categories/1/questions')
        data = json.loads(response.data)


        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['current_category'],1)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])


    def test_quiz(self):
        quiz_json = {'previous_questions': [],
                          'quiz_category': {'type':'Science', 'id': 1}
                          }

        response = self.client().post('/quizzes', json=quiz_json)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['question'])

















if __name__ == "__main__":
    unittest.main()