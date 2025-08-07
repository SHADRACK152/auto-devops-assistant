#!/usr/bin/env python3
"""
Simple script to test environment variable loading
"""
import os

print("=== Environment Variable Test ===")
print(f"PORT: {os.getenv('PORT', 'NOT_SET')}")
print(f"RAILWAY_ENVIRONMENT: {os.getenv('RAILWAY_ENVIRONMENT', 'NOT_SET')}")
print(f"GROQ_API_KEY: {'SET' if os.getenv('GROQ_API_KEY') else 'NOT_SET'}")
print(f"TIDB_HOST: {'SET' if os.getenv('TIDB_HOST') else 'NOT_SET'}")
print(f"TIDB_USER: {'SET' if os.getenv('TIDB_USER') else 'NOT_SET'}")
print(f"TIDB_PASSWORD: {'SET' if os.getenv('TIDB_PASSWORD') else 'NOT_SET'}")
print(f"TIDB_DATABASE: {'SET' if os.getenv('TIDB_DATABASE') else 'NOT_SET'}")

print("\n=== All Environment Variables ===")
env_vars = list(os.environ.keys())
print(f"Total environment variables: {len(env_vars)}")
print(f"First 20 variables: {env_vars[:20]}")

# Look for Railway-specific variables
railway_vars = [k for k in env_vars if 'railway' in k.lower()
                or 'groq' in k.lower() or 'tidb' in k.lower()]
print(f"\nRailway/GROQ/TIDB related variables: {railway_vars}")
