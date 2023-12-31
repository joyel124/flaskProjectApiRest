from flask import Flask
from flask_restful import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage
from predict_resnet50 import predict
import tempfile

app = Flask(__name__)
app.logger.setLevel('INFO')

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('file',
                    type=FileStorage,
                    location='files',
                    required=True,
                    help='provide a file')

class Image(Resource):

    def post(self):
        args = parser.parse_args()
        the_file = args['file']
        # save a temporary copy of the file
        ofile, ofname = tempfile.mkstemp()
        the_file.save(ofname)
        # predict
        results = predict(ofname)[0]
        # formatting the results as a JSON-serializable structure:
        output = {'top_categories': []}
        for _, categ, score in results:
            output['top_categories'].append((categ, float(score)))

        return output


api.add_resource(Image, '/image')

if __name__ == '__main__':
    app.run(debug=True)