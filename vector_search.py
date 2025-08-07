#!/usr/bin/env python3
"""
TiDB Vector Search Integration for Deployment Pattern Matching
"""

import os
import json
import numpy as np
from typing import List, Dict, Any
from sqlalchemy import create_engine, text
from config import TIDB_CONFIG

class DeploymentVectorSearch:
    """Vector search for similar deployment issues using TiDB Serverless"""
    
    def __init__(self):
        self.engine = self._create_tidb_connection()
        self._ensure_vector_tables()
    
    def _create_tidb_connection(self):
        """Create TiDB connection with vector search capabilities"""
        try:
            import ssl
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            uri = (f"mysql+pymysql://{TIDB_CONFIG['user']}:"
                   f"{TIDB_CONFIG['password']}@{TIDB_CONFIG['host']}:"
                   f"{TIDB_CONFIG['port']}/{TIDB_CONFIG['database']}")
            
            return create_engine(uri, connect_args={"ssl": ssl_context})
        except Exception as e:
            print(f"⚠️ TiDB Vector Search unavailable: {e}")
            return None
    
    def _ensure_vector_tables(self):
        """Create vector search tables if they don't exist"""
        if not self.engine:
            return
            
        try:
            with self.engine.connect() as conn:
                # Deployment patterns table with vector embeddings
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS deployment_patterns (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        pattern_hash VARCHAR(64) UNIQUE,
                        log_content TEXT,
                        error_patterns JSON,
                        solutions JSON,
                        embedding VECTOR(384),
                        success_rate FLOAT DEFAULT 0.0,
                        usage_count INT DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    )
                """))
                
                # Create vector index separately with proper TiDB syntax
                try:
                    # First, add TiFlash replica for vector index support
                    print("🔧 Setting up TiFlash replica for vector search...")
                    conn.execute(text("""
                        ALTER TABLE deployment_patterns SET TIFLASH REPLICA 1
                    """))
                    print("✅ TiFlash replica configured")
                    
                    # Now create the vector index
                    conn.execute(text("""
                        CREATE VECTOR INDEX idx_embedding 
                        ON deployment_patterns ((VEC_COSINE_DISTANCE(embedding)))
                    """))
                    print("✅ Vector index created successfully")
                except Exception as index_error:
                    # Try the alternative approach if TiFlash setup fails
                    if "columnar replica" in str(index_error).lower():
                        try:
                            print("🔧 Trying alternative vector index creation...")
                            conn.execute(text("""
                                ALTER TABLE deployment_patterns 
                                ADD VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding))) 
                                ADD_COLUMNAR_REPLICA_ON_DEMAND
                            """))
                            print("✅ Vector index created with on-demand replica")
                        except Exception as alt_error:
                            print(f"⚠️ Vector index creation info: {alt_error}")
                            print("💡 Vector search will work without index (slower performance)")
                    elif "already exists" not in str(index_error).lower():
                        print(f"⚠️ Vector index creation info: {index_error}")
                    else:
                        print("✅ Vector index already exists")
                
                # Solution effectiveness tracking
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS solution_feedback (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        pattern_id INT,
                        solution_id VARCHAR(64),
                        user_rating ENUM('excellent', 'good', 'fair', 'poor'),
                        was_helpful BOOLEAN,
                        feedback_text TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (pattern_id) REFERENCES deployment_patterns(id)
                    )
                """))
                
                conn.commit()
                print("✅ Vector search tables ready")
        except Exception as e:
            print(f"⚠️ Vector table creation failed: {e}")
    
    def find_similar_patterns(self, log_content: str, limit: int = 5) -> List[Dict]:
        """Find similar deployment patterns using vector search"""
        if not self.engine:
            return []
        
        try:
            # Generate embedding for current log (simplified - would use actual embedding model)
            embedding = self._generate_embedding(log_content)
            
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT 
                        pattern_hash,
                        log_content,
                        error_patterns,
                        solutions,
                        success_rate,
                        usage_count,
                        VEC_COSINE_DISTANCE(embedding, :embedding_vec) as similarity
                    FROM deployment_patterns
                    ORDER BY similarity ASC
                    LIMIT :limit
                """), {
                    "embedding_vec": str(embedding.tolist()),
                    "limit": limit
                })
                
                patterns = []
                for row in result:
                    patterns.append({
                        "pattern_hash": row.pattern_hash,
                        "log_content": row.log_content,
                        "error_patterns": json.loads(row.error_patterns),
                        "solutions": json.loads(row.solutions),
                        "success_rate": row.success_rate,
                        "usage_count": row.usage_count,
                        "similarity": row.similarity
                    })
                
                return patterns
        except Exception as e:
            print(f"❌ Vector search failed: {e}")
            return []
    
    def store_deployment_pattern(self, log_content: str, patterns: List[Dict], solutions: List[Dict]) -> str:
        """Store new deployment pattern with vector embedding"""
        if not self.engine:
            return "local_pattern"
        
        try:
            pattern_hash = str(hash(log_content))[:16]
            embedding = self._generate_embedding(log_content)
            
            with self.engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO deployment_patterns 
                    (pattern_hash, log_content, error_patterns, solutions, embedding)
                    VALUES (:hash, :content, :patterns, :solutions, :embedding_vec)
                    ON DUPLICATE KEY UPDATE
                    usage_count = usage_count + 1,
                    updated_at = CURRENT_TIMESTAMP
                """), {
                    "hash": pattern_hash,
                    "content": log_content,
                    "patterns": json.dumps(patterns),
                    "solutions": json.dumps(solutions),
                    "embedding_vec": str(embedding.tolist())
                })
                
                conn.commit()
                print(f"✅ Pattern stored: {pattern_hash}")
                return pattern_hash
        except Exception as e:
            print(f"❌ Pattern storage failed: {e}")
            return "storage_failed"
    
    def record_solution_feedback(self, pattern_id: str, solution_id: str, rating: str, helpful: bool, feedback: str = ""):
        """Record user feedback for solution effectiveness"""
        if not self.engine:
            return
        
        try:
            with self.engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO solution_feedback 
                    (pattern_id, solution_id, user_rating, was_helpful, feedback_text)
                    SELECT id, :solution_id, :rating, :helpful, :feedback
                    FROM deployment_patterns 
                    WHERE pattern_hash = :pattern_id
                """), {
                    "pattern_id": pattern_id,
                    "solution_id": solution_id,
                    "rating": rating,
                    "helpful": helpful,
                    "feedback": feedback
                })
                
                conn.commit()
                print(f"✅ Feedback recorded for {pattern_id}")
        except Exception as e:
            print(f"❌ Feedback recording failed: {e}")
    
    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate vector embedding for text (simplified implementation)"""
        # In production, use a proper embedding model like sentence-transformers
        # For demo, create a simple hash-based embedding
        import hashlib
        
        # Create deterministic embedding based on text features
        words = text.lower().split()
        embedding = np.zeros(384)  # Standard sentence embedding size
        
        for i, word in enumerate(words[:50]):  # Use first 50 words
            word_hash = int(hashlib.md5(word.encode()).hexdigest(), 16)
            embedding[i % 384] += (word_hash % 100) / 100.0
        
        # Normalize
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning and usage statistics"""
        if not self.engine:
            return {"status": "offline", "patterns": 0, "feedback": 0}
        
        try:
            with self.engine.connect() as conn:
                stats = conn.execute(text("""
                    SELECT 
                        COUNT(*) as total_patterns,
                        AVG(success_rate) as avg_success_rate,
                        SUM(usage_count) as total_usage,
                        (SELECT COUNT(*) FROM solution_feedback) as feedback_count
                    FROM deployment_patterns
                """)).fetchone()
                
                return {
                    "status": "active",
                    "patterns": stats.total_patterns,
                    "avg_success_rate": float(stats.avg_success_rate or 0),
                    "total_usage": stats.total_usage,
                    "feedback_count": stats.feedback_count
                }
        except Exception as e:
            print(f"❌ Stats query failed: {e}")
            return {"status": "error", "patterns": 0, "feedback": 0}

# Global instance
vector_search = DeploymentVectorSearch()
