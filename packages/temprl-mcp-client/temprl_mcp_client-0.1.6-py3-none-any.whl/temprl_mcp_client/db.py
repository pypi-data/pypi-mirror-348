"""
Database operations for PostgreSQL integration with ChatMemory.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
import psycopg2
from psycopg2.extras import DictCursor

def get_postgres_connection(
    host: str = 'localhost',
    port: str = '5432',
    database: str = 'postgres',
    user: str = 'postgres',
    password: str = ''
):
    """Get a PostgreSQL connection using provided parameters."""
    return psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

def init_db(
    host: str,
    port: str,
    database: str,
    user: str,
    password: str
):
    """Initialize the PostgreSQL database tables."""
    conn = get_postgres_connection(host, port, database, user, password)
    cursor = conn.cursor()
    
    try:
        # Create conversations table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_conversations (
            uuid TEXT PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            metadata JSONB DEFAULT '{}'::jsonb
        )
        ''')
        
        # Create messages table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id SERIAL PRIMARY KEY,
            conversation_uuid TEXT REFERENCES chat_conversations(uuid) ON DELETE CASCADE,
            index_num INTEGER,
            role TEXT,
            content TEXT,
            tool_calls JSONB,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(conversation_uuid, index_num)
        )
        ''')
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()

def save_conversation(
    chat_id: str,
    title: str,
    created_at: str,
    updated_at: str,
    metadata: Dict,
    host: str,
    port: str,
    database: str,
    user: str,
    password: str
):
    """Save conversation metadata to PostgreSQL."""
    conn = get_postgres_connection(host, port, database, user, password)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO chat_conversations (uuid, title, created_at, updated_at, metadata)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (uuid) DO UPDATE
        SET title = EXCLUDED.title,
            updated_at = EXCLUDED.updated_at,
            metadata = EXCLUDED.metadata
        ''', (chat_id, title, created_at, updated_at, json.dumps(metadata)))
        
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def save_messages(
    chat_id: str,
    messages: List[Dict],
    host: str,
    port: str,
    database: str,
    user: str,
    password: str
):
    """Save messages to PostgreSQL."""
    conn = get_postgres_connection(host, port, database, user, password)
    cursor = conn.cursor()
    
    try:
        # Clear existing messages for this conversation
        cursor.execute('DELETE FROM chat_messages WHERE conversation_uuid = %s', (chat_id,))
        
        # Insert all messages
        for i, message in enumerate(messages):
            tool_calls = json.dumps(message.get("tool_calls", [])) if "tool_calls" in message else None
            cursor.execute('''
            INSERT INTO chat_messages 
            (conversation_uuid, index_num, role, content, tool_calls, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                chat_id,
                i,
                message.get("role", ""),
                message.get("content", ""),
                tool_calls,
                datetime.now()
            ))
        
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def load_conversation(
    chat_id: str,
    host: str,
    port: str,
    database: str,
    user: str,
    password: str
) -> Optional[Dict]:
    """Load conversation metadata from PostgreSQL."""
    conn = get_postgres_connection(host, port, database, user, password)
    cursor = conn.cursor(cursor_factory=DictCursor)
    
    try:
        cursor.execute('''
        SELECT uuid, title, created_at, updated_at, metadata
        FROM chat_conversations WHERE uuid = %s
        ''', (chat_id,))
        
        result = cursor.fetchone()
        if result:
            return dict(result)
        return None
    finally:
        cursor.close()
        conn.close()

def load_messages(
    chat_id: str,
    host: str,
    port: str,
    database: str,
    user: str,
    password: str
) -> List[Dict]:
    """Load messages from PostgreSQL."""
    conn = get_postgres_connection(host, port, database, user, password)
    cursor = conn.cursor(cursor_factory=DictCursor)
    
    try:
        cursor.execute('''
        SELECT role, content, tool_calls
        FROM chat_messages 
        WHERE conversation_uuid = %s 
        ORDER BY index_num
        ''', (chat_id,))
        
        messages = []
        for row in cursor.fetchall():
            message = {
                "role": row["role"],
                "content": row["content"]
            }
            if row["tool_calls"]:
                message["tool_calls"] = json.loads(row["tool_calls"])
            messages.append(message)
        
        return messages
    finally:
        cursor.close()
        conn.close()

def list_conversations(
    limit: int = 10,
    host: str = 'localhost',
    port: str = '5432',
    database: str = 'postgres',
    user: str = 'postgres',
    password: str = ''
) -> List[Dict]:
    """List recent conversations from PostgreSQL."""
    conn = get_postgres_connection(host, port, database, user, password)
    cursor = conn.cursor(cursor_factory=DictCursor)
    
    try:
        cursor.execute('''
        SELECT c.uuid as chat_id, c.title, c.created_at, c.updated_at,
               COUNT(m.id) as message_count
        FROM chat_conversations c
        LEFT JOIN chat_messages m ON c.uuid = m.conversation_uuid
        GROUP BY c.uuid, c.title, c.created_at, c.updated_at
        ORDER BY c.updated_at DESC
        LIMIT %s
        ''', (limit,))
        
        return [dict(row) for row in cursor.fetchall()]
    finally:
        cursor.close()
        conn.close()

def delete_conversation(
    chat_id: str,
    host: str,
    port: str,
    database: str,
    user: str,
    password: str
) -> bool:
    """Delete a conversation and its messages from PostgreSQL."""
    conn = get_postgres_connection(host, port, database, user, password)
    cursor = conn.cursor()
    
    try:
        # Messages will be deleted automatically due to CASCADE
        cursor.execute('DELETE FROM chat_conversations WHERE uuid = %s', (chat_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        return deleted
    except Exception:
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close() 