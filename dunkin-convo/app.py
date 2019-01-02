from flask import Flask
from flask import request
from flask_restplus import Api, Resource, fields
from database import Database

import json

app = Flask(__name__)
api = Api(app, version='1.0', title='Conversation API',
    description='API for interating with the tutor',
)

parser = api.parser()
parser.add_argument('student-response', type=str, help='Response from the student', location='headers', required=False)
parser.add_argument('file-of-origin', type=str, help='the learning objective for the current question', location='headers', required=True)
parser.add_argument('current-idea-index', type=int, help='the current level (or topic) the student is on based on the learning objective', location='headers', required=False)
parser.add_argument('current-question-index', type=int, help='index of which question to ask', location='headers', required=False)
db = Database()

@api.route('/convo/question/')
@api.doc(parser=parser)
class Response(Resource):
    def get(self):
        student_response = str(request.headers['student-response'])
        file_of_origin = str(request.headers['file-of-origin'])
        current_idea_index = int(request.headers['current-idea-index'])
        return db.get_next_idea(current_idea_index, file_of_origin)

@api.route('/convo/question/length')
@api.doc(parser=parser)
class Length(Resource):
    def get(self):
        file_of_origin = str(request.headers['file-of-origin'])
        return db.get_length_ideas(file_of_origin)

@api.route('/convo/topics/')
class Topic(Resource):
    def get(self):
        print("calling topics...")
        return db.find_core_ideas()

@api.route('/convo/question/answer/')
@api.doc(parser=parser)
class compare(Resource):
    def get(self):
        student_response = str(request.headers['student-response'])
        file_of_origin = str(request.headers['file-of-origin'])
        current_idea_index = int(request.headers['current-idea-index'])
        current_question_index = int(request.headers['current-question-index'])
        return db.compare_answer(current_idea_index, file_of_origin, student_response, current_question_index)

if __name__ == '__main__':
    app.run(port=8080, threaded=True, debug=False, host='0.0.0.0')