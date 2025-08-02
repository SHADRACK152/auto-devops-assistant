"""
TiDB Serverless connection troubleshooting script
"""

import pymysql
from config import TIDB_CONFIG

def test_different_ssl_configs():
    """Test various SSL configurations for TiDB Serverless"""
    
    configs = [
        {
            "name": "SSL Disabled",
            "params": {
                "ssl_disabled": True,
            }
        },
        {
            "name": "SSL Enabled - No Verification",
            "params": {
                "ssl_disabled": False,
                "ssl_verify_cert": False,
                "ssl_verify_identity": False,
            }
        },
        {
            "name": "SSL Enabled - With SSL CA Empty",
            "params": {
                "ssl_disabled": False,
                "ssl_ca": "",
                "ssl_verify_cert": False,
                "ssl_verify_identity": False,
            }
        },
        {
            "name": "Minimal SSL",
            "params": {
                "ssl": True,
            }
        }
    ]
    
    for config in configs:
        print(f"\n🔍 Testing: {config['name']}")
        print("-" * 40)
        
        try:
            connection = pymysql.connect(
                host=TIDB_CONFIG['host'],
                port=TIDB_CONFIG['port'],
                user=TIDB_CONFIG['user'],
                password=TIDB_CONFIG['password'],
                database=TIDB_CONFIG['database'],
                connect_timeout=30,
                read_timeout=30,
                write_timeout=30,
                **config['params']
            )
            
            cursor = connection.cursor()
            cursor.execute("SELECT 1, 'Connection successful!'")
            result = cursor.fetchone()
            
            print(f"✅ SUCCESS! Result: {result}")
            cursor.close()
            connection.close()
            return config
            
        except Exception as e:
            print(f"❌ Failed: {str(e)[:100]}...")
    
    return None

def test_with_charset():
    """Test with explicit charset"""
    try:
        print("\n🔍 Testing with charset=utf8mb4")
        print("-" * 40)
        
        connection = pymysql.connect(
            host=TIDB_CONFIG['host'],
            port=TIDB_CONFIG['port'],
            user=TIDB_CONFIG['user'],
            password=TIDB_CONFIG['password'],
            database=TIDB_CONFIG['database'],
            charset='utf8mb4',
            ssl_disabled=False,
            ssl_verify_cert=False,
            ssl_verify_identity=False,
            connect_timeout=30
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        result = cursor.fetchone()
        
        print(f"✅ SUCCESS! TiDB Version: {result}")
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TiDB Serverless Connection Troubleshooting")
    print("=" * 50)
    
    print(f"Host: {TIDB_CONFIG['host']}")
    print(f"Port: {TIDB_CONFIG['port']}")
    print(f"User: {TIDB_CONFIG['user']}")
    print(f"Database: {TIDB_CONFIG['database']}")
    
    # Test different SSL configurations
    working_config = test_different_ssl_configs()
    
    if working_config:
        print(f"\n🎉 Found working configuration: {working_config['name']}")
        print("You can update your app.py with these parameters:")
        print(working_config['params'])
    else:
        print("\n❌ No SSL configuration worked. Trying other approaches...")
        
        # Test with charset
        charset_success = test_with_charset()
        
        if not charset_success:
            print("\n🤔 Possible issues:")
            print("1. User credentials might be incorrect")
            print("2. Database 'test' might not exist")
            print("3. TiDB cluster might have IP restrictions")
            print("4. Try creating a new database in TiDB Cloud")
            print("\nSuggestion: For now, let's continue with mock database and fix this later.")
