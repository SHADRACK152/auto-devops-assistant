"""
Simple TiDB connection test script
"""

import pymysql
from config import TIDB_CONFIG

def test_direct_connection():
    """Test direct PyMySQL connection"""
    try:
        print("🔍 Testing direct PyMySQL connection...")
        print(f"Host: {TIDB_CONFIG['host']}")
        print(f"Port: {TIDB_CONFIG['port']}")
        print(f"User: {TIDB_CONFIG['user']}")
        print(f"Database: {TIDB_CONFIG['database']}")
        
        connection = pymysql.connect(
            host=TIDB_CONFIG['host'],
            port=TIDB_CONFIG['port'],
            user=TIDB_CONFIG['user'],
            password=TIDB_CONFIG['password'],
            database=TIDB_CONFIG['database'],
            ssl_disabled=False,
            ssl_verify_cert=False,
            ssl_verify_identity=False,
            connect_timeout=30,
            autocommit=True
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        print(f"✅ Connection successful! Result: {result}")
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    try:
        from sqlalchemy import create_engine, text
        
        print("\n🔍 Testing SQLAlchemy connection...")
        
        uri = (f"mysql+pymysql://{TIDB_CONFIG['user']}:"
               f"{TIDB_CONFIG['password']}@{TIDB_CONFIG['host']}:"
               f"{TIDB_CONFIG['port']}/{TIDB_CONFIG['database']}"
               f"?ssl_disabled=false&ssl_verify_cert=false&ssl_verify_identity=false")
        
        print(f"URI: {uri.replace(TIDB_CONFIG['password'], '***')}")
        
        engine = create_engine(uri, pool_timeout=20, pool_recycle=3600)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            value = result.fetchone()[0]
            print(f"✅ SQLAlchemy connection successful! Result: {value}")
            return True
            
    except Exception as e:
        print(f"❌ SQLAlchemy connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TiDB Connection Test")
    print("=" * 50)
    
    # Test direct PyMySQL connection
    direct_success = test_direct_connection()
    
    # Test SQLAlchemy connection
    sqlalchemy_success = test_sqlalchemy_connection()
    
    print("\n" + "=" * 50)
    if direct_success and sqlalchemy_success:
        print("🎉 All connection tests passed!")
    else:
        print("❌ Some connection tests failed.")
        print("\nTroubleshooting tips:")
        print("1. Check if your TiDB cluster is running")
        print("2. Verify credentials are correct")
        print("3. Check network connectivity")
        print("4. Make sure you're using the correct host/port")
