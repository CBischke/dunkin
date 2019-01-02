from flask import Flask
from flask import request
from flask_restplus import Api, Resource, fields
from ranking.ranking_manager import Ranking_Manager
from model.database import Database

import json

app = Flask(__name__)
api = Api(app, version='1.0', title='Tutor API',
    description='API for uploading to the tutor',
)

parser = api.parser()
parser.add_argument('learning-material', type=str, help='Learning topic for the tutor to teach', location='form', required=True)
parser.add_argument('file-of-origin', type=str, help='name of the file for the content', location='headers', required=True)

ranking_mng = Ranking_Manager()


@api.route('/tutor/idea/')
@api.doc(parser=parser)
class Response(Resource):
    def post(self):
        learning_material = str(request.form['learning-material'])
        file_of_origin = str(request.headers['file-of-origin']).replace(" ", "_")
        topic = ranking_mng.run_inference_on_material(learning_material, file_of_origin)
        return topic.toJson()
    def delete(self):
        learning_material = str(request.form['learning-material'])
        if learning_material == "Boy that Italian family over there sure is quiet":
            db = Database()
            db.delete_collection()
            return "dropped"
        return "not dropped"


if __name__ == '__main__':
    app.run(port=8080, threaded=True, debug=False, host='0.0.0.0')