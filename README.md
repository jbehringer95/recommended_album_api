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
- PostgreSQL or SQLite (for local database)
- Spotify Developer Account

### Environment Variables

Create a `.env` file in the root directory with:
```python
spotify_client_id=your_spotify_client_id
spotify_client_secret=your_spotify_client_secret
DATABASE_URL=postgresql://username:password@localhost:5432/albumdb  # For PostgreSQL
# or
DATABASE_URL=sqlite:///albums.db  # For SQLite
```

### Database Setup

1. Create a local database:

For PostgreSQL:
```bash
# Install PostgreSQL and create database
psql
CREATE DATABASE albumdb;
```

For SQLite:
```bash
# SQLite database will be created automatically when running the application
```

2. Initialize the database with sample data:
```python
# db_setup.py
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Create engine
engine = create_engine(os.getenv('DATABASE_URL'))

# Load sample data
df = pd.read_csv('sample_albums.csv')  # You'll need to create this with some sample data
df.to_sql('albums', engine, if_exists='replace', index=False)
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
pip install psycopg2-binary  # For PostgreSQL
# or
pip install sqlite3  # For SQLite
```

3. Set up the database:
```bash
python db_setup.py
```

4. Run the application:
```bash
python main.py
```

## Example Usage

### Python
```python
import requests
import urllib.parse

# Local Base URL
BASE = 'http://127.0.0.1:5000/prediction/'

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

Note: Make sure you have set up your environment variables, database, and are running the Flask application locally before making requests.
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
