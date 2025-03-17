# Recommended Album API

A Flask-based REST API that recommends music albums based on genre preferences using machine learning and the Spotify API.

## 🎵 Features

- Genre-based album recommendations
- Integration with Spotify API for album artwork and verification
- AWS DynamoDB backend for album data storage
- Machine learning-powered recommendation engine using TF-IDF vectorization
- RESTful API endpoints for recommendations and genre tags

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Flask-RESTful
- **Machine Learning**: scikit-learn (TF-IDF Vectorizer)
- **Database**: AWS DynamoDB
- **Storage**: AWS S3
- **External API**: Spotify Web API
- **Authentication**: Spotify Client Credentials Flow

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- AWS Account with S3 and DynamoDB access
- Spotify Developer Account

### Environment Variables

Create a `.env` file in the root directory with:
```python
spotify_client_id=your_spotify_client_id
spotify_client_secret=your_spotify_client_secret
access_key=your_aws_access_key
secret_key=your_aws_secret_key
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/jbehringer95/recommended_album_api.git
cd recommended_album_api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## 📡 API Endpoints

### Get Album Recommendations
```http
GET /prediction/<string:value_list>
```
Returns album recommendations based on provided genre tags.

### Get Available Tags
```http
GET /tags
```
Returns all available genre tags.

### Health Check
```http
GET /health
```
Returns API health status.

## Example Usage

### Python
```python
import requests
import urllib.parse

# Base URL
BASE = 'http://recommended-album-api-dev.us-east-1.elasticbeanstalk.com/prediction/'

# Example: Get recommendations for Art Rock genre
value_list = ['Art Rock']
response = requests.get(BASE + urllib.parse.quote(str(value_list)))
print(response.json())
```

### Response
```json
[
    {
        "Album_Name": "In the Court of the Crimson King",
        "Artist": "King Crimson",
        "Genres": "Progressive Rock, Art Rock",
        "url": "https://i.scdn.co/image/ab67616d0000b273e7a385c0ce0f3f827e9f3caa"
    }
]
```

## 🧪 Testing

Run the test suite:
```bash
python test.py
```

## 📚 Project Structure
```
recommended_album_api/
├── main.py              # Main application file
├── predictions.py       # ML recommendation logic
├── aws_connection.py    # AWS connectivity
├── requirements.txt     # Project dependencies
└── test.py             # Test suite
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Justin Behringer** - *Initial work* - [jbehringer95](https://github.com/jbehringer95)

## 🙏 Acknowledgments

- Spotify Web API for providing album data
- AWS for cloud infrastructure
- scikit-learn for ML capabilities
