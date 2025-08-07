#!/bin/bash
# Railway Environment Variables Setup Script
# Run this after deploying to Railway

echo "🔐 Setting up secure environment variables in Railway..."
echo ""
echo "📋 COPY THESE VARIABLES TO RAILWAY DASHBOARD:"
echo "   Go to: https://railway.app/dashboard"
echo "   Select: auto-devops-assistant project"
echo "   Click: Variables tab"
echo "   Add each variable below:"
echo ""

echo "🤖 AI Configuration:"
echo "GROQ_API_KEY=your-groq-api-key-here"
echo ""

echo "🗄️  Database Configuration:"
echo "TIDB_HOST=your-tidb-host"
echo "TIDB_PORT=4000"
echo "TIDB_USER=your-tidb-username"
echo "TIDB_PASSWORD=your-tidb-password"
echo "TIDB_DATABASE=test"
echo ""

echo "⚙️  Flask Configuration:"
echo "FLASK_ENV=production"
echo "PORT=5000"
echo ""

echo "✅ After adding these variables, Railway will automatically redeploy!"
echo "🚀 Your Auto DevOps Assistant will then have full AI and database functionality!"
