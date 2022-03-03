import os
import re
import json
import urllib.parse
from flask import Flask
from flask_restful import Api, Resource
from predictions import get_recommendations
from aws_connection import pulling_dataframe, query_album

from dotenv import load_dotenv


load_dotenv()

ACCESS_KEY = os.getenv('access_key')
SECRET_KEY = os.getenv('secret_key')

app = Flask(__name__)
api = Api(app)


class AlbumSuggester(Resource):
    def get(self, value_list):
        value_list = urllib.parse.unquote(value_list)
        value_list = value_list.split(', ')
        value_list = [re.sub('[^a-zA-Z\s]', '', i) for i in value_list]
        df = pulling_dataframe(ACCESS_KEY, SECRET_KEY)
        recommendations = get_recommendations(df, 'Album', 'New_Album', value_list)
        album = []
        for num in range(1,6):
            response = query_album(int(recommendations['index'].iloc[num]), ACCESS_KEY, SECRET_KEY)

            for values in response:
                del values['Index']
                album.append(values)

        return album


api.add_resource(AlbumSuggester, "/prediction/<string:value_list>")

if __name__ == "__main__":
    app.run(debug=True)