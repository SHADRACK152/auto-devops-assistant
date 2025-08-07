import os

# TiDB Serverless Configuration
# Your actual TiDB Cloud connection details
TIDB_CONFIG = {
    "host": "gateway01.eu-central-1.prod.aws.tidbcloud.com",
    "port": 4000,
    "user": "t5uTfqdrPKmAXCN.root",
    "password": "Nc6IzB7h26LPTi25",
    "database": "test",  # later
    "ssl_disabled": False,  # Enable SSL for TiDB Serverless
    "ssl_verify_cert": False,  # Skip certificate verification for simplicity
    "ssl_verify_identity": False,
}

# OpenAI Configuration for AI-powered log analysis
# Get your API key from: https://platform.openai.com/api-keys

# Try to get OpenAI API key from environment variable first, then fallback
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-your-openai-api-key-here")

# Online AI Configuration (Free APIs!)
# Groq: Get free API key from https://console.groq.com/
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# Hugging Face: Get free API token from https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
# Together AI: Get $25 free credits from https://together.ai/
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY", "")
# Cohere: Get free API key from https://cohere.ai/
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")

# AI Analysis Settings
# Enable AI features (will fallback to pattern recognition if no API key)
AI_ENABLED = True
AI_MODEL = "gpt-3.5-turbo"
# Use advanced pattern recognition when OpenAI unavailable
FALLBACK_TO_PATTERNS = True
AI_MAX_TOKENS = 1000
AI_TEMPERATURE = 0.3

# Flask Configuration
DEBUG = True
SECRET_KEY = "508080"
