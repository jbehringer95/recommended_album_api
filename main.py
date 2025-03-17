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
import logging
from functools import wraps
import traceback
from typing import Optional, List, Dict, Any


load_dotenv()

SPOTIFY_ID = os.getenv('spotify_client_id')
SPOTIFY_SECRET = os.getenv('spotify_client_secret')

ACCESS_KEY = os.getenv('access_key')
SECRET_KEY = os.getenv('secret_key')

app = Flask(__name__)
api = Api(app)
CORS(app)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Custom exceptions
class SpotifyAPIError(Exception):
    pass

class DatabaseError(Exception):
    pass

# Decorator for endpoint error handling
def handle_endpoint_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Endpoint error: {str(e)}\n{traceback.format_exc()}")
            return {"error": "Internal server error"}, 500
    return wrapper

class AlbumSuggester(Resource):
    @handle_endpoint_errors
    def get(self, value_list: str) -> List[Dict[str, Any]]:
        logger.info(f"Received request for genres: {value_list}")
        
        try:
            sp = self._get_spotify_client()
        except Exception as e:
            logger.error(f"Failed to initialize Spotify client: {e}")
            raise SpotifyAPIError("Failed to connect to Spotify")
        
        try:
            processed_values = self._process_input_values(value_list)
            logger.debug(f"Processed values: {processed_values}")
        except Exception as e:
            logger.error(f"Failed to process input values: {e}")
            return {"error": "Invalid input format"}, 400
        
        try:
            df = pulling_dataframe(ACCESS_KEY, SECRET_KEY, 'Vectorizor_df.csv')
            recommendations = get_recommendations(df, 'Album', 'New_Album', processed_values)
            logger.info(f"Generated {len(recommendations)} recommendations")
        except Exception as e:
            logger.error(f"Failed to get recommendations: {e}")
            raise DatabaseError("Failed to fetch recommendations")
        
        return self._get_album_details(sp, recommendations)

    def _get_spotify_client(self):
        if not all([SPOTIFY_ID, SPOTIFY_SECRET]):
            logger.error("Missing Spotify credentials")
            raise ValueError("Spotify credentials not configured")
            
        try:
            client_credentials_manager = SpotifyClientCredentials(
                client_id=SPOTIFY_ID, 
                client_secret=SPOTIFY_SECRET
            )
            return spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        except Exception as e:
            logger.error(f"Spotify client initialization failed: {e}")
            raise SpotifyAPIError("Failed to initialize Spotify client")

    def _process_input_values(self, value_list):
        decoded_list = urllib.parse.unquote(value_list)
        values = decoded_list.split(', ')
        return [re.sub('[^a-zA-Z\s]', '', i) for i in values]

    def _get_album_details(self, sp, recommendations) -> List[Dict[str, Any]]:
        album = []
        album_names = []
        errors = 0
        max_errors = 3  # Maximum number of consecutive errors before giving up

        for num in range(1, 100):
            if len(album) >= 5:
                break

            if errors >= max_errors:
                logger.warning("Too many consecutive errors, stopping album fetch")
                break

            try:
                response = query_album(int(recommendations['index'].iloc[num]), ACCESS_KEY, SECRET_KEY)
                errors = 0  # Reset error counter on success
            except Exception as e:
                logger.error(f"Failed to query album {num}: {e}")
                errors += 1
                continue

            for values in response:
                if values['Album_Name'] in album_names:
                    continue

                try:
                    album_data = self._fetch_album_data(sp, values.copy())
                    if album_data:
                        album.append(album_data)
                        album_names.append(values['Album_Name'])
                        logger.info(f"Added album: {values['Album_Name']}")
                        break
                except Exception as e:
                    logger.error(f"Failed to fetch album data for {values.get('Album_Name', 'unknown')}: {e}")
                    continue

        if not album:
            logger.warning("No albums were successfully retrieved")
            return {"error": "No matching albums found"}, 404

        return album

    def _fetch_album_data(self, sp, values: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            del values['Index']
            search_query = f"{values['Album_Name']} artist:{values['Artist']}"
            logger.debug(f"Searching Spotify with query: {search_query}")
            
            album_results = sp.search(search_query, type='album', limit=50)
            
            for album_result in album_results['albums']['items']:
                if (values['Artist'].lower() == album_result['artists'][0]['name'].lower() and
                    values['Album_Name'].lower() == album_result['name'].lower()):
                    values['url'] = album_result['images'][0]['url']
                    return values
                    
            logger.debug(f"No exact match found for {values['Album_Name']}")
            return None
            
        except Exception as e:
            logger.error(f"Spotify API error for {values.get('Album_Name', 'unknown')}: {e}")
            return None

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