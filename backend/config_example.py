# TiDB Serverless Configuration - Example
# Copy this file to config.py and fill in your actual credentials
TIDB_CONFIG = {
    "host": "YOUR_TIDB_HOST",
    "port": 4000,
    "user": "YOUR_USERNAME.root",
    "password": "YOUR_PASSWORD",
    "database": "test",
    "ssl_disabled": False,
    "ssl_verify_cert": False,
    "ssl_verify_identity": False,
}

# OpenAI Configuration
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

# Flask Configuration
DEBUG = True
SECRET_KEY = "your-secret-key-here-change-in-production"
