# This is the entry point for Vercel's Python Serverless Function
# It wraps your Flask app for deployment as an API route

from backend.app import app as vercel_app

# Vercel will use 'app' as the entry point
app = vercel_app
