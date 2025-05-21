"""
PostgreSQL Configuration Tool
This script helps configure the PostgreSQL connection details for the application
"""
import os
import sys
import getpass
from configparser import ConfigParser

def configure_postgresql():
    print("=" * 70)
    print("PostgreSQL Configuration Tool for Music App Backend")
    print("=" * 70)
    print("\nThis tool will help you configure your PostgreSQL connection.\n")
    print("PgAdmin Default Settings:")
    print("- Default username is usually 'postgres'")
    print("- Port is usually '5432'")
    print("- You need to provide the password you set during PostgreSQL installation")
    print("- You can find your databases in the PgAdmin interface\n")
    
    # Get configuration details
    db_user = input("Enter PostgreSQL username [postgres]: ") or "postgres"
    # Use getpass to hide password input, but provide a default
    db_password = getpass.getpass("Enter PostgreSQL password [fuckUpostgre01]: ") or "fuckUpostgre01"
    
    db_host = input("Enter PostgreSQL host [localhost]: ") or "localhost"
    db_port = input("Enter PostgreSQL port [5432]: ") or "5432"
    db_name = input("Enter database name [musicapp]: ") or "musicapp"
    
    # Create .env file if it doesn't exist
    env_file = ".env"
    
    # Check if file exists and if we should overwrite
    if os.path.exists(env_file):
        overwrite = input(f"{env_file} already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Configuration cancelled.")
            return
    
    # Try to connect to the database to verify credentials
    try:
        from sqlalchemy import create_engine
        connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        print("\nTesting connection to PostgreSQL...")
        engine = create_engine(connection_string)
        
        # Try to connect to server first, then check if database exists
        try:
            connection = engine.connect()
            connection.close()
            print("Connection successful!")
            database_exists = True
        except Exception as e:
            if "does not exist" in str(e):
                # Database doesn't exist, but server connection works
                print(f"Database '{db_name}' does not exist, but server connection is good.")
                create_db = input(f"Do you want to create the database '{db_name}'? (y/n): ")
                if create_db.lower() == 'y':
                    # Create database by connecting to 'postgres' database first
                    postgres_conn_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/postgres"
                    postgres_engine = create_engine(postgres_conn_string)
                    postgres_conn = postgres_engine.connect()
                    postgres_conn.execute("COMMIT")  # End current transaction
                    postgres_conn.execute(f"CREATE DATABASE {db_name}")
                    postgres_conn.close()
                    print(f"Database '{db_name}' created successfully!")
                    database_exists = True
                else:
                    print("Database creation cancelled.")
                    database_exists = False
            else:
                # Other connection error
                print(f"\nError: Could not connect to PostgreSQL: {e}")
                print("\nPlease check your PostgreSQL installation and credentials.")
                print("Make sure PostgreSQL is running.")
                return
        
        if database_exists:
            # Write to .env file
            with open(env_file, 'w') as f:
                f.write(f"SECRET_KEY=e300f5d8ad7e400815ee6cc71587b012\n")
                f.write(f"DB_USER={db_user}\n")
                f.write(f"DB_PASSWORD={db_password}\n")
                f.write(f"DB_HOST={db_host}\n")
                f.write(f"DB_PORT={db_port}\n")
                f.write(f"DB_NAME={db_name}\n")
                f.write(f"DATABASE_URI=postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}\n")
                f.write(f"SPOTIFY_CLIENT_ID=dummy_client_id\n")
                f.write(f"SPOTIFY_CLIENT_SECRET=dummy_client_secret\n")
                f.write(f"SPOTIFY_REDIRECT_URI=http://localhost:5000/callback\n")
            
            print(f"\nConfiguration saved to {env_file}")
            print("\nNext steps:")
            print("1. Run 'flask db init' to initialize the migrations")
            print("2. Run 'flask db migrate -m \"initial migration\"' to create a migration")
            print("3. Run 'flask db upgrade' to apply the migration")
            print("4. Start the application with 'python run.py'")
    except Exception as e:
        print(f"\nError: Could not connect to PostgreSQL: {e}")
        print("\nPlease check your PostgreSQL installation and credentials.")
        print("Make sure PostgreSQL is running and the database exists.")
        print("\nTo create the database, connect to PostgreSQL and run:")
        print(f"  CREATE DATABASE {db_name};")
        
if __name__ == "__main__":
    configure_postgresql() 