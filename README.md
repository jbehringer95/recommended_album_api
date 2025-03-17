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
