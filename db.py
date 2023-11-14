import psycopg2
import os

def get_conn():
    # create connection
    conn = psycopg2.connect(os.environ.get("EXTERNAL_CONNECTION_STRING")

    # Return connection to database
    return conn

def init_db():
    # get connection
    conn = get_conn()

    # get cursor
    cur = conn.cursor()

    cur.execute("""
        DROP TABLE IF EXISTS products;
   	 
    	  CREATE TABLE products (
      	id INTEGER PRIMARY KEY,
      	name TEXT UNIQUE NOT NULL,
      	quantity INTEGER NOT NULL
    	  );
    """)
    cur.close()
    conn.commit()
    conn.close()
