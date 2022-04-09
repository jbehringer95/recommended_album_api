import os
import re
import json
import urllib.parse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
from predictions import get_recommendations
from aws_connection import pulling_dataframe, query_album

from dotenv import load_dotenv


load_dotenv()

SPOTIFY_ID = os.getenv('spotify_client_id')
SPOTIFY_SECRET = os.getenv('spotify_client_secret')

ACCESS_KEY = os.getenv('access_key')
SECRET_KEY = os.getenv('secret_key')

app = Flask(__name__)
api = Api(app)
CORS(app)


class AlbumSuggester(Resource):
    def get(self, value_list):
        client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_ID, client_secret=SPOTIFY_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        value_list = urllib.parse.unquote(value_list)
        value_list = value_list.split(', ')
        value_list = [re.sub('[^a-zA-Z\s]', '', i) for i in value_list]
        df = pulling_dataframe(ACCESS_KEY, SECRET_KEY, 'Vectorizor_df.csv')
        recommendations = get_recommendations(df, 'Album', 'New_Album', value_list)

        album = []
        album_names = []

        for num in range(1,10):
            # Pulling the album data from the database one at a time
            response = query_album(int(recommendations['index'].iloc[num]), ACCESS_KEY, SECRET_KEY)

            for values in response:

                if values['Album_Name'] not in album_names:
                    album_names.append(values['Album_Name'])
                    del values['Index']
                    album_result = sp.search(values['Album_Name'], type='album', limit=1)
                    values['url'] = album_result['albums']['items'][0]['images'][0]['url']
                    album.append(values)
            
            if len(album) == 5:
                break

        return album

class GetAllTags(Resource):
    def get(self):
        df = pulling_dataframe(ACCESS_KEY, SECRET_KEY, 'columns.csv')
        tags = list(df.columns)
        
        return tags

class Health(Resource):
    def get(self):
        return


api.add_resource(AlbumSuggester, "/prediction/<string:value_list>")
api.add_resource(GetAllTags, '/tags')
api.add_resource(Health, '/health')


if __name__ == "__main__":
    app.run(debug=True)