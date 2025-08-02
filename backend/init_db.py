"""
Database initialization script for Auto DevOps Assistant
Creates tables for storing deployment logs and embeddings
"""

from sqlalchemy import create_engine, text
from config import TIDB_CONFIG
import sys

def create_connection():
    """Create database connection"""
    try:
        import ssl
        
        # Create SSL context (the working method)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Build connection URI
        uri = (f"mysql+pymysql://{TIDB_CONFIG['user']}:"
               f"{TIDB_CONFIG['password']}@{TIDB_CONFIG['host']}:"
               f"{TIDB_CONFIG['port']}/{TIDB_CONFIG['database']}")
        
        # SSL connection args
        connect_args = {"ssl": ssl_context}
        
        engine = create_engine(uri, connect_args=connect_args, 
                             pool_timeout=30, pool_recycle=3600)
        return engine
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables(engine):
    """Create necessary tables for the application"""
    
    # Table for storing deployment logs
    create_logs_table = """
    CREATE TABLE IF NOT EXISTS deployment_logs (
        id VARCHAR(36) PRIMARY KEY,
        content TEXT NOT NULL,
        source VARCHAR(100) DEFAULT 'unknown',
        severity VARCHAR(20) DEFAULT 'info',
        summary TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_timestamp (timestamp),
        INDEX idx_source (source),
        INDEX idx_severity (severity)
    );
    """
    
    # Table for storing log embeddings (for vector search)
    create_embeddings_table = """
    CREATE TABLE IF NOT EXISTS log_embeddings (
        id VARCHAR(36) PRIMARY KEY,
        log_id VARCHAR(36) NOT NULL,
        embedding_vector TEXT NOT NULL,
        model_name VARCHAR(100) DEFAULT 'sentence-transformers',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (log_id) REFERENCES deployment_logs(id) ON DELETE CASCADE,
        INDEX idx_log_id (log_id)
    );
    """
    
    # Table for storing error patterns and fixes
    create_fixes_table = """
    CREATE TABLE IF NOT EXISTS error_fixes (
        id VARCHAR(36) PRIMARY KEY,
        error_pattern VARCHAR(500) NOT NULL,
        error_type VARCHAR(100) NOT NULL,
        fix_suggestion TEXT NOT NULL,
        fix_code TEXT,
        confidence_score DECIMAL(3,2) DEFAULT 0.50,
        usage_count INT DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        INDEX idx_error_type (error_type),
        INDEX idx_pattern (error_pattern(100))
    );
    """
    
    try:
        with engine.connect() as connection:
            print("Creating deployment_logs table...")
            connection.execute(text(create_logs_table))
            connection.commit()
            
            print("Creating log_embeddings table...")
            connection.execute(text(create_embeddings_table))
            connection.commit()
            
            print("Creating error_fixes table...")
            connection.execute(text(create_fixes_table))
            connection.commit()
            
        print("✅ All tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def test_connection(engine):
    """Test database connection"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 as test"))
            test_value = result.fetchone()[0]
            if test_value == 1:
                print("✅ Database connection successful!")
                return True
            else:
                print("❌ Database connection test failed")
                return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def show_tables(engine):
    """Show all tables in the database"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            print("\n📋 Tables in database:")
            for table in tables:
                print(f"  - {table[0]}")
    except Exception as e:
        print(f"Error showing tables: {e}")

if __name__ == "__main__":
    print("🚀 Initializing Auto DevOps Assistant Database...")
    
    # Create connection
    engine = create_connection()
    if not engine:
        print("❌ Failed to connect to database. Check your config.py settings.")
        sys.exit(1)
    
    # Test connection
    if not test_connection(engine):
        print("❌ Database connection test failed.")
        sys.exit(1)
    
    # Create tables
    if create_tables(engine):
        print("\n🎉 Database initialization completed successfully!")
        show_tables(engine)
    else:
        print("❌ Database initialization failed.")
        sys.exit(1)
