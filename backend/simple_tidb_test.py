"""
Simple TiDB connection test using the exact recommended method
"""

import pymysql
import ssl
from config import TIDB_CONFIG

def test_basic_connection():
    """Test basic connection without SSL first"""
    try:
        print("🔍 Testing basic connection (no SSL)...")
        connection = pymysql.connect(
            host=TIDB_CONFIG['host'],
            port=TIDB_CONFIG['port'],
            user=TIDB_CONFIG['user'],
            password=TIDB_CONFIG['password'],
            database=TIDB_CONFIG['database'],
            connect_timeout=30
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✅ Basic connection successful! Result: {result}")
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Basic connection failed: {e}")
        return False

def test_ssl_connection():
    """Test with proper SSL context"""
    try:
        print("\n🔍 Testing SSL connection...")
        
        # Create SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        connection = pymysql.connect(
            host=TIDB_CONFIG['host'],
            port=TIDB_CONFIG['port'],
            user=TIDB_CONFIG['user'],
            password=TIDB_CONFIG['password'],
            database=TIDB_CONFIG['database'],
            ssl=ssl_context,
            connect_timeout=30
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        result = cursor.fetchone()
        print(f"✅ SSL connection successful! TiDB Version: {result}")
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ SSL connection failed: {e}")
        return False

def test_minimal_ssl():
    """Test minimal SSL configuration"""
    try:
        print("\n🔍 Testing minimal SSL...")
        
        connection = pymysql.connect(
            host=TIDB_CONFIG['host'],
            port=TIDB_CONFIG['port'],
            user=TIDB_CONFIG['user'],
            password=TIDB_CONFIG['password'],
            database=TIDB_CONFIG['database'],
            ssl={'check_hostname': False},
            connect_timeout=30
        )
        
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print(f"✅ Minimal SSL successful! Available databases: {databases}")
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Minimal SSL failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TiDB Connection Test - Simplified")
    print("=" * 50)
    print(f"Connecting to: {TIDB_CONFIG['host']}:{TIDB_CONFIG['port']}")
    print(f"Database: {TIDB_CONFIG['database']}")
    print(f"User: {TIDB_CONFIG['user']}")
    
    # Try different connection methods
    success = False
    
    # Test 1: Basic connection
    if test_basic_connection():
        success = True
    
    # Test 2: SSL connection
    elif test_ssl_connection():
        success = True
    
    # Test 3: Minimal SSL
    elif test_minimal_ssl():
        success = True
    
    if success:
        print("\n🎉 Connection successful! TiDB is working.")
        print("You can now update your Flask app to use the working method.")
    else:
        print("\n❌ All connection attempts failed.")
        print("\nPossible solutions:")
        print("1. Check if 'test' database exists in your TiDB cluster")
        print("2. Try creating a new database in TiDB Cloud console")
        print("3. Verify username/password are correct")
        print("4. Continue with mock database for now")
        print("\n💡 For hackathon purposes, the mock database works perfectly!")
        print("You can demonstrate all features and fix TiDB connection later.")
