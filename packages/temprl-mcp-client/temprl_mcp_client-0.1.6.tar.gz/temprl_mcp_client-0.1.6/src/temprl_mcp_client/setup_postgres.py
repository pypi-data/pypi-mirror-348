#!/usr/bin/env python

"""
Set up the PostgreSQL database for the Temprl MCP client.
This script will create the necessary tables for storing chat history.
"""

import os
import sys
import dotenv
from pathlib import Path

# Load environment variables from .env file
dotenv.load_dotenv()

# Import from the package
from temprl_mcp_client.db import init_db, get_connection

def main():
    """Initialize the PostgreSQL database."""
    print("Setting up PostgreSQL database for chat memory storage...")
    
    try:
        # Try to connect to the database to verify connection
        conn = get_connection()
        print("Successfully connected to PostgreSQL database.")
        conn.close()
        
        # Initialize the database tables
        init_db()
        print("Successfully created database tables.")
        
        print("\nDatabase setup complete! You can now use the chat memory system with PostgreSQL.")
    except Exception as e:
        print(f"Error setting up database: {e}")
        print("\nPlease check your PostgreSQL connection settings in the .env file:")
        print(f"  POSTGRES_HOST={os.environ.get('POSTGRES_HOST', 'localhost')}")
        print(f"  POSTGRES_PORT={os.environ.get('POSTGRES_PORT', '5432')}")
        print(f"  POSTGRES_DB={os.environ.get('POSTGRES_DB', 'temprl_mcp')}")
        print(f"  POSTGRES_USER={os.environ.get('POSTGRES_USER', 'postgres')}")
        print(f"  POSTGRES_PASSWORD={os.environ.get('POSTGRES_PASSWORD', '***')}")
        
        print("\nMake sure PostgreSQL is running and the database exists.")
        print("You may need to create the database manually with:")
        print(f"  CREATE DATABASE {os.environ.get('POSTGRES_DB', 'temprl_mcp')};")
        
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 