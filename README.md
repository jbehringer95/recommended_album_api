Recommended Album API
A Flask-based REST API that recommends music albums based on genre preferences using machine learning and the Spotify API.
🎵 Features
Genre-based album recommendations
Integration with Spotify API for album artwork and verification
AWS DynamoDB backend for album data storage
Machine learning-powered recommendation engine using TF-IDF vectorization
RESTful API endpoints for recommendations and genre tags
🛠️ Tech Stack
Backend: Python, Flask, Flask-RESTful
Machine Learning: scikit-learn (TF-IDF Vectorizer)
Database: AWS DynamoDB
Storage: AWS S3
External API: Spotify Web API
Authentication: Spotify Client Credentials Flow
🚀 Getting Started
Prerequisites
Python 3.8+
AWS Account with S3 and DynamoDB access
Spotify Developer Account
Environment Variables
Create a .env file in the root directory with:
Installation
1. Clone the repository:
2. Install dependencies:
Run the application:
📡 API Endpoints
Get Album Recommendations
Returns album recommendations based on provided genre tags.
Get Available Tags
Returns all available genre tags.
Health Check
Returns API health status.
🧪 Testing
Run the test suite:
📚 Project Structure
🤝 Contributing
Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request
📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
👥 Authors
Justin Behringer - Initial work - jbehringer95
🙏 Acknowledgments
Spotify Web API for providing album data
AWS for cloud infrastructure
scikit-learn for ML capabilities
